# -*- coding: utf-8 -*-

import math
import subprocess
import tempfile

from dataclasses import dataclass
from pathlib import Path

__version__ = "0.0"

# Raw R code, inserted as is, for anything Python values can't express,
# e.g. functions (scales::percent) or expressions in aes (factor(cyl)).
class R(str): pass

def to_r(value):
    match value:
        case R(): return value
        case None: return "NULL"
        case True: return "TRUE"
        case False: return "FALSE"
        case int(): return str(value)
        case float() if math.isnan(value): return "NA"
        case float() if math.isinf(value): return "Inf" if value > 0 else "-Inf"
        case float(): return repr(value)
        case str(): return '"{}"'.format(value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n"))
        case list(): return "c({})".format(", ".join(map(to_r, value)))
        case tuple(): return "c({})".format(", ".join(map(to_r, value)))
        case dict(): return "c({})".format(", ".join(f"`{k}`={to_r(v)}" for k, v in value.items()))
        case _: raise TypeError(f"Can't convert {type(value)} to R")

def to_r_aes(aes):
    return "aes({})".format(", ".join(f"{k}={v if isinstance(v, R) else f'`{v}`'}"
                                      for k, v in aes.items()))

@dataclass
class Call:
    name: str
    args: tuple
    kwargs: dict

class plot:

    def __init__(self, data, x=None, y=None, **aes):
        self.data = data
        self.aes = {k: v for k, v in dict(x=x, y=y, **aes).items() if v is not None}
        self.calls = []

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        def call(*args, **kwargs):
            new = plot(self.data, **self.aes)
            new.calls = self.calls + [Call(name, args, kwargs)]
            return new
        return call

    def plot_to_r(self):
        calls = list(self.calls)
        if not any(x.name.startswith(("geom_", "stat_")) for x in calls):
            name = "geom_point" if "y" in self.aes else "geom_histogram"
            calls.insert(0, Call(name, (), {}))
        code = [f"ggplot(data, {to_r_aes(self.aes)})"]
        for call in calls:
            args = [to_r(x) for x in call.args] + [
                f"mapping={to_r_aes(v)}" if k == "aes" else f"{k}={to_r(v)}"
                for k, v in call.kwargs.items()]
            code.append("{}({})".format(call.name, ", ".join(args)))
        return " +\n    ".join(code)

    def save(self, path, width=2400, height=1600, units="px", dpi=200, **kwargs):
        path = Path(path).resolve()
        with tempfile.NamedTemporaryFile(suffix=".parquet") as f:
            data_path = f.name
            write_parquet = getattr(self.data, "write_parquet", None) or self.data.to_parquet
            write_parquet(data_path)
            kwargs = dict(width=width, height=height, units=units, dpi=dpi, **kwargs)
            code = "\n".join((
                f"library(ggplot2)",
                f"library(nanoparquet)",
                f"library(ragg)",
                f"device = getOption('png.device', ragg::agg_png)",
                f"family = getOption('png.family', 'sans')",
                f"data = read_parquet({to_r(str(data_path))})",
                f"plot = {self.plot_to_r()} + theme(text=element_text(family=family))",
                f"ggsave({to_r(str(path))}, plot, {', '.join(f'{k}={to_r(v)}' for k, v in kwargs.items())}, device=device)",
            ))
            print(code)
            subprocess.run(["Rscript", "-e", code], check=True)

    def view(self, **kwargs):
        path = tempfile.NamedTemporaryFile(prefix="ggplot-", suffix=".png", delete=False).name
        self.save(path, **kwargs)
        subprocess.Popen(["/usr/bin/display", path])

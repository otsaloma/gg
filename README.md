# Plot Python Data Frames with ggplot2

gg brings the full power and quality output of R's [ggplot2][] to Python
data frames: [Dataiter][], [Pandas][] and [Polars][]. Nothing is
reimplemented: method calls are passed through to ggplot2 as is, the
data goes to R as a temporary Parquet file and `Rscript` renders the
plot. Everything in ggplot2, including extension packages, is available
and the ggplot2 documentation is the documentation for gg too.

[ggplot2]: https://ggplot2.tidyverse.org/
[Dataiter]: https://github.com/otsaloma/dataiter
[Pandas]: https://pandas.pydata.org/
[Polars]: https://pola.rs/

**Disclaimers:**
- You need R with packages ggplot2, nanoparquet and ragg installed
- Viewing plots uses ImageMagick's `display` (but is easy to change)
- Each plot starts a new R process, which takes about a second
- Arguments are not checked on the Python side; errors come from R
- This is a hack for personal use, the API might change

## Installation

```bash
# Latest development version
pip install -U git+https://github.com/otsaloma/gg
```

## Documentation

```python
import dataiter as di
import gg

data = di.DataFrame.read_csv("../dataiter/data/vehicles.csv")

# View plot (temp PNG file in image viewer)
(gg.plot(data, "year")
   .geom_histogram(binwidth=1, boundary=0)
   .view())

# Save plot to file
(gg.plot(data, "year")
   .geom_histogram(binwidth=1, boundary=0)
   .save("year.png"))
```

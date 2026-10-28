# R's ggplot2 Plotting for Dataiter

TODO

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

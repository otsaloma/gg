#!/usr/bin/env python3

import dataiter as di
import gg

data = di.DataFrame.read_csv("../dataiter/data/vehicles.csv")

(gg.plot(data, "year")
   .geom_histogram(binwidth=1, boundary=0)
   .view())

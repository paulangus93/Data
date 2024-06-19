# Data

Small-scale projects to demonstrate individual skill in dataset analysis. Will update periodically to improve organisation and code quality.

# Projects

1. Chaos Theory (coded, to revise)
2. N-body (coded, to revise)

# Chaos Theory

This is an exercise in visualisation and datamining of a chaotic system. I will iterate a chaotic system, create a bifurcation map, and calculate the Feigenbaum Number and the Lyapunov exponent from the resulting data. These universal constants are known to a high degree of accuracy, thus the code's efficacy can be measured and improved upon by comparison to their established values.

1. The recursive formula x<sub>n + 1</sub> = rx<sub>n</sub>(1 - x<sub>n</sub><sup>2</sup>) is an example of a chaotic system. From this, I will plot a range of n values as a function of r to create a bifurcation map. Inaccuracy can be visualised by plotting the bifurcation at r=2 at small and large n values.

The Feigenbaum Number describes the rate of increase of the bifurcation period with respect to r. It can be determined empirically by visualising any 3 sequential bifurcations, but the first 3 starting at r = 2 is the most accurate. This provides an exercise in data visualisation as steps need to be taken to improve accuracy at high zoom. Data mining is a valuable alternative to determine its value with greater accuracy.

The onset of chaos can be described graphically by referring to the point at which the initial bifurcations intersect, or analytically via calculation of the Lyapunov exponent which represents the rate of divergence. The smallest value of r for which the Lyapunov exponent becomes positive is the point of chaos, and this value can be datamined trivially.

# N-body


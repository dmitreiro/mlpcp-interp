# MLCCM
**Machine Learning** for **Calibration** of **Constitutive Models**

***

## Background
### Main purpose
Based on previous scientific researches<!-- (see [bibliography](#bibliography)) -->, this project aims to study Abaqus integration point data interpolation into well defined and equally spaced mesh grid points.

### Why integration point data interpolation into a structured mesh grid?
Finite element simulation data is inherently tied to integration points, which are distributed according to the mesh used in the simulation.
By other words, we can say that the obtained results are mesh dependent.
But, what if we want to know data in different points other than the ones given by the simulation mesh?
Well, interpolating integration point data into a structured mesh grid addresses this challenge!

### Interpolation and its context
Interpolation is a fundamental mathematical technique used to estimate unknown values between known data points.
In the context of material parameter prediction through machine learning (ML) using simulation data, interpolation helps create a continuous representation of discrete data obtained from finite element integration points.
This representation is essential when mapping simulation results onto a desired structured grid, enabling smoother and more precise data analysis.

In this project, Python's `scipy.interpolate` library is used, specifically the `RBFInterpolator` (Radial Basis Function Interpolator) class.
The `scipy.interpolate` library is a part of the SciPy ecosystem, which provides a collection of mathematical algorithms and convenience functions built on NumPy.
It is widely used for performing interpolation tasks, including both univariate and multivariate data interpolation, with support for regular and scattered datasets.

This choice is motivated by the library's robustness, flexibility, and the efficient implementation of its various interpolation methods in the context of this work.
`RBFInterpolator` is particularly suited for scattered data interpolation, where data points are irregularly distributed in space.
It also supports extrapolation, which is a crucial feature for this use case, as not all interpolation methods provide this capability.

Previously,`griddata` class (from the same library) was also explored, which is also part of the **Multivariate Interpolation** family.
However, `griddata` does not support extrapolation, which limited its applicability for this work, making the `RBFInterpolator` class the preferred choice.

### Choosed interpolation methods and grids

* **Linear:** A computationally efficient method that assumes a piecewise linear relationship between data points. It is fast and works well for datasets where smoothness is less critical.

* **Cubic:** Provides a smoother interpolation by using cubic radial basis functions. It balances smoothness and computational cost, making it suitable for many engineering applications.

* **Multiquadric:** Known for its global smoothness and accuracy. It introduces a radial function that grows quadratically, allowing it to handle complex datasets with non-uniform point distributions effectively.

Each of these methods has its strengths and trade-offs, and the choice depends on the specific nature of the simulation data and the desired accuracy of the interpolated results. The following sections will delve into their application and performance across different grid structures.

### Which one should I choose?
<!-- "re-interpolation" back to integration points -->
<!-- predicted vs original parameter comparison -->
<!-- global statistics and analysis -->

### Bibliography

***

## Setup

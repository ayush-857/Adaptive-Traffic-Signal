# Adaptive-Traffic-Signal

## Overview 

This is a Python-based adaptive traffic signal simulation system that dynamically allocates green signal time to each road based on weighted traffic analysis, emergency vehicle prioritization, and fairness metrics. This ensures a smarter traffic management system compared to traditional fixed-time signals.

## Features

- ML-based traffic prediction
- Adaptive green signal allocation
- Weighted vehicle density calculation
- Emergency vehicle prioritization
- Waiting time analysis
- Traffic fairness metrics
- Congestion-based traffic clearing
- Throughput tracking across cycles
- Graphical traffic visualization

## Libraries Used 

- Pandas
- NumPy
- Scikit-learn
- Matplotlib

## How the System Works

- Input traffic data is given.
- The ML model predicts future traffic based on it.
- Weighted vehicles are calculated.
- Green signal time is allocated based on different parameters.
- Waiting time and fairness metrics are evaluated.
- Traffic is cleared and updated for the next cycle.
- Graphs for different cycles are generated.

## Traffic Allocation Logic 

The system assigns different weights to different vehicle types:

- Cars → Weight = 1
- Bikes → Weight = 0.5
- Buses → Weight = 2

Roads with higher weighted density are given more green signal time. Previous waiting time is also considered to ensure fairness.

## Machine Learning Component

The project uses Linear Regression models to predict future traffic conditions.

The model is trained using simulated traffic patterns and predicts:
- Future car count
- Future bike count
- Future bus count

## Performance Metrics

The system evaluates:

- Average waiting time
- Maximum waiting time
- Waiting time variance
- Throughput (vehicles cleared)
- Improvement over fixed equal-time signals

## Visualization

The simulation generates graphs for:

- Traffic composition per road
- Green signal allocation
- Waiting time analysis
- Throughput across cycles

## Future Improvements 

Possible future extensions include:

- Real-time IoT sensor integration
- Computer vision-based traffic detection
- Real-world traffic dataset integration

## Author

Ayush

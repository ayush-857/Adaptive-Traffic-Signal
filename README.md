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


## Workflow Diagram 

<img width="1853" height="3973" alt="untitled (1)" src="https://github.com/user-attachments/assets/472abd95-aa73-47fa-b140-fa7ccdd516d3" />


## Visualization

The simulation generates graphs for:

- Traffic composition per road
- Green signal allocation
- Waiting time analysis
- Throughput across cycles

Here are the results of the graphs for the throughout for 3 different modes for 3 cycles each:

Increasing Mode






<img width="793" height="675" alt="Screenshot 2026-05-20 020907" src="https://github.com/user-attachments/assets/643a2bb4-07e8-43c2-abf9-695de50ea538" />

Stable mode







<img width="876" height="780" alt="Screenshot 2026-05-20 020448" src="https://github.com/user-attachments/assets/29e72294-efff-40d4-8568-da775c59741f" />

Decreasing mode






<img width="802" height="679" alt="Screenshot 2026-05-20 015702" src="https://github.com/user-attachments/assets/10a53ce1-7b44-4952-8fb4-d28cc8074547" />


## Detailed Results

Detailed simulation outputs and performance analysis are available in:

- [RESULTS_ANALYSIS.md](RESULTS_ANALYSIS.md)


## Future Improvements 

Possible future extensions include:

- Real-time IoT sensor integration
- Computer vision-based traffic detection
- Real-world traffic dataset integration

## Author

Ayush

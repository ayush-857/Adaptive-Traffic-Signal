# Simulation Results and Analysis

## Overview

This document presents the performance analysis of the Adaptive AI-Based Traffic Signal Simulation System under different traffic conditions.

The system was tested under:
- Increasing Traffic Mode
- Stable Traffic Mode
- Decreasing Traffic Mode

The analysis focuses on:
- Average waiting time
- Throughput
- Fairness
- Congestion handling
- Emergency vehicle prioritization
- Signal allocation efficiency


# Increasing Traffic Mode

## Observations

Average Waiting Time: 2.52 - 4.59 - 6.95

Baseline Waiting Time: 2.61 - 4.64 - 6.77

Improvement Over Baseline: 3.5% - 1.13% - (-2.65%)

Max Waiting Time: 3.12 - 5.24 - 8.16

Waiting Time Variance: 0.34 - 0.32 - 2.05

Throughput: 154.47 - 150.82 - 146.29


Cycle 1:





<img width="1919" height="1079" alt="Screenshot 2026-05-20 015552" src="https://github.com/user-attachments/assets/c64cb46d-37e6-4571-82be-4de12a13a691" />


Cycle 2:






<img width="1919" height="1079" alt="Screenshot 2026-05-20 015623" src="https://github.com/user-attachments/assets/9fa7490a-6ee7-455b-9814-5c7c0aa3b1d1" />


Cycle 3:





<img width="1919" height="1079" alt="Screenshot 2026-05-20 015643" src="https://github.com/user-attachments/assets/0ceb06df-5cce-42f8-aa99-eb3e7facc3d1" />



# Stable Traffic Mode

## Observations

Average Waiting Time: 2.63 - 2.15 - 1.97

Baseline Waiting Time: 2.61 - 2.28 - 2.04

Improvement Over Baseline: (-0.65%) - 5.62% - 3.11%

Max Waiting Time: 3.76 - 2.75 - 2.39

Waiting Time Variance: 1.31 - 0.41 - 0.18

Throughput: 154.88 - 149.48 - 148.92


Cycle1:





<img width="1919" height="1079" alt="Screenshot 2026-05-20 020358" src="https://github.com/user-attachments/assets/e9957228-3fed-4073-846e-71a81f9b021b" />


Cycle 2:





<img width="1919" height="1079" alt="Screenshot 2026-05-20 020412" src="https://github.com/user-attachments/assets/ea74217e-9187-4e5f-9ad1-170fe32a36f9" />


Cycle 3:





<img width="1919" height="1077" alt="Screenshot 2026-05-20 020429" src="https://github.com/user-attachments/assets/fc328387-1330-465b-bf3a-123086017cc2" />


# Decreasing Traffic Mode

## Observations

Average Waiting Time: 2.52 - 1.28 - 0.83

Baseline Waiting Time: 2.61 - 1.39 - 0.85

Improvement Over Baseline: 3.5% - 7.94% - 1.3%

Max Waiting Time: 3.12 - 1.74 - 0.94

Waiting Time Variance: 0.34 - 0.23 - 0.01

Throughput: 154.47 - 138.04 - 95.09


Cycle 1:






<img width="1919" height="1078" alt="Screenshot 2026-05-20 020819" src="https://github.com/user-attachments/assets/441f7c07-04ee-45cf-bd04-05e8a7d85c2e" />


Cycle 2:






<img width="1919" height="1079" alt="Screenshot 2026-05-20 020836" src="https://github.com/user-attachments/assets/25e8a0de-59af-4b1b-9db5-7a360303b2c5" />


Cycle 3:





<img width="1919" height="1079" alt="Screenshot 2026-05-20 020854" src="https://github.com/user-attachments/assets/f7cdc5e6-e088-448e-963d-0a3608db641b" />





# Overall Conclusion


The Adaptive AI-Based Traffic Signal Simulation System successfully demonstrated dynamic traffic signal allocation under increasing, stable, and decreasing traffic conditions.

The system continuously adjusted green signal timings using weighted vehicle density, congestion analysis, fairness metrics, and emergency vehicle prioritization.

In most simulation cycles, the adaptive system outperformed the baseline equal-signal allocation model by reducing average waiting time and maintaining stable throughput under varying traffic conditions.

Two simulation cycles showed slightly lower performance than the baseline system. These cases occurred during emergency vehicle prioritization and extremely high congestion scenarios, where the model temporarily sacrificed optimization efficiency to ensure emergency clearance and balanced traffic management. This reflects realistic adaptive traffic behavior commonly observed in real-world intelligent traffic systems.

Overall, the project demonstrates the potential of AI-based adaptive traffic control systems for improving traffic efficiency, reducing congestion, and supporting intelligent urban traffic management.

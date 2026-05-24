# Mathematical Formulas Used

## 1. Weighted Vehicle Density Formula

Weighted Vehicles =  
(Cars × 1) + (Bikes × 0.5) + (Buses × 2)

### Explanation
- Cars weight = 1
- Bikes weight = 0.5
- Buses weight = 2

This converts different vehicle types into a unified traffic load value.

---

## 2. Traffic Density Formula

Density =  
Weighted Vehicles / Total Weighted Vehicles

### Explanation
This calculates the traffic share of each road relative to the total junction traffic.

---

## 3. Adaptive Green Signal Allocation Formula

Green Signal Time =  
Minimum Time + (Density × Remaining Cycle Time)

Where,

Remaining Cycle Time =  
Cycle Time − (Minimum Time × Number of Roads)

### Explanation
- Every road receives a guaranteed minimum signal time.
- Remaining time is distributed dynamically based on traffic density.

---

## 4. Fairness-Based Waiting Time Adjustment

Adjusted Green Time =  
Green Time + (Previous Waiting Time × 0.1)

### Explanation
Roads with higher waiting time in previous cycles gradually receive more priority.

---

## 5. Emergency Vehicle Priority Formula

Emergency Green Time =  
Green Time × 1.5

### Explanation
Roads containing emergency vehicles receive boosted signal duration.

---

## 6. Waiting Time Formula

Waiting Time =  
Weighted Vehicles / Green Signal Time

### Explanation
Higher traffic with lower signal time results in larger waiting time.

---

## 7. Baseline Equal Signal Formula

Equal Signal Time =  
Cycle Time / Number of Roads

Baseline Waiting =  
Weighted Vehicles / Equal Signal Time

### Explanation
Represents traditional traffic systems where all roads receive equal signal time.

---

## 8. Improvement Percentage Formula

Improvement (%) =  
((Baseline Waiting − Average Waiting Time) / Baseline Waiting) × 100

### Explanation
Measures performance improvement over traditional equal-time systems.

---

## 9. Congestion Factor Formula

Congestion Factor =  
Weighted Vehicles / Maximum Weighted Vehicles

### Explanation
Used to estimate congestion severity for each road.

---

## 10. Dynamic Vehicle Clearance Formula

### Cars Cleared

Cars Cleared =  
Green Time × (0.4 + 0.2 × (1 − Congestion Factor))

### Bikes Cleared

Bikes Cleared =  
Green Time × (0.6 + 0.2 × (1 − Congestion Factor))

### Buses Cleared

Buses Cleared =  
Green Time × (0.15 + 0.1 × (1 − Congestion Factor))

### Explanation
Vehicle clearance rate dynamically changes according to congestion level.

---

## 11. Throughput Formula

Throughput =  
Σ (Cars Cleared + Bikes Cleared + Buses Cleared)

### Explanation
Measures total vehicles cleared during a cycle.

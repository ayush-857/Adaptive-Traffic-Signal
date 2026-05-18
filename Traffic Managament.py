import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

np.random.seed(42)

traffic_data = {
    "Road": ["Road A", "Road B", "Road C", "Road D"],
    "Cars": [60, 50, 30, 20],
    "Bikes": [60, 50, 40, 25],
    "Buses": [13, 10, 5, 5]
}

def get_user_settings():
    mode = input('What is the traffic mode (Stable, Increasing, Decreasing)? ') .lower()
    if mode not in ["stable", "increasing", "decreasing"]:
        mode = "stable"

    try:
        num_cycles = int(input("Enter number of cycles: "))

        if num_cycles <= 0:
            num_cycles = 3

    except ValueError:
        num_cycles = 3
    return mode, num_cycles

def generate_training_data(mode):
    X = []
    y_cars = []
    y_bikes = []
    y_buses = []

    for i in range(50):
        cars = np.random.randint(20, 100)
        bikes = np.random.randint(30, 120)
        buses = np.random.randint(5, 20)

        if mode == "increasing":
            next_cars = cars + np.random.randint(15, 30)
            next_bikes = bikes + np.random.randint(20, 40)
            next_buses = buses + np.random.randint(3, 8)

        elif mode == "decreasing":
            next_cars = max(0, cars - np.random.randint(5, 15))
            next_bikes = max(0, bikes - np.random.randint(5, 20))
            next_buses = max(0, buses - np.random.randint(1, 5))

        else:
            next_cars = max(0, cars + np.random.randint(-10, 10))
            next_bikes = max(0, bikes + np.random.randint(-15, 15))
            next_buses = max(0, buses + np.random.randint(-3, 3))

        X.append([cars, bikes, buses])
        y_cars.append(next_cars)
        y_bikes.append(next_bikes)
        y_buses.append(next_buses)
    return X, y_cars, y_bikes, y_buses

def train_models(X, y_cars, y_bikes, y_buses):
    model_cars = LinearRegression().fit(X, y_cars)
    model_bikes = LinearRegression().fit(X, y_bikes)
    model_buses = LinearRegression().fit(X, y_buses)

    return model_cars, model_bikes, model_buses

def create_dataframe(traffic_data):

    df = pd.DataFrame(traffic_data)

    return df

def assign_emergencies(df):

    df["Emergency"] = np.random.choice(
        [0, 1],
        size=len(df),
        p=[0.9, 0.1]
    )

    return df

def calculate_weighted_vehicles(df):

    weight_car = 1
    weight_bike = 0.5
    weight_bus = 2

    df["Weighted Vehicles"] = (
        df["Cars"] * weight_car +
        df["Bikes"] * weight_bike +
        df["Buses"] * weight_bus
    )

    return df

def allocate_green_signals(df, prev_waiting_time):

    total_vehicles = df["Weighted Vehicles"].sum()

    number_of_roads = len(df)

    min_time = 15
    max_time = 60
    cycle_time = 120

    remaining_time = cycle_time - (min_time * number_of_roads)

    df["Density"] = df["Weighted Vehicles"] / total_vehicles

    df["Green Signal (sec)"] = (
        min_time +
        (df["Density"] * remaining_time)
    )

    df["Green Signal (sec)"] = df[
        "Green Signal (sec)"
    ].clip(upper=max_time)

    if prev_waiting_time is not None:

        df["Green Signal (sec)"] += (
            prev_waiting_time.values * 0.1
        )

        df["Green Signal (sec)"] = df[
            "Green Signal (sec)"
        ].clip(upper=max_time)

    df.loc[
        df["Emergency"] == 1,
        "Green Signal (sec)"
    ] *= 1.5

    df["Green Signal (sec)"] = df[
        "Green Signal (sec)"
    ].clip(upper=max_time)

    total_allocated = df["Green Signal (sec)"].sum()

    time_diff = cycle_time - total_allocated

    if time_diff > 0:

        eligible = df["Green Signal (sec)"] < max_time

        eligible_density_sum = df.loc[
            eligible,
            "Density"
        ].sum()

        if eligible_density_sum > 0:

            df.loc[
                eligible,
                "Green Signal (sec)"
            ] += (
                df.loc[eligible, "Density"]
                / eligible_density_sum
            ) * time_diff

    total_allocated = df["Green Signal (sec)"].sum()

    if total_allocated > cycle_time:

        df["Green Signal (sec)"] *= (
            cycle_time / total_allocated
        )

    return df

def calculate_metrics(df, cycle_time):

    df["Waiting Time"] = (
        df["Weighted Vehicles"]
        / df["Green Signal (sec)"]
    )

    avg_waiting_time = df["Waiting Time"].mean()

    max_waiting_time = df["Waiting Time"].max()

    fairness_variance = df["Waiting Time"].var()

    number_of_roads = len(df)

    equal_time = cycle_time / number_of_roads

    baseline_waiting = (
        df["Weighted Vehicles"] / equal_time
    ).mean()

    improvement = (
        (baseline_waiting - avg_waiting_time)
        / baseline_waiting
    ) * 100

    return (
        df,
        avg_waiting_time,
        max_waiting_time,
        fairness_variance,
        baseline_waiting,
        improvement
    )

def clear_traffic(df):

    congestion_factor = (
        df["Weighted Vehicles"]
        / df["Weighted Vehicles"].max()
    )

    cars_cleared = (
        df["Green Signal (sec)"]
        * (0.4 + 0.2 * (1 - congestion_factor))
    )

    bikes_cleared = (
        df["Green Signal (sec)"]
        * (0.6 + 0.2 * (1 - congestion_factor))
    )

    buses_cleared = (
        df["Green Signal (sec)"]
        * (0.15 + 0.1 * (1 - congestion_factor))
    )

    cars_cleared = np.minimum(
        cars_cleared,
        df["Cars"]
    )

    bikes_cleared = np.minimum(
        bikes_cleared,
        df["Bikes"]
    )

    buses_cleared = np.minimum(
        buses_cleared,
        df["Buses"]
    )

    df["Cars"] = df["Cars"] - cars_cleared
    df["Bikes"] = df["Bikes"] - bikes_cleared
    df["Buses"] = df["Buses"] - buses_cleared

    df["Cars"] = df["Cars"].clip(lower=0)
    df["Bikes"] = df["Bikes"].clip(lower=0)
    df["Buses"] = df["Buses"].clip(lower=0)

    throughput = (
        cars_cleared
        + bikes_cleared
        + buses_cleared
    ).sum()

    return df, throughput

def predict_next_traffic(
    df,
    model_cars,
    model_bikes,
    model_buses
):

    old_cars = df["Cars"].copy()
    old_bikes = df["Bikes"].copy()
    old_buses = df["Buses"].copy()

    features = df[["Cars", "Bikes", "Buses"]].values

    max_growth = 30
    max_drop = 20

    predicted_cars = model_cars.predict(features)
    predicted_bikes = model_bikes.predict(features)
    predicted_buses = model_buses.predict(features)

    df["Cars"] = np.clip(
        predicted_cars,
        old_cars - max_drop,
        old_cars + max_growth
    )

    df["Bikes"] = np.clip(
        predicted_bikes,
        old_bikes - max_drop,
        old_bikes + max_growth
    )

    df["Buses"] = np.clip(
        predicted_buses,
        old_buses - 10,
        old_buses + 15
    )

    df["Cars"] = np.round(df["Cars"])
    df["Bikes"] = np.round(df["Bikes"])
    df["Buses"] = np.round(df["Buses"])

    df["Cars"] = df["Cars"].clip(lower=0)
    df["Bikes"] = df["Bikes"].clip(lower=0)
    df["Buses"] = df["Buses"].clip(lower=0)

    return df

def add_new_traffic(df, mode):

    if mode == "increasing":

        new_cars = np.random.randint(15, 30, size=len(df))
        new_bikes = np.random.randint(20, 40, size=len(df))
        new_buses = np.random.randint(3, 8, size=len(df))

    elif mode == "decreasing":

        new_cars = np.random.randint(5, 15, size=len(df))
        new_bikes = np.random.randint(5, 15, size=len(df))
        new_buses = np.random.randint(1, 4, size=len(df))

    else:

        new_cars = np.random.randint(10, 20, size=len(df))
        new_bikes = np.random.randint(10, 25, size=len(df))
        new_buses = np.random.randint(2, 6, size=len(df))

    df["Cars"] += new_cars
    df["Bikes"] += new_bikes
    df["Buses"] += new_buses

    return df

def plot_cycle(df):

    plt.figure()

    plt.bar(
        df["Road"],
        df["Cars"],
        label="Cars"
    )

    plt.bar(
        df["Road"],
        df["Bikes"],
        bottom=df["Cars"],
        label="Bikes"
    )

    plt.bar(
        df["Road"],
        df["Buses"],
        bottom=df["Cars"] + df["Bikes"],
        label="Buses"
    )

    plt.xlabel("Road")
    plt.ylabel("Number of Vehicles")
    plt.title("Traffic Composition per Road")

    plt.legend()

    plt.figure()

    plt.bar(
        df["Road"],
        df["Green Signal (sec)"]
    )

    plt.xlabel("Road")
    plt.ylabel("Green Time (seconds)")
    plt.title("Green Signal Allocation per Road")

    plt.figure()

    plt.bar(
        df["Road"],
        df["Waiting Time"]
    )

    plt.xlabel("Road")
    plt.ylabel("Waiting Time")
    plt.title("Waiting Time per Road")

    plt.grid(
        True,
        linestyle="--",
        alpha=0.4
    )

    plt.show()

def plot_throughput(throughput_history):

    plt.figure()

    plt.plot(
        range(1, len(throughput_history) + 1),
        throughput_history,
        marker='o'
    )

    plt.xlabel("Cycle")
    plt.ylabel("Vehicles Cleared")

    plt.title("Throughput Across Cycles")

    plt.grid(
        True,
        linestyle="--",
        alpha=0.4
    )

    plt.show()


def display_cycle_summary(
    cycle,
    df,
    avg_waiting_time,
    max_waiting_time,
    fairness_variance,
    baseline_waiting,
    improvement,
    throughput
):

    print(f"\n--- Cycle {cycle} ---\n")

    total_vehicles = df["Weighted Vehicles"].sum()

    print(
        "Total Vehicles at Junction:",
        round(total_vehicles, 2)
    )

    print()

    print("Smart Traffic Signal Allocation\n")

    for index, row in df.iterrows():

        print(row["Road"])

        print(
            "Weighted Vehicles:",
            round(row["Weighted Vehicles"], 2)
        )

        print(
            "Green Signal:",
            round(row["Green Signal (sec)"], 2),
            "seconds"
        )

        print(
            "Emergency:",
            "YES 🚑"
            if row["Emergency"] == 1
            else "No"
        )

        print()

    print(
        "Total Allocated Time:",
        round(df["Green Signal (sec)"].sum(), 2)
    )

    print(
        "Average Waiting Time:",
        round(avg_waiting_time, 2)
    )

    print(
        "Baseline Avg Waiting Time (Equal Signals):",
        round(baseline_waiting, 2)
    )

    print(
        "Improvement over baseline:",
        round(improvement, 2),
        "%"
    )

    print(
        "Max Waiting Time:",
        round(max_waiting_time, 2)
    )

    print(
        "Waiting Time Variance:",
        round(fairness_variance, 2)
    )

    print(
        "Throughput (vehicles cleared):",
        round(throughput, 2)
    )



def main():

    mode, num_cycles = get_user_settings()

    X, y_cars, y_bikes, y_buses = generate_training_data(mode)

    model_cars, model_bikes, model_buses = train_models(
        X,
        y_cars,
        y_bikes,
        y_buses
    )

    prev_waiting_time = None

    throughput_history = []

    current_traffic_data = traffic_data.copy()

    for cycle in range(1, num_cycles + 1):
        print(f"\n--- Cycle {cycle} ---\n")

        df = create_dataframe(current_traffic_data)

        df = assign_emergencies(df)

        df = calculate_weighted_vehicles(df)

        df = allocate_green_signals(
            df,
            prev_waiting_time
        )

        cycle_time = 120

        (
            df,
            avg_waiting_time,
            max_waiting_time,
            fairness_variance,
            baseline_waiting,
            improvement
        ) = calculate_metrics(
            df,
            cycle_time
        )

        prev_waiting_time = df["Waiting Time"]

        df, throughput = clear_traffic(df)

        throughput_history.append(throughput)

        df = predict_next_traffic(
            df,
            model_cars,
            model_bikes,
            model_buses
        )

        df = add_new_traffic(df, mode)

        current_traffic_data = df[
            ["Road", "Cars", "Bikes", "Buses"]
        ].to_dict(orient="list")

        display_cycle_summary(
            cycle,
            df,
            avg_waiting_time,
            max_waiting_time,
            fairness_variance,
            baseline_waiting,
            improvement,
            throughput
        )


        plot_cycle(df)

    plot_throughput(throughput_history)


if __name__ == "__main__":
    main()
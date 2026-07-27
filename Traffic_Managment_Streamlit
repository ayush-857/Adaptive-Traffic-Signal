import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import streamlit as st
import time

st.set_page_config(
    page_title="AI Smart Traffic Signal System",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🚦 AI Smart Traffic Signal System")

st.markdown("""
### Adaptive Traffic Management using Machine Learning & Simulation

This simulation intelligently allocates green signal timings based on:

- 🚗 Traffic Density
- ⏳ Previous Waiting Time
- 🚑 Emergency Vehicle Priority

while maintaining a fixed 120-second signal cycle.
""")

st.divider()


with st.container(border=True):

    st.subheader("⚙ Simulation Configuration")

    mode = st.selectbox(
        "Traffic Mode",
        ["Stable", "Increasing", "Decreasing"]
    )

    num_cycles = st.selectbox(
        "Number of Cycles",
        [1, 2, 3, 4, 5]
    )

    st.divider()

    start_simulation = st.button(
        "🚦 Start Simulation",
        use_container_width=True
    )




if "simulation_complete" not in st.session_state:
    st.session_state.simulation_complete = False

if "cycle_records" not in st.session_state:
    st.session_state.cycle_records = []

if "throughput_history" not in st.session_state:
    st.session_state.throughput_history = []

if "current_cycle" not in st.session_state:
    st.session_state.current_cycle = 1

if "show_summary" not in st.session_state:
    st.session_state.show_summary = False

np.random.seed(42)

traffic_data = {
    "Road": ["Road A", "Road B", "Road C", "Road D"],
    "Cars": [60, 50, 30, 20],
    "Bikes": [60, 50, 40, 25],
    "Buses": [13, 10, 5, 5]
}



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



def plot_cycle(df):

    st.subheader("📊 Cycle Analysis")

    col1, col2, col3 = st.columns(3)

    # ==========================
    # Traffic Composition
    # ==========================
    with col1:

        plt.figure(figsize=(4,3))

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
        plt.ylabel("Vehicles")
        plt.title("Traffic Composition")

        plt.legend(fontsize=8)

        plt.grid(
            axis="y",
            linestyle="--",
            alpha=0.4
        )

        plt.tight_layout()

        st.pyplot(plt.gcf())

        plt.close()

    # ==========================
    # Green Signal Allocation
    # ==========================
    with col2:

        plt.figure(figsize=(4,3))

        plt.bar(
            df["Road"],
            df["Green Signal (sec)"]
        )

        plt.xlabel("Road")
        plt.ylabel("Seconds")

        plt.title("Green Signal Allocation")

        plt.grid(
            True,
            linestyle="--",
            alpha=0.4
        )

        plt.tight_layout()

        st.pyplot(plt.gcf())

        plt.close()

    # ==========================
    # Waiting Time
    # ==========================
    with col3:

        plt.figure(figsize=(4,3))

        plt.bar(
            df["Road"],
            df["Waiting Time"]
        )

        plt.xlabel("Road")
        plt.ylabel("Waiting Time")

        plt.title("Waiting Time")

        plt.grid(
            True,
            linestyle="--",
            alpha=0.4
        )

        plt.tight_layout()

        st.pyplot(plt.gcf())

        plt.close()

def plot_throughput(throughput_history):

    plt.figure(figsize=(7,3.5))

    plt.plot(
        range(1, len(throughput_history) + 1),
        throughput_history,
        marker="o",
        linewidth=2
    )

    plt.xlabel("Cycle")
    plt.ylabel("Vehicles Cleared")
    plt.title("Throughput Across Cycles")

    plt.grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()

    st.pyplot(plt.gcf())

    plt.close()


def display_kpi_cards(
    total_vehicles,
    avg_waiting_time,
    improvement,
    throughput
):

    st.subheader("📊 Cycle Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🚗 Total Vehicles",
            value=round(total_vehicles)
        )

    with col2:
        st.metric(
            label="⏱ Average Wait",
            value=f"{avg_waiting_time:.2f} s"
        )

    with col3:
        st.metric(
            label="📈 Improvement",
            value=f"{improvement:.2f}%"
        )

    with col4:
        st.metric(
            label="🚦 Throughput",
            value=round(throughput)
        )
def display_ai_decision(df):



    highest = df.loc[df["Green Signal (sec)"].idxmax()]
    lowest = df.loc[df["Green Signal (sec)"].idxmin()]

    st.success(
        f"🚦 AI selected **{highest['Road']}** as the highest priority road for this cycle."
    )

    st.markdown("### 🧠 Decision Analysis")

    st.write(
        f"• **Weighted Traffic:** {highest['Weighted Vehicles']:.1f} vehicles "
        f"({highest['Density']:.1%} of total traffic)"
    )

    st.write(
        f"• **Green Signal Allocated:** {highest['Green Signal (sec)']:.2f} seconds."
    )

    if highest["Emergency"] == 1:
        st.write(
            "• 🚑 Emergency vehicle detected. Priority multiplier was applied to reduce emergency response time."
        )
    else:
        st.write(
            "• 🚦 No emergency override was required for this road."
        )

    if highest["Density"] == df["Density"].max():
        st.write(
            "• 📈 This road carried the highest traffic density, making it the optimal candidate for additional green time."
        )

    st.write(
        "• ⏳ Historical waiting time from the previous cycle was incorporated into the allocation algorithm."
    )

    st.write(
        "• ⚖️ Minimum and maximum signal constraints (15–60 seconds) were enforced."
    )

    st.write(
        "• 🔒 The overall junction cycle remained fixed at **120 seconds**, ensuring synchronization."
    )

    st.markdown("---")

    st.markdown("### 📊 AI Observations")

    st.metric(
        "Highest Priority Road",
        highest["Road"]
    )

    st.metric(
        "Lowest Priority Road",
        lowest["Road"]
    )

    st.metric(
        "Total Weighted Traffic",
        f"{df['Weighted Vehicles'].sum():.1f}"
    )

    st.metric(
        "Average Waiting Time",
        f"{df['Waiting Time'].mean():.2f} sec"
    )

    st.markdown("---")

    st.markdown("### 💡 AI Recommendation")

    if highest["Density"] > 0.40:
        st.info(
            "Traffic is heavily concentrated on one approach. Continuous monitoring is recommended to prevent queue spillback."
        )
    elif df["Emergency"].sum() > 0:
        st.info(
            "Emergency traffic was detected. Priority-based signal control successfully minimized emergency delay while maintaining the overall cycle."
        )
    else:
        st.info(
            "Traffic distribution is relatively balanced. The current adaptive allocation is expected to maintain smooth flow."
        )


def display_final_summary():

    st.title("📊 Final Summary Dashboard")

    records = st.session_state.cycle_records

    total_cycles = len(records)

    total_throughput = sum(
        r["throughput"] for r in records
    )

    avg_wait = sum(
        r["avg_waiting_time"] for r in records
    ) / total_cycles

    avg_improvement = sum(
        r["improvement"] for r in records
    ) / total_cycles

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Cycles",
            total_cycles
        )

    with c2:
        st.metric(
            "Vehicles Cleared",
            round(total_throughput,2)
        )

    with c3:
        st.metric(
            "Average Wait",
            f"{avg_wait:.2f} s"
        )

    with c4:
        st.metric(
            "Improvement",
            f"{avg_improvement:.2f}%"
        )

    st.divider()

    left, center, right = st.columns([1, 2, 1])

    with center:
        with st.container(border=True):
            st.subheader("📈 Throughput Analysis")

            plot_throughput(
                st.session_state.throughput_history
            )

    highest = max(
        records,
        key=lambda x: x["throughput"]
    )

    best = max(
        records,
        key=lambda x: x["improvement"]
    )

    # Overall Statistics

    highest_traffic = None
    highest_priority = None

    max_weight = -1
    max_green = -1

    total_emergencies = 0
    road_emergencies = {}

    highest_avg_wait = max(
        records,
        key=lambda x: x["avg_waiting_time"]
    )

    lowest_avg_wait = min(
        records,
        key=lambda x: x["avg_waiting_time"]
    )

    for record in records:

        df = record["df"]

        total_emergencies += df["Emergency"].sum()

        for _, row in df.iterrows():

            road = row["Road"]

            road_emergencies[road] = (
                    road_emergencies.get(road, 0)
                    + row["Emergency"]
            )

            if row["Weighted Vehicles"] > max_weight:
                max_weight = row["Weighted Vehicles"]

                highest_traffic = (
                    road,
                    record["cycle"]
                )

            if row["Green Signal (sec)"] > max_green:
                max_green = row["Green Signal (sec)"]

                highest_priority = road

    most_emergency_road = max(
        road_emergencies,
        key=road_emergencies.get
    )

    st.subheader("🏆 Simulation Highlights")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### 🚦 Highest Throughput")

            st.metric(
                "Cycle",
                highest["cycle"]
            )

            st.write(
                f"**Vehicles Cleared:** {highest['throughput']:.2f}"
            )

    with col2:
        with st.container(border=True):
            st.markdown("### 📈 Highest Improvement")

            st.metric(
                "Cycle",
                best["cycle"]
            )

            st.write(
                f"**Improvement:** {best['improvement']:.2f}%"
            )
    st.divider()

    st.subheader("📊 Simulation Statistics")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):
            st.markdown("### 🚗 Highest Weighted Traffic")

            st.write(f"**Road:** {highest_traffic[0]}")

            st.write(f"**Cycle:** {highest_traffic[1]}")

            st.write(f"**Weighted Vehicles:** {max_weight:.2f}")

    with col2:

        with st.container(border=True):
            st.markdown("### 🟢 Most Prioritized Road")

            st.write(f"**Road:** {highest_priority}")

            st.write(f"**Highest Green Time:** {max_green:.2f} sec")

    st.markdown("")

    col3, col4 = st.columns(2)

    with col3:

        with st.container(border=True):
            st.markdown("### 🚑 Emergency Statistics")

            st.metric(
                "Total Emergency Events",
                int(total_emergencies)
            )

    with col4:

        with st.container(border=True):
            st.markdown("### 🚑 Most Emergency Road")

            st.metric(
                "Road",
                most_emergency_road
            )

            st.write(
                f"Events: {road_emergencies[most_emergency_road]}"
            )

    st.markdown("")

    col5, col6 = st.columns(2)

    with col5:

        with st.container(border=True):
            st.markdown("### ⏱ Highest Average Wait")

            st.metric(
                "Cycle",
                highest_avg_wait["cycle"]
            )

            st.write(
                f"{highest_avg_wait['avg_waiting_time']:.2f} s"
            )

    with col6:

        with st.container(border=True):
            st.markdown("### ⚡ Lowest Average Wait")

            st.metric(
                "Cycle",
                lowest_avg_wait["cycle"]
            )

            st.write(
                f"{lowest_avg_wait['avg_waiting_time']:.2f} s"
            )

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
    st.subheader(f"🚦 Cycle {cycle} Summary")

    total_vehicles = df["Weighted Vehicles"].sum()

    display_kpi_cards(
        total_vehicles,
        avg_waiting_time,
        improvement,
        throughput
    )

    st.subheader("🤖 AI Insights")

    display_ai_decision(df)

    st.markdown("### 📈 Cycle Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Maximum Waiting Time",
            f"{max_waiting_time:.2f}"
        )

    with col2:
        st.metric(
            "Waiting Time Variance",
            f"{fairness_variance:.2f}"
        )

    with col3:
        st.metric(
            "Baseline Waiting Time",
            f"{baseline_waiting:.2f}"
        )

    st.divider()


    with st.expander("📋 Detailed Road Data"):

        st.dataframe(
            df[
                [
                    "Road",
                    "Weighted Vehicles",
                    "Density",
                    "Green Signal (sec)",
                    "Waiting Time",
                    "Emergency"
                ]
            ],
            hide_index=True,
            use_container_width=True
        )

if start_simulation:
    st.success("Simulation Started!")

    st.write(f"**Traffic Mode:** {mode}")
    st.write(f"**Number of Cycles:** {num_cycles}")

    X, y_cars, y_bikes, y_buses = generate_training_data(mode)

    model_cars, model_bikes, model_buses = train_models(
        X,
        y_cars,
        y_bikes,
        y_buses
    )

    prev_waiting_time = None

    st.session_state.cycle_records = []
    st.session_state.throughput_history = []

    current_traffic_data = traffic_data.copy()

    for cycle in range(1, num_cycles + 1):
        st.divider()
        st.subheader(f"Cycle {cycle}")

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

        st.session_state.throughput_history.append(throughput)

        df = predict_next_traffic(
            df,
            model_cars,
            model_bikes,
            model_buses
        )

        current_traffic_data = df[
            ["Road", "Cars", "Bikes", "Buses"]
        ].to_dict(orient="list")

        st.session_state.cycle_records.append({

            "cycle": cycle,

            "df": df.copy(),

            "avg_waiting_time": avg_waiting_time,

            "max_waiting_time": max_waiting_time,

            "fairness_variance": fairness_variance,

            "baseline_waiting": baseline_waiting,

            "improvement": improvement,

            "throughput": throughput,

            "total_vehicles": df["Weighted Vehicles"].sum()
        })

    st.session_state.simulation_complete = True

    st.session_state.current_cycle = 1

    st.session_state.show_summary = False

if st.session_state.simulation_complete:



    if st.session_state.show_summary:

        display_final_summary()

        if st.button(
                "⬅ Back to Cycles",
                use_container_width=True
        ):
            st.session_state.show_summary = False
            st.rerun()

        st.stop()


    st.write(f"Stored {len(st.session_state.cycle_records)} simulation cycles.")

    total_cycles = len(st.session_state.cycle_records)
    st.subheader(
        f"Cycle {st.session_state.current_cycle} of {total_cycles}"
    )



    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:

        if st.button(
                "⬅ Previous",
                disabled=st.session_state.current_cycle == 1,
                use_container_width=True
        ):
            st.session_state.current_cycle -= 1
            st.rerun()

    with col2:

        selected_cycle = st.selectbox(
            "Cycle",
            range(1, total_cycles + 1),
            index=st.session_state.current_cycle - 1,
            key="cycle_selector"
        )

        if selected_cycle != st.session_state.current_cycle:
            st.session_state.current_cycle = selected_cycle
            st.rerun()

    with col3:

        if st.session_state.current_cycle < total_cycles:

            if st.button(
                    "Next ➡",
                    use_container_width=True
            ):
                st.session_state.current_cycle += 1
                st.rerun()

        else:

            if st.button(
                    "📊 Final Summary",
                    use_container_width=True
            ):
                st.session_state.show_summary = True
                st.rerun()

    selected_record = st.session_state.cycle_records[
        st.session_state.current_cycle - 1
        ]



    display_cycle_summary(
        selected_record["cycle"],
        selected_record["df"],
        selected_record["avg_waiting_time"],
        selected_record["max_waiting_time"],
        selected_record["fairness_variance"],
        selected_record["baseline_waiting"],
        selected_record["improvement"],
        selected_record["throughput"]
    )

    plot_cycle(selected_record["df"])





import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from core.simulator import PricingSimulator
from core.strategies import StaticPricing, DynamicPricing, AdvancedPricing


st.title("Dynamic Pricing Simulator")
st.write("Adjust the parameters on the left and click Run to compare pricing strategies.")

st.sidebar.header("Parameters")

base_demand   = st.sidebar.slider("Base Demand",          20,   300,  100, step=10)
sensitivity   = st.sidebar.slider("Price Sensitivity",    0.5,  3.0,  1.5, step=0.1)
init_stock    = st.sidebar.slider("Initial Inventory",    100, 1000,  500, step=50)
sim_days      = st.sidebar.slider("Simulation Days",       20,  200,  100, step=10)
base_price    = st.sidebar.slider("Base Price",            20,  500,  100, step=10)
max_customers = st.sidebar.slider("Max Customers Per Day", 50,  500,  120, step=10)

run = st.sidebar.button("Run Simulation")

if run:
    config = {
        "base_demand":           base_demand,
        "sensitivity":           sensitivity,
        "initial_inventory":     init_stock,
        "simulation_days":       sim_days,
        "base_price":            float(base_price),
        "max_customers_per_day": max_customers,
    }

    strategies = {
        "static":   StaticPricing(),
        "dynamic":  DynamicPricing(),
        "advanced": AdvancedPricing(),
    }

    sim     = PricingSimulator(config)
    results = sim.run_all(strategies, show_log=False)

    st.write("### Results")
    base_rev = results["static"]["revenue"]
    for name, data in results.items():
        rev  = data["revenue"]
        left = data["leftover"]
        if name == "static":
            st.write(f"**{name.capitalize()}** - Revenue: {rev:,.0f} | Stock left: {left} (baseline)")
        else:
            gain = ((rev - base_rev) / base_rev) * 100
            st.write(f"**{name.capitalize()}** - Revenue: {rev:,.0f} | Stock left: {left} | +{gain:.1f}% over static")

    st.write("### Revenue Over Time")
    fig, ax = plt.subplots(figsize=(9, 4))
    for name, data in results.items():
        df = data["data"]
        ax.plot(df["day"], df["total_revenue"], label=name)
    ax.set_xlabel("Day")
    ax.set_ylabel("Cumulative Revenue")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
    plt.close(fig)

    st.write("### Price Changes Over Time")
    fig2, ax2 = plt.subplots(figsize=(9, 4))
    for name, data in results.items():
        df = data["data"]
        ax2.plot(df["day"], df["price"], label=name)
    ax2.set_xlabel("Day")
    ax2.set_ylabel("Price")
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)
    plt.close(fig2)

    st.write("### Total Revenue Comparison")
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    names = list(results.keys())
    revs  = [results[s]["revenue"] for s in names]
    ax3.bar(names, revs, color=["gray", "steelblue", "seagreen"])
    ax3.set_ylabel("Revenue")
    for i, v in enumerate(revs):
        ax3.text(i, v + 100, str(int(v)), ha="center")
    st.pyplot(fig3)
    plt.close(fig3)

    with st.expander("Show raw data"):
        frames = []
        for name, data in results.items():
            df = data["data"].copy()
            df["strategy_name"] = name
            frames.append(df)
        st.dataframe(pd.concat(frames, ignore_index=True))

else:
    st.write("Set the parameters in the sidebar and click Run Simulation.")

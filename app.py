import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from core.simulator import PricingSimulator
from core.strategies import StaticPricing, DynamicPricing, AdvancedPricing

st.title("Dynamic Pricing Simulator - My Project")
st.write("Play with the parameters on the left and see what happens.")

# make a sidebar
st.sidebar.header("Parameters Config")

b_demand = st.sidebar.slider("Base Demand", 20, 300, 100, step=10)
sens = st.sidebar.slider("Price Sensitivity", 0.5, 3.0, 1.5, step=0.1)
i_stock = st.sidebar.slider("Initial Inventory", 100, 1000, 500, step=50)
s_days = st.sidebar.slider("Simulation Days", 20, 200, 100, step=10)
b_price = st.sidebar.slider("Base Price", 20, 500, 100, step=10)
mx_cust = st.sidebar.slider("Max Customers Per Day", 50, 500, 120, step=10)

click = st.sidebar.button("Run The Simulation")

if click == True:
    my_config_dict = {
        "base_demand": b_demand,
        "sensitivity": sens,
        "initial_inventory": i_stock,
        "simulation_days": s_days,
        "base_price": float(b_price),
        "max_customers_per_day": mx_cust,
    }

    # setup strategies
    my_strats = {}
    my_strats["static"] = StaticPricing()
    my_strats["dynamic"] = DynamicPricing()
    my_strats["advanced"] = AdvancedPricing()

    my_sim = PricingSimulator(my_config_dict)
    all_res_dict = my_sim.run_all(my_strats, show_print=False)

    st.write("### Simulation Results")
    
    # get base revenue to compare with others
    base_revenue = all_res_dict["static"]["revenue"]
    
    for s_name in all_res_dict:
        s_data = all_res_dict[s_name]
        the_rev = s_data["revenue"]
        the_leftover = s_data["leftover"]
        
        if s_name == "static":
            st.write("**Static (Baseline)** - Revenue: $" + str(int(the_rev)) + " | Stock left: " + str(the_leftover))
        else:
            # calculate gain
            gain_math = ((the_rev - base_revenue) / base_revenue) * 100
            rounded_gain = round(gain_math, 1)
            st.write("**" + s_name.capitalize() + "** - Revenue: $" + str(int(the_rev)) + " | Stock left: " + str(the_leftover) + " | +" + str(rounded_gain) + "% gain")

    st.write("### Graph: Revenue Over Time")
    fig1, my_ax1 = plt.subplots(figsize=(9, 4))
    for s_name in all_res_dict:
        df1 = all_res_dict[s_name]["data"]
        my_ax1.plot(df1["day"], df1["total_revenue"], label=s_name)
    my_ax1.set_xlabel("Days")
    my_ax1.set_ylabel("Revenue so far")
    my_ax1.legend()
    my_ax1.grid(True)
    st.pyplot(fig1)
    
    # need to close plot so it doesnt build up memory
    plt.close(fig1)

    st.write("### Graph: Price Changes")
    fig2, my_ax2 = plt.subplots(figsize=(9, 4))
    for s_name in all_res_dict:
        df2 = all_res_dict[s_name]["data"]
        my_ax2.plot(df2["day"], df2["price"], label=s_name)
    my_ax2.set_xlabel("Days")
    my_ax2.set_ylabel("Current Price")
    my_ax2.legend()
    my_ax2.grid(True)
    st.pyplot(fig2)
    plt.close(fig2)

    st.write("### Graph: Total Revenue")
    fig3, my_ax3 = plt.subplots(figsize=(6, 4))
    
    # lists for bar chart
    x_list = []
    y_list = []
    for s_name in all_res_dict:
        x_list.append(s_name)
        y_list.append(all_res_dict[s_name]["revenue"])
        
    my_ax3.bar(x_list, y_list, color=["grey", "blue", "green"])
    my_ax3.set_ylabel("Total Revenue")
    
    # put the number on top of the bar
    for counter in range(len(y_list)):
        val = y_list[counter]
        my_ax3.text(counter, val + 100, str(int(val)), ha="center")
        
    st.pyplot(fig3)
    plt.close(fig3)

    # raw data section
    with st.expander("Click here to see raw pandas data"):
        df_list = []
        for s_name in all_res_dict:
            # make a copy so we don't mess up original
            temp_df = all_res_dict[s_name]["data"].copy()
            temp_df["strategy_name"] = s_name
            df_list.append(temp_df)
            
        final_table = pd.concat(df_list, ignore_index=True)
        st.dataframe(final_table)

else:
    st.write("Change the parameters if you want and then click Run.")

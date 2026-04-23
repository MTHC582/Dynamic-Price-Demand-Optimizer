import matplotlib.pyplot as plt
import pandas as pd
import os


# analyzes the simulation results and makes plots
class SimulationAnalyzer:
    def __init__(self, the_results):
        self.results = the_results

    # prints a summary of revenue for each strategy
    def print_summary(self):
        print("")
        print("Summary")

        best_strat_name = ""
        best_money = -1
        money_tracker = {}

        for key in self.results:
            data_row = self.results[key]
            rev = data_row["revenue"]
            # sum up the sold column
            total_sold = data_row["data"]["sold"].sum()
            left = data_row["leftover"]

            money_tracker[key] = rev
            print(
                "  "
                + key
                + " -> revenue: "
                + str(round(rev, 0))
                + ", sold: "
                + str(total_sold)
                + ", left: "
                + str(left)
            )

            if rev > best_money:
                best_money = rev
                best_strat_name = key

        print("")
        print("  Winner:", best_strat_name)

        # show % gain vs static
        if "static" in money_tracker:
            base_money = money_tracker["static"]
        else:
            base_money = 1  # avoid dividing by zero just in case

        for key in money_tracker:
            rmoney = money_tracker[key]
            if key == "static":
                pass  # skip static
            else:
                difference = rmoney - base_money
                percent_gain = (difference / base_money) * 100
                gain_rounded = round(percent_gain, 1)
                print("  " + key + " is " + str(gain_rounded) + "% better than static")

    # saves a CSV and 3 graphs to the output folder
    def save_outputs(self, my_folder="output"):
        # try to make directories so it doesnt crash if they exist
        try:
            os.makedirs(my_folder)
        except:
            pass

        try:
            os.makedirs(my_folder + "/graphs")
        except:
            pass

        # combine all data and save to csv
        list_of_frames = []
        for n in self.results:
            df = self.results[n]["data"].copy()
            df["strategy_name"] = n
            list_of_frames.append(df)

        big_df = pd.concat(list_of_frames, ignore_index=True)
        big_df.to_csv(my_folder + "/results.csv", index=False)
        print("  saved results.csv to out folder")

        # graph 1 - revenue over time
        plt.figure(figsize=(10, 5))
        for n in self.results:
            df = self.results[n]["data"]
            plt.plot(df["day"], df["total_revenue"], label=n)

        plt.title("Revenue over time")
        plt.xlabel("Day of simulation")
        plt.ylabel("Total Revenue so far")
        plt.legend()
        plt.grid(True)
        plt.savefig(my_folder + "/graphs/revenue_vs_time.png")
        plt.close()

        # graph 2 - price changes
        plt.figure(figsize=(10, 5))
        for n in self.results:
            df = self.results[n]["data"]
            plt.plot(df["day"], df["price"], label=n)

        plt.title("Price changes over time")
        plt.xlabel("Day")
        plt.ylabel("What is the Price")
        plt.legend()
        plt.grid(True)
        plt.savefig(my_folder + "/graphs/price_over_time.png")
        plt.close()

        # graph 3 - bar chart of total revenue
        plt.figure(figsize=(7, 5))
        nm_list = []
        rev_list = []

        for n in self.results:
            nm_list.append(n)
            rev_list.append(self.results[n]["revenue"])

        plt.bar(nm_list, rev_list, color=["gray", "blue", "green"])
        plt.title("Total Revenue Comparison - who won")
        plt.ylabel("Revenue Amount")
        plt.savefig(my_folder + "/graphs/strategy_comparison.png")
        plt.close()

        print("  saved the 3 graphs to " + my_folder + "/graphs/")

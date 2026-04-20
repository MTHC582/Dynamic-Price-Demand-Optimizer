import matplotlib.pyplot as plt
import pandas as pd
import os


class SimulationAnalyzer:
    def __init__(self, results):
        self.results = results

    # prints a summary of revenue for each strategy
    def print_summary(self):
        print("\nSummary")

        best_name = None
        best_rev = 0
        rev_map = {}

        for name, data in self.results.items():
            r = data["revenue"]
            s = data["data"]["sold"].sum()
            lf = data["leftover"]
            rev_map[name] = r
            print(f"  {name} -> revenue: {r:.0f}, sold: {s}, left: {lf}")

            if r > best_rev:
                best_rev = r
                best_name = name

        print(f"\n  Winner: {best_name}")

        # show % gain vs static
        base = rev_map.get("static", 1)
        for name, r in rev_map.items():
            if name == "static":
                continue
            gain = ((r - base) / base) * 100
            print(f"  {name} is {gain:.1f}% better than static")

    # saves a CSV and 3 graphs to the output folder
    def save_outputs(self, out_dir="output"):
        os.makedirs(out_dir, exist_ok=True)
        os.makedirs(f"{out_dir}/graphs", exist_ok=True)

        # combine all data and save to csv
        all_data = []
        for name, data in self.results.items():
            df = data["data"].copy()
            df["strategy_name"] = name
            all_data.append(df)

        pd.concat(all_data, ignore_index=True).to_csv(
            f"{out_dir}/results.csv", index=False
        )
        print(f"  saved results.csv")

        # graph 1 - revenue over time
        plt.figure(figsize=(10, 5))
        for name, data in self.results.items():
            df = data["data"]
            plt.plot(df["day"], df["total_revenue"], label=name)
        plt.title("Revenue over time")
        plt.xlabel("Day")
        plt.ylabel("Revenue")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{out_dir}/graphs/revenue_vs_time.png")
        plt.close()

        # graph 2 - price changes
        plt.figure(figsize=(10, 5))
        for name, data in self.results.items():
            df = data["data"]
            plt.plot(df["day"], df["price"], label=name)
        plt.title("Price changes over time")
        plt.xlabel("Day")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{out_dir}/graphs/price_over_time.png")
        plt.close()

        # graph 3 - bar chart of total revenue
        plt.figure(figsize=(7, 5))
        names = list(self.results.keys())
        revs = [self.results[s]["revenue"] for s in names]
        plt.bar(names, revs, color=["gray", "steelblue", "seagreen"])
        plt.title("Total Revenue Comparison")
        plt.ylabel("Revenue")
        plt.savefig(f"{out_dir}/graphs/strategy_comparison.png")
        plt.close()

        print(f"  saved graphs to {out_dir}/graphs/")

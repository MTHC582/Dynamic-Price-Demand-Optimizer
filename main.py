import sys
import json
import copy
from core.simulator import PricingSimulator
from core.analysis import SimulationAnalyzer
from core.strategies import StaticPricing, DynamicPricing, AdvancedPricing


# runs all strategies on a few different market configs to test robustness
def my_stress_test(base_cfg):
    print("")
    print("Stress Test")

    # setup test cases manually
    case1 = {"name": "Low demand", "base_demand": 50, "sensitivity": 1.5}
    case2 = {"name": "High demand", "base_demand": 150, "sensitivity": 1.0}
    case3 = {"name": "Very sensitive", "base_demand": 100, "sensitivity": 2.2}
    case4 = {"name": "Less stock", "initial_inventory": 200}

    my_tests = [case1, case2, case3, case4]

    strats = {}
    strats["static"] = StaticPricing()
    strats["dynamic"] = DynamicPricing()
    strats["advanced"] = AdvancedPricing()

    # keep track of wins
    win_tally = {"static": 0, "dynamic": 0, "advanced": 0}

    counter = 1
    for t_case in my_tests:
        # get name then delete it so it doesnt mess up config
        lbl = t_case["name"]
        del t_case["name"]

        # copy dict so we don't change the original
        config_copy = copy.deepcopy(base_cfg)
        for key in t_case:
            config_copy[key] = t_case[key]

        print("  Test " + str(counter) + " - " + lbl)

        sim = PricingSimulator(config_copy)
        r = sim.run_all(strats, show_print=False)

        # find the best one
        highest_rev = 0
        best_strat = ""
        for s_name in r:
            rev_here = r[s_name]["revenue"]
            if rev_here > highest_rev:
                highest_rev = rev_here
                best_strat = s_name

        print("    best was:", best_strat)
        win_tally[best_strat] = win_tally[best_strat] + 1

        counter = counter + 1

    # find who has most wins
    max_wins = -1
    overall_best = ""
    for key in win_tally:
        if win_tally[key] > max_wins:
            max_wins = win_tally[key]
            overall_best = key

    print("")
    print("  Most wins overall:", overall_best)
    print("")


def main():
    print("Dynamic Pricing Simulator")
    print("")

    # read config
    config = {}
    try:
        f = open("config.json", "r")
        config = json.load(f)
        f.close()  # don't forget to close!
        print("config loaded ok")
    except Exception as e:
        print("Error loading config!", e)
        sys.exit(1)

    print("Config values:")
    for key in config:
        print("  " + key + " = " + str(config[key]))

    # run it!
    strats = {}
    strats["static"] = StaticPricing()
    strats["dynamic"] = DynamicPricing()
    strats["advanced"] = AdvancedPricing()

    sim = PricingSimulator(config)
    res = sim.run_all(strats)

    analyzer = SimulationAnalyzer(res)
    analyzer.print_summary()
    analyzer.save_outputs()

    # run stress test at the end
    my_stress_test(config)

    print("Done. Check the output folder for the files.")


# If You run from this file ,use "python main.py" in terminal
if __name__ == "__main__":
    main()

import sys
import json
import copy
from core.simulator import PricingSimulator
from core.analysis import SimulationAnalyzer
from core.strategies import StaticPricing, DynamicPricing, AdvancedPricing


# runs all strategies on a few different market configs to test robustness
def stress_test(base_cfg):
    print("\nStress Test")

    test_cases = [
        {"name": "Low demand",     "base_demand": 50,  "sensitivity": 1.5},
        {"name": "High demand",    "base_demand": 150, "sensitivity": 1.0},
        {"name": "Very sensitive", "base_demand": 100, "sensitivity": 2.2},
        {"name": "Less stock",     "initial_inventory": 200},
    ]

    strats = {
        "static":   StaticPricing(),
        "dynamic":  DynamicPricing(),
        "advanced": AdvancedPricing(),
    }

    win_count = {}

    for i, case in enumerate(test_cases, 1):
        label = case.pop("name")
        cfg   = copy.deepcopy(base_cfg)
        cfg.update(case)

        print(f"  Test {i} - {label}")

        sim   = PricingSimulator(cfg)
        res   = sim.run_all(strats, show_log=False)
        best  = max(res, key=lambda k: res[k]["revenue"])

        print(f"    best: {best}")
        win_count[best] = win_count.get(best, 0) + 1

    overall = max(win_count, key=win_count.get)
    print(f"\n  Most wins overall: {overall}")
    print("")


def main():
    print("Dynamic Pricing Simulator\n")

    try:
        with open("config.json", "r") as f:
            config = json.load(f)
        print("config loaded")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("Config:")
    for k, v in config.items():
        print(f"  {k} = {v}")

    strats = {
        "static":   StaticPricing(),
        "dynamic":  DynamicPricing(),
        "advanced": AdvancedPricing(),
    }

    sim     = PricingSimulator(config)
    results = sim.run_all(strats)

    analyzer = SimulationAnalyzer(results)
    analyzer.print_summary()
    analyzer.save_outputs()

    stress_test(config)

    print("Done. Check output/ for files.")


if __name__ == "__main__":
    main()

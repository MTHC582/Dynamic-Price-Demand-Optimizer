import sys
import copy
from utils.helpers import load_config
from simulation.simulator import PricingSimulator
from analysis.analysis import SimulationAnalyzer
from models.strategies import StaticPricing, DynamicPricing, AdvancedPricing

def run_scenarios(base_config):
    """
    Executes multiple market scenarios to evaluate strategy robustness.
    """
    print("\nSCENARIO-BASED SENSITIVITY ANALYSIS")
    print("Evaluating strategy performance across varied market conditions")

    scenarios = [
        {"name": "Low Demand", "base_demand": 50, "elasticity": 1.5},
        {"name": "High Demand", "base_demand": 150, "elasticity": 1.0},
        {"name": "Price Sensitivity", "base_demand": 100, "elasticity": 2.2},
        {"name": "Limited Inventory", "initial_inventory": 200, "time_steps": 100}
    ]

    strategy_map = {
        'static': StaticPricing(),
        'dynamic': DynamicPricing(),
        'advanced': AdvancedPricing()
    }

    best_overall_strategy = {}

    for i, scenario in enumerate(scenarios, 1):
        print(f"\nScenario {i} [{scenario['name']}]:")
        
        current_config = copy.deepcopy(base_config)
        current_config.update(scenario)
        
        sim = PricingSimulator(current_config)
        results = sim.run_all(strategy_map, verbose=False)
        
        best_strat = max(results, key=lambda k: results[k]['revenue'])
        print(f" > Optimal Strategy: {best_strat.capitalize()}")
        
        best_overall_strategy[best_strat] = best_overall_strategy.get(best_strat, 0) + 1

    final_winner = max(best_overall_strategy, key=best_overall_strategy.get)
    print("\nCONSOLIDATED SCENARIO RESULTS")
    print(f"Overall Most Robust Strategy: {final_winner.capitalize()}")
    print("----------------------------------------\n")

def main():
    print("\nSIMULATION INITIALIZATION")
    print("Dynamic Pricing & Demand Optimization System")
    print("----------------------------------------")
    
    try:
        config = load_config("data/config.json")
    except Exception as e:
        print(f"Initialization Error: {e}")
        sys.exit(1)

    print("\nCONFIGURATION PARAMETERS")
    print(f" - Base Demand: {config['base_demand']}")
    print(f" - Elasticity: {config['elasticity']}")
    print(f" - Initial Inventory: {config['initial_inventory']}")
    print(f" - Simulation Steps: {config['time_steps']}")

    # 1. Primary Execution
    strategy_map = {
        'static': StaticPricing(),
        'dynamic': DynamicPricing(),
        'advanced': AdvancedPricing()
    }
    
    simulator = PricingSimulator(config)
    results = simulator.run_all(strategy_map)

    # 2. Analysis & Export
    analyzer = SimulationAnalyzer(results)
    analyzer.generate_report()
    analyzer.export_data_and_graphs()

    # 3. Stress Testing
    run_scenarios(config)

    print("\nFINAL STATUS")
    print("Execution complete. Data and visualizations exported to /output.")
    print("----------------------------------------\n")

if __name__ == "__main__":
    main()

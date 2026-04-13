import pandas as pd
from typing import Dict, Any, List
from models.market import MarketEnvironment
from models.strategies import PricingStrategy

class PricingSimulator:
    """
    Core engine that executes the simulation across different strategies.
    Supports a plug-and-play architecture for any PricingStrategy.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the simulator with configuration parameters.
        """
        self.config = config
        self.market = MarketEnvironment(config)
        self.initial_inventory = config.get('initial_inventory', 500)
        self.time_steps = config.get('time_steps', 100)
        self.base_price = config.get('base_price', 100.0)

    def run_strategy(self, strategy_obj: PricingStrategy, strategy_name: str) -> Dict[str, Any]:
        """
        Executes a single pricing strategy through all time steps.
        
        Args:
            strategy_obj (PricingStrategy): An instance of a class implementing PricingStrategy.
            strategy_name (str): Display name for the strategy.
            
        Returns:
            Dict: Results containing historical data, final revenue, and inventory left.
        """
        inventory = self.initial_inventory
        revenue = 0
        history = []

        for t in range(self.time_steps):
            if inventory <= 0:
                break # Out of stock

            # 1. Determine Price using Strategy Pattern
            context = {
                'inventory': inventory,
                'initial_inventory': self.initial_inventory,
                'time_step': t,
                'total_steps': self.time_steps,
                'base_price': self.base_price
            }
            price = strategy_obj.calculate_price(context)

            # 2. Observe Market Reaction (with Customer Segmentation)
            expected_demand = self.market.get_total_expected_demand(price)
            actual_purchases = self.market.simulate_actual_purchases(expected_demand)

            # 3. Fulfill Orders
            sold = min(actual_purchases, inventory)
            inventory -= sold
            revenue += sold * price

            # 4. Log Data
            history.append({
                'time_step': t,
                'strategy': strategy_name,
                'price': round(price, 2),
                'sold': sold,
                'remaining_inventory': inventory,
                'cumulative_revenue': round(revenue, 2)
            })

        df = pd.DataFrame(history)
        return {
            'data': df,
            'revenue': round(revenue, 2),
            'leftover': inventory
        }

    def run_all(self, strategy_map: Dict[str, PricingStrategy], verbose: bool = True) -> Dict[str, Any]:
        """
        Runs multiple strategies sequentially for comparison.
        """
        if verbose:
            print("\nSTRATEGY EXECUTION LOG")

        results = {}
        for name, strategy_obj in strategy_map.items():
            if verbose:
                print(f" - Running: {name.capitalize()} Pricing Model")
            
            res = self.run_strategy(strategy_obj, name)
            results[name] = res

        return results

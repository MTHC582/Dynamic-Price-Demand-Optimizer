
import pandas as pd
from core.market import MarketEnvironment


class PricingSimulator:

    def __init__(self, config):
        self.config     = config
        self.market     = MarketEnvironment(config)
        self.init_stock = config.get("initial_inventory", 500)
        self.num_days   = config.get("simulation_days", 100)
        self.base_price = config.get("base_price", 100.0)

    # runs one strategy from day 0 to end and tracks everything
    def run_one(self, strategy, name):
        stock    = self.init_stock
        earnings = 0
        rows     = []

        for day in range(self.num_days):
            if stock <= 0:
                break

            # info the strategy needs to pick a price
            ctx = {
                "inventory":         stock,
                "initial_inventory": self.init_stock,
                "time_step":         day,
                "total_steps":       self.num_days,
                "base_price":        self.base_price,
            }

            price = strategy.calculate_price(ctx)

            # simulate how many people buy at this price
            exp = self.market.get_total_expected_demand(price)
            act = self.market.simulate_actual_purchases(exp)

            sold      = min(act, stock)
            stock    -= sold
            earnings += sold * price

            rows.append({
                "day":           day,
                "strategy":      name,
                "price":         round(price, 2),
                "sold":          sold,
                "stock_left":    stock,
                "total_revenue": round(earnings, 2),
            })

        return {
            "data":     pd.DataFrame(rows),
            "revenue":  round(earnings, 2),
            "leftover": stock
        }

    # runs all strategies and returns all results together
    def run_all(self, strategies, show_log=True):
        if show_log:
            print("\nRunning strategies...")

        results = {}
        for name, strat in strategies.items():
            if show_log:
                print(f"  -> {name}")
            results[name] = self.run_one(strat, name)

        return results

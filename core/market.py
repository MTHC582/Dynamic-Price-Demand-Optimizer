import numpy as np


# This class is for Simulating a market environment
# Such as customer segments and price sensitivity alon with demand
class MarketEnvironment:
    def __init__(self, config):
        self.base_demand = config.get("base_demand", 100)
        self.sensitivity = config.get("sensitivity", 1.2)
        self.max_customers = config.get("max_customers_per_day", 120)
        self.base_price = config.get("base_price", 100.0)

        #  Budget : Highly sensitive (around 1.5 times)
        #  Regular: Moderate (base value pr no change)
        #  Urgent : Low sensitivity (around 0.5 times)
        self.segments = {
            "Budget": {"portion": 0.4, "sensitivity": self.sensitivity * 1.5},
            "Regular": {"portion": 0.4, "sensitivity": self.sensitivity},
            "Urgent": {"portion": 0.2, "sensitivity": self.sensitivity * 0.5},
        }

    def get_segment_demand(self, price, segment_name):
        # Formula:         (SOuce wiki...)
        # Demand = Segment Base Demand * (Base Price / Price) ^ Segment Elasticity

        segment = self.segments[segment_name]
        segment_base_demand = self.base_demand * segment["portion"]

        demand = segment_base_demand * (
            (self.base_price / price) ** segment["sensitivity"]
        )
        return demand

    def get_total_expected_demand(self, price):
        # Gathers demand from all customer segments.
        total_demand = 0
        for seg in self.segments:
            total_demand += self.get_segment_demand(price, seg)
        return min(total_demand, self.max_customers)

    def simulate_actual_purchases(self, expected_demand):
        # In ordre to simulate random purchase via poisson distribution
        realisitc_purchase_value = np.random.poisson(expected_demand)
        return int(realisitc_purchase_value)

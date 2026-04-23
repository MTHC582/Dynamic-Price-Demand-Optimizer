import numpy as np
# from random import randint


# This class is for Simulating a market environment
# Such as customer segments and price sensitivity alon with demand
class MarketEnvironment:
    def __init__(self, conf):
        self.base_demand = conf.get(
            "base_demand", 100
        )  # get method to make sure it wont crash
        self.sensitivity = conf.get("sensitivity", 1.2)
        self.max_customers = conf.get("max_customers_per_day", 120)
        self.base_price = conf.get("base_price", 100.0)

        #  Budget : Highly sensitive (around 1.5 times)
        #  Regular: Moderate (base value pr no change)
        #  Urgent : Low sensitivity (around 0.5 times)

        # setting up the segments here
        self.segments = {}
        self.segments["Budget"] = {
            "portion": 0.4,
            "sensitivity": self.sensitivity * 1.5,
        }
        self.segments["Regular"] = {"portion": 0.4, "sensitivity": self.sensitivity}
        self.segments["Urgent"] = {
            "portion": 0.2,
            "sensitivity": self.sensitivity * 0.5,
        }

    def get_segment_demand(self, curr_price, seg_name):
        # Formula:         (SOuce wiki...)
        # Demand = Segment Base Demand * (Base Price / Price) ^ Segment Elasticity

        my_seg = self.segments[seg_name]

        # find the base demand for this specific segment
        seg_base_demand = self.base_demand * my_seg["portion"]

        # calculating the formula
        math_part1 = self.base_price / curr_price
        math_part2 = math_part1 ** my_seg["sensitivity"]
        final_demand = seg_base_demand * math_part2

        return final_demand

    def get_total_expected_demand(self, the_price):
        # Gathers demand from all customer segments.
        tot = 0
        for s in self.segments:
            d = self.get_segment_demand(the_price, s)
            tot = tot + d

        # don't allow more than max customers
        if tot > self.max_customers:
            tot = self.max_customers

        return tot

    def simulate_actual_purchases(self, expected_amt):
        # In ordre to simulate random purchase via poisson distribution
        # makes it somewht realistic
        realisitc_purchase_value = np.random.poisson(expected_amt)
        # cautious enough to return an integer
        return int(realisitc_purchase_value)

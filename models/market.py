import numpy as np
from typing import Dict, Any

class MarketEnvironment:
    """
    Simulates a market environment with customer segments and price elasticity.
    The environment models how demand reacts to price changes across different buyer groups.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the market parameters.
        
        Args:
            config (Dict[str, Any]): Dictionary containing base_demand, elasticity, 
                                     and other environmental constraints.
        """
        self.base_demand = config.get('base_demand', 100)
        self.elasticity = config.get('elasticity', 1.2)
        self.max_customers = config.get('max_customers_per_step', 120)
        self.base_price = config.get('base_price', 100.0)

        # Define Customer Segments (Microeconomics/Stochastic logic)
        # Budget: Highly sensitive, Regular: Moderate, Urgent: Low sensitivity
        self.segments = {
            "Budget": {"portion": 0.4, "elasticity": self.elasticity * 1.5},
            "Regular": {"portion": 0.4, "elasticity": self.elasticity},
            "Urgent": {"portion": 0.2, "elasticity": self.elasticity * 0.5}
        }

    def get_segment_demand(self, price: float, segment_name: str) -> float:
        """
        Calculates demand for a specific segment using price elasticity.
        Formula: Segment Base Demand * (Base Price / Price) ^ Segment Elasticity
        """
        segment = self.segments[segment_name]
        segment_base_demand = self.base_demand * segment['portion']
        
        # Power-law elasticity model
        demand = segment_base_demand * ((self.base_price / price) ** segment['elasticity'])
        return demand

    def get_total_expected_demand(self, price: float) -> float:
        """
        Aggregates demand from all customer segments.
        """
        total_demand = sum(self.get_segment_demand(price, seg) for seg in self.segments)
        return min(total_demand, self.max_customers)

    def simulate_actual_purchases(self, expected_demand: float) -> int:
        """
        Simulates stochastic (random) purchases using Poisson distribution.
        Poisson models independent arrival events, a core concept in Queueing Theory.
        """
        actual_purchases = np.random.poisson(expected_demand)
        return int(actual_purchases)

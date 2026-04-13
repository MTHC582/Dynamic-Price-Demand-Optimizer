from abc import ABC, abstractmethod
from typing import Dict, Any

class PricingStrategy(ABC):
    """
    Abstract Base Class for all pricing strategies.
    This follows the Strategy Pattern, allowing for high extendibility.
    New strategies can be added by simply subclassing this.
    """
    
    @abstractmethod
    def calculate_price(self, context: Dict[str, Any]) -> float:
        """
        Calculates the price based on provided market and inventory context.
        
        Args:
            context (Dict[str, Any]): Dictionary containing 'inventory', 'initial_inventory', 
                                     'time_step', 'total_steps', 'base_price', etc.
                                     
        Returns:
            float: The calculated price.
        """
        pass

class StaticPricing(PricingStrategy):
    """
    Strategy 1: Fixed pricing regardless of market conditions.
    Provides a baseline for comparison.
    """
    def calculate_price(self, context: Dict[str, Any]) -> float:
        return context.get('base_price', 100.0)

class DynamicPricing(PricingStrategy):
    """
    Strategy 2: Basic reactive pricing based on inventory vs time.
    Uses simple thresholds to adjust price when sales are ahead or behind schedule.
    """
    def calculate_price(self, context: Dict[str, Any]) -> float:
        inventory = context['inventory']
        initial_inventory = context['initial_inventory']
        time_step = context['time_step']
        total_steps = context['total_steps']
        base_price = context.get('base_price', 100.0)
        
        time_ratio = (total_steps - time_step) / total_steps
        inventory_ratio = inventory / initial_inventory
        
        # If we have too much stock for the remaining time, drop the price (Discounting)
        if inventory_ratio > time_ratio + 0.1:
            return base_price * 0.85 
        # If we are selling out too fast, raise the price (Premium)
        elif inventory_ratio < time_ratio - 0.1:
            return base_price * 1.25 
            
        return base_price

class AdvancedPricing(PricingStrategy):
    """
    Strategy 3: Sophisticated dynamic pricing (Inventory + Time + Scarcity).
    Models urgency and inventory pressure more granularly.
    """
    def calculate_price(self, context: Dict[str, Any]) -> float:
        inventory = context['inventory']
        initial_inventory = context['initial_inventory']
        time_step = context['time_step']
        total_steps = context['total_steps']
        base_price = context.get('base_price', 100.0)
        
        time_left_ratio = max((total_steps - time_step) / total_steps, 0.01)
        inventory_ratio = inventory / initial_inventory
        
        # Urgency factor: ratio of inventory left vs time left
        # urgency > 1 means we have more inventory than proportional time remaining
        urgency_factor = inventory_ratio / time_left_ratio
        
        if urgency_factor > 1.5:
            return base_price * 0.70  # Desperate clear-out
        elif urgency_factor > 1.1:
            return base_price * 0.90  # Mild discount
        elif urgency_factor < 0.4:
            return base_price * 1.50  # High scarcity premium
        elif urgency_factor < 0.8:
            return base_price * 1.15  # Mild premium
            
        return base_price

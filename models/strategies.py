# Parent Class to define the structure of the pricing strategy
# we will be passing this class via inheritance
class PricingStrategy:
    def calculate_price(self, context):
        """
        Calculates the price based on provided market and inventory context.

        Args:
            context (Dict[str, float]): Dictionary containing 'inventory', 'initial_inventory',
                                     'time_step', 'total_steps', 'base_price', etc.

        Returns:
            float: The calculated price.
        """
        pass


class StaticPricing(PricingStrategy):
    """
    Strategy 1: Fixed pricing regardless of market conditions.
                Just for a Baselne comparison.
    """

    def calculate_price(self, context):
        return context.get("base_price", 100.0)


class DynamicPricing(PricingStrategy):
    """
    Strategy 2: Basic dynamic/changing pricing based on inventory and time
                Adjusts price when sales are ahead or behind schedule
    """

    def calculate_price(self, context):
        inventory = context["inventory"]
        initial_inventory = context["initial_inventory"]
        time_step = context["time_step"]
        total_steps = context["total_steps"]
        base_price = context.get("base_price", 100.0)

        time_ratio = (total_steps - time_step) / total_steps
        inventory_ratio = inventory / initial_inventory

        # We got too mcuh stock hence drop the price instead(discount)
        # or else if we are selling out ahead of time, raise the price..
        if inventory_ratio > time_ratio + 0.1:
            return base_price * 0.85
        elif inventory_ratio < time_ratio - 0.1:
            return base_price * 1.25

        return base_price


class AdvancedPricing(PricingStrategy):
    """
    Strategy 3: Advanced dynamic pricing (Inventory + Time + Scarcity)
                Handles pricing by adjusting the price based on the urgency (time factor)
    """

    def calculate_price(self, context):
        inventory = context["inventory"]
        initial_inventory = context["initial_inventory"]
        time_step = context["time_step"]
        total_steps = context["total_steps"]
        base_price = context.get("base_price", 100.0)

        time_left_ratio = max((total_steps - time_step) / total_steps, 0.01)
        inventory_ratio = inventory / initial_inventory

        # We define the Urgency factor as the ratio of inventory left vs time left
        # urgency > 1 means we have more inventory left ahead of timin
        urgency_factor = inventory_ratio / time_left_ratio

        # Approx vals Source: Wiki..
        if urgency_factor > 1.5:
            return base_price * 0.70  # Desperate clear-out
        elif urgency_factor > 1.1:
            return base_price * 0.90  # Mild discount
        elif urgency_factor < 0.4:
            return base_price * 1.50  # High scarcity premium
        elif urgency_factor < 0.8:
            return base_price * 1.15  # Mild premium

        # between 0.5 to 1... no change
        return base_price

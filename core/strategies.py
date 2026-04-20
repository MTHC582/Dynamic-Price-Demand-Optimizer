
# base class for all strategies
# every strategy needs to have a calculate_price method
class PricingStrategy:
    def calculate_price(self, ctx):
        pass   # will be filled by child class


# Strategy 1 - just returns a fixed price always
# using this to compare with other strategies
class StaticPricing(PricingStrategy):
    def calculate_price(self, ctx):
        p = ctx.get("base_price", 100.0)
        return p


# Strategy 2 - changes price based on how much stock is left and time remaining
class DynamicPricing(PricingStrategy):
    def calculate_price(self, ctx):
        curr_inv   = ctx["inventory"]
        start_inv  = ctx["initial_inventory"]
        curr_day   = ctx["time_step"]
        total_days = ctx["total_steps"]
        p          = ctx.get("base_price", 100.0)

        # ratio of time left
        t_ratio = (total_days - curr_day) / total_days
        # ratio of stock left
        s_ratio = curr_inv / start_inv

        # if we have more stock than expected at this time
        if s_ratio > t_ratio + 0.1:
            return p * 0.85   # sell cheaper to move stock

        # if we're running out faster than expected
        if s_ratio < t_ratio - 0.1:
            return p * 1.25   # can charge more

        return p   # no change, things are balanced


# Strategy 3 - uses an urgency score to decide price changes
# urgency = how much stock we have vs how much time we have
class AdvancedPricing(PricingStrategy):
    def calculate_price(self, ctx):
        curr_inv   = ctx["inventory"]
        start_inv  = ctx["initial_inventory"]
        curr_day   = ctx["time_step"]
        total_days = ctx["total_steps"]
        p          = ctx.get("base_price", 100.0)

        t_left  = max((total_days - curr_day) / total_days, 0.01)
        s_ratio = curr_inv / start_inv

        urgency = s_ratio / t_left   # > 1 means too much stock left

        if urgency > 1.5:
            return p * 0.70   # lots of stock, big discount
        elif urgency > 1.1:
            return p * 0.90   # a bit overstocked, small discount
        elif urgency < 0.4:
            return p * 1.50   # running very low, charge premium
        elif urgency < 0.8:
            return p * 1.15   # getting low, small increase

        return p   # somewhere in the middle, keep price

# python file for my strategies

# class PricingStrategy:
#     pass

# Strategy 1 - just returns a fixed price always
# using this to compare with my other strategies
class StaticPricing:
    def calculate_price(self, my_info_dict):
        # get the price. if not there, use 100
        if "base_price" in my_info_dict:
            my_price = my_info_dict["base_price"]
        else:
            my_price = 100.0

        return my_price


# Strategy 2 - changes price based on how much stock is left and time remaining
class DynamicPricing:
    def calculate_price(self, info):
        stock_now = info["inventory"]
        start_stock = info["initial_inventory"]
        day_now = info["time_step"]
        total_days = info["total_steps"]

        if "base_price" in info:
            my_price = info["base_price"]
        else:
            my_price = 100.0

        # math to see how much time left
        time_left_percent = (total_days - day_now) / total_days

        # math to see how much stock left
        stock_left_percent = stock_now / start_stock

        # check if we are stuck with too much stock
        if stock_left_percent > time_left_percent + 0.1:
            return my_price * 0.85  # discount it by 15 percent

        # check if we are selling out too fast
        if stock_left_percent < time_left_percent - 0.1:
            return my_price * 1.25  # make it more expensive

        # otherwise return normal price
        return my_price


# Strategy 3 - uses an urgency score to decide price changes
class AdvancedPricing:
    def calculate_price(self, data):
        stock = data["inventory"]
        start = data["initial_inventory"]
        day = data["time_step"]
        total = data["total_steps"]

        if "base_price" in data:
            price = data["base_price"]
        else:
            price = 100.0

        time_left = (total - day) / total
        if time_left < 0.01:
            time_left = 0.01  # prevent divide by zero error i got here before

        stock_ratio = stock / start

        # urgency score
        urg = stock_ratio / time_left

        # print("urgency is", urg)

        if urg > 1.5:
            new_price = price * 0.70  # mega sale
            return new_price
        if urg > 1.1:
            return price * 0.90  # mini sale
        if urg < 0.4:
            return price * 1.50
        if urg < 0.8:
            return price * 1.15

        return price

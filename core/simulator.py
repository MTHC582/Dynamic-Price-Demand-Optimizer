import pandas as pd
from core.market import MarketEnvironment


# this runs the whole thing
class PricingSimulator:
    def __init__(self, my_config):
        self.config = my_config
        self.market = MarketEnvironment(my_config)
        self.init_stock = my_config.get("initial_inventory", 500)
        self.num_days = my_config.get("simulation_days", 100)
        self.base_price = my_config.get("base_price", 100.0)

    # runs one strategy from day 0 to end and tracks everything
    def run_one(self, strat_obj, strat_name):
        current_stock = self.init_stock
        money_made = 0
        all_the_rows = []

        day = 0
        while day < self.num_days:
            # stop if we have no stock
            if current_stock <= 0:
                break

            # all the info to give to the strategy
            my_context = {
                "inventory": current_stock,
                "initial_inventory": self.init_stock,
                "time_step": day,
                "total_steps": self.num_days,
                "base_price": self.base_price,
            }

            the_price = strat_obj.calculate_price(my_context)

            # figure out how many ppl buy
            expected = self.market.get_total_expected_demand(the_price)
            actual_buy = self.market.simulate_actual_purchases(expected)

            # we can't sell more than we have
            if actual_buy > current_stock:
                amount_sold = current_stock
            else:
                amount_sold = actual_buy

            current_stock = current_stock - amount_sold
            money_made = money_made + (amount_sold * the_price)

            # save this row for later
            row_data = {}
            row_data["day"] = day
            row_data["strategy"] = strat_name
            row_data["price"] = round(the_price, 2)
            row_data["sold"] = amount_sold
            row_data["stock_left"] = current_stock
            row_data["total_revenue"] = round(money_made, 2)
            all_the_rows.append(row_data)

            day = day + 1

        # make the final dictionary
        final_dict = {}
        final_dict["data"] = pd.DataFrame(
            all_the_rows
        )  # using pandas here for the output
        final_dict["revenue"] = round(money_made, 2)
        final_dict["leftover"] = current_stock

        return final_dict

    # runs all strategies and returns all results together
    def run_all(self, strat_dict, show_print=True):
        if show_print == True:
            print("")
            print("Running strategies...")

        results_dict = {}

        # loop through dictionary
        for key in strat_dict:
            strat_val = strat_dict[key]
            if show_print == True:
                print("  -> " + key)

            # run it and save to results
            res = self.run_one(strat_val, key)
            results_dict[key] = res

        return results_dict

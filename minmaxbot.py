import random
from collections import defaultdict
from itertools import product

from bot import Bot
from launcher import launch
from game_facade import GameFacade, Unit

class MinmaxBot(Bot):

    def __init__(self, ip_address, port, name, power_name):
        super().__init__(ip_address, port, name, power_name)
        self.enemies = ["RUSSIA", "AUSTRIA"]

    def get_my_orders(self, my_orderable_locations, all_possible_orders):
        my_orders = {}
        for loc in my_orderable_locations:
            if all_possible_orders[loc]:
                my_orders[loc] = all_possible_orders[loc]
            else:
                raise Exception()
        return my_orders

    def location_len(self, location):
        if location in ["BUL", "STP", "SPA"]:
            return len(location) + 3
        return len(location)

    def is_move(self, location, order):
        L = 2 + self.location_len(location) + 1
        return len(order) > L and order[L] == '-'
        
    def is_hold(self, location, order):
        L = 2 + self.location_len(location) + 1
        return len(order) == L + 1 and order[L] == 'H'

    def get_move_hold_orders(self, loc_orders_dict):
        loc_moves_dict = defaultdict(list)
        for loc, orders in loc_orders_dict.items():
            for order in orders:
                if self.is_move(loc, order) or self.is_hold(loc, order):
                    loc_moves_dict[loc].append(order)
        return loc_moves_dict

    def get_moves_holds_combinations(self, loc_orders_dict):
        loc_moves_holds_dict = self.get_move_hold_orders(loc_orders_dict)

        combinations = list(product(*loc_moves_holds_dict.values()))

        print("dfsd")
        return combinations

    def get_orders(self, game, power_name):
        possible_orders = game.get_all_possible_orders()
        my_orderable_locations = game.get_orderable_locations(power_name)
        current_phase_type = game.get_current_phase()[-1]
        if current_phase_type == "A": # Adjustments
                power = game.get_power(power_name)
                build_count = len(power.centers) - len(power.units)
                ordered_locations = random.sample(my_orderable_locations, abs(build_count))
                ret_orders = [random.choice([order for order in possible_orders[loc] if order != "WAIVE"]) for loc in ordered_locations]
        elif current_phase_type == "R": # Retreat
                ret_orders = [random.choice(possible_orders[loc]) for loc in game.get_orderable_locations(power_name)]
        else: # Move
            # my_orders = self.get_my_orders(my_orderable_locations, possible_orders)
            # comb_moves_holds = self.get_moves_holds_combinations(my_orders)
            # if len(comb_moves_holds):
            #     ret_orders = random.choice(comb_moves_holds)
            # else:
            #     ret_orders = [random.choice(possible_orders[loc]) for loc in game.get_orderable_locations(power_name)]
            game_facade = GameFacade(game)
            ret_orders = []
            if game_facade.isMovementPhase():
                units = game_facade.getMovesByUnit(power_name)
                for unit in units:
                    dest = random.choice(list(unit.hold_moves.keys()))
                    ret_orders.append(unit.get_hold_moves_order(dest))
            else:
                raise Exception
        return ret_orders

if __name__ == '__main__':
    launch(MinmaxBot)

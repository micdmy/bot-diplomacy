import random

from bot import Bot
from launcher import launch


class RandBot(Bot):

    def __init__(self, ip_address, port, name, power_name):
        super().__init__(ip_address, port, name, power_name)

    def get_orders(self, game, power_name):
        possible_orders = game.get_all_possible_orders()
        orders = [random.choice(possible_orders[loc]) for loc in game.get_orderable_locations(power_name) if possible_orders[loc]]
        return orders

if __name__ == '__main__':
    launch(RandBot)

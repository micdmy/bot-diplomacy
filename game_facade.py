from diplomacy.engine.game import Game
from typing import List


class Unit():
    def __init__(self, U_LOC_str):
        self.type = U_LOC_str[0]
        self.location = U_LOC_str[2:]
        self.is_on_cost = '/' in U_LOC_str

    def calculate_possible_orders(self, adjacent_locs, abuts_func):
        self.hold_moves = {self.location : None} # add hold order location
        for dest in adjacent_locs:
            if abuts_func(self.type, self.location, '-', dest): # move to dest possible?
                self.hold_moves[dest] = None
    
    def get_hold_moves_order(self, dest = ""):
        if dest == self.location: # hold order
            return GameFacade.order_string(self.type, self.location, 'H')
        else: # move order
            return GameFacade.order_string(self.type, self.location, '-', dest)


class GameFacade():
    def __init__(self, game : Game):
        self._game = game

    def isMovementPhase(self):
        return self._game.phase_type == 'M'
    
    def getMovesByUnit(self, power_name : str) -> List[Unit]:
        power = self._game.get_power(power_name)
        units = [Unit(U_LOC_str) for U_LOC_str in power.units]
        for unit in units:
            unit.calculate_possible_orders(self._game.map.dest_with_coasts[unit.location], self._game._abuts)
        return units

    @classmethod
    def order_string(cls, unit_type, location, order, dest = ""):
        return "%s %s %s %s" % (unit_type, location, order, dest)
        


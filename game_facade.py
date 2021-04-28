from diplomacy.engine.game import Game
from typing import List, Set, Tuple
from itertools import product
from copy import deepcopy
from random import choice


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
        
    @classmethod
    def get_exclusive_hold_moves_dests(cls, units : List[Unit]) -> Set[str]:
        dests = set()
        for unit in units:
            dests.update(list(unit.hold_moves.keys()))
        return dests

    @classmethod
    def get_consistent_src_dst_pairs(cls, units : List[Unit]):
        unit_iterator = iter(units)
        return cls._consistent_permutations_random(unit_iterator, next(unit_iterator), [])

    @classmethod
    def _consistent_permutations(cls, unit_iter, unit, choosen : Tuple[Unit, str]):
        used = [unit_dst_pair[1] for unit_dst_pair in choosen]
        dsts = [dst for dst in list(unit.hold_moves.keys()) if dst not in used]
        if len(dsts) == 0:
            return None
        try:
            next_unit = next(unit_iter)
            permutations = []
            for dst in dsts:
                new_permutations = cls._consistent_permutations(deepcopy(unit_iter), next_unit, choosen + [(unit, dst)])
                if new_permutations != None:
                    permutations.extend(new_permutations)
            return permutations
        except StopIteration:
            c = [(unit, dst) for dst in dsts]
            h = (c, *[[c] for c in choosen]) 
            ppp = list(product(*h))
            return ppp

    @classmethod
    def _consistent_permutations_random(cls, unit_iter, unit, choosen : Tuple[Unit, str]):
        used = [unit_dst_pair[1] for unit_dst_pair in choosen]
        dsts = [dst for dst in list(unit.hold_moves.keys()) if dst not in used]
        if len(dsts) == 0:
            return None
        try:
            next_unit = next(unit_iter)
            dst_rand = choice(dsts)
            new_permutations = cls._consistent_permutations_random(deepcopy(unit_iter), next_unit, choosen + [(unit, dst_rand)])
            if new_permutations == None:
                for dst in [dst for dst in dsts if dst != dst_rand]:
                    new_permutations = cls._consistent_permutations_random(deepcopy(unit_iter), next_unit, choosen + [(unit, dst)])
                    if new_permutations != None:
                        return new_permutations
                return None
            else:
                return new_permutations
        except StopIteration:
            dst = choice(dsts)
            c = [(unit, dst)]
            h = (c, *[[c] for c in choosen]) 
            ppp = list(product(*h))
            return ppp

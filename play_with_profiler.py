import cProfile
import pstats
from copy import deepcopy

def foo(number):
    s = "%d"%number
    if s == "(99999)":
        return True
    return False
    
a = [1,2]
b = [1,4,5]
c = [3,5,6,2]

def gener(units):
    it = iter(units)
    return func(it, next(it), [])

def func(it, unit, choosen):
    used = choosen
    dsts = [d for d in unit if d not in used]
    if len(dsts) == 0:
        return None
    try:
        next_unit = next(unit_iter)
        permutations = []
        for d in dsts:
            new_permutations = func(deepcopy(it), next_unit, choosen + [unit])
            if new_permutations != None:
                permutations.extend(new_permutations)
        return permutations
    except StopIteration:
        return list(product(dsts, *choosen))


with cProfile.Profile() as pr:
    for i in range(0, 99999):
        if foo(i):
            break

    gener(*[a, b, c]))



stats = pstats.Stats(pr)
stats.strip_dirs()
stats.print_stats()
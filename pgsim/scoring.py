from itertools import product

from resources import TYPECHART


def best_damage_multiplier(
        offensive_types: list[str],
        defensive_types: list[str],
        super_effective_factor: float = 1.6,
        ):
    """TODO"""

    multiplier = {offensive_type: 1. for offensive_type in offensive_types}
    for offensive_type, defensive_type in product(offensive_types, defensive_types):
        if offensive_type in TYPECHART[defensive_type]["weaknesses"]:
            multiplier[offensive_type] *= super_effective_factor
        if offensive_type in TYPECHART[defensive_type]["resistances"]:
            multiplier[offensive_type] /= super_effective_factor
        if offensive_type in TYPECHART[defensive_type]["immunities"]:
            multiplier[offensive_type] /= (super_effective_factor**2)
    return max(multiplier.values())


def score(object_a, object_b):
    # TODO : Differentiate between object
    f_types = object_a.get_types()
    s_types = object_b.get_types()
    multiplier_first_on_second = best_damage_multiplier(f_types, s_types)
    multiplier_second_on_first = best_damage_multiplier(s_types, f_types)
    if multiplier_first_on_second - multiplier_second_on_first > 0:
        return 1
    if multiplier_first_on_second - multiplier_second_on_first < 0:
        return -1
    return 0

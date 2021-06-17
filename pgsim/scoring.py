import logging
from itertools import product

from resources import TYPECHART
from pgsim.pokemon import DoubleType, AdvancedDoubleType


def best_damage_multiplier(
        offensive_types: set[str],
        defensive_types: set[str],
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
    if not type(object_a) == type(object_b):
        msg = f"objects do not have the same type : {type(object_a)} and {type(object_b)}"
        logging.error(msg)
        raise TypeError(msg)
    if type(object_a) == DoubleType:
        return _score_doubletype(object_a, object_b)
    if type(object_a) == AdvancedDoubleType:
        return _score_advanceddoubletype(object_a, object_b)
    raise NotImplementedError()


def _score_doubletype(object_a, object_b):
    f_types = object_a.get_types()
    s_types = object_b.get_types()
    multiplier_first_on_second = best_damage_multiplier(f_types, s_types)
    multiplier_second_on_first = best_damage_multiplier(s_types, f_types)
    if multiplier_first_on_second - multiplier_second_on_first > 0:
        return 1
    if multiplier_first_on_second - multiplier_second_on_first < 0:
        return -1
    return 0


def _score_advanceddoubletype(object_a, object_b):
    multiplier_fast_move_first_on_second = best_damage_multiplier(object_a.get_fast_move_type(), object_b.get_types())
    multiplier_fast_move_second_on_first = best_damage_multiplier(object_b.get_fast_move_type(), object_a.get_types())
    multiplier_charge_move_first_on_second = best_damage_multiplier(object_a.get_charge_move_types(), object_b.get_types())
    multiplier_charge_move_second_on_first = best_damage_multiplier(object_b.get_charge_move_types(), object_a.get_types())

    multiplier_first_on_second = (multiplier_fast_move_first_on_second+multiplier_charge_move_first_on_second)/2
    multiplier_second_on_first = (multiplier_fast_move_second_on_first+multiplier_charge_move_second_on_first)/2

    if multiplier_first_on_second - multiplier_second_on_first > 0:
        return 1
    if multiplier_first_on_second - multiplier_second_on_first < 0:
        return -1
    return 0

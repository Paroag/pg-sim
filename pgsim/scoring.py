import logging
from itertools import product

from pgsim.pokemon import DoubleType, AdvancedDoubleType
from resources import TYPECHART


def get_damage_multiplier(
    offensive_types: set[str],
    defensive_types: set[str],
    super_effective_multiplier: float = 1.6,
):
    multiplier = {offensive_type: 1. for offensive_type in offensive_types}
    for offensive_type, defensive_type in product(offensive_types, defensive_types):
        if offensive_type in TYPECHART[defensive_type]["weaknesses"]:
            multiplier[offensive_type] *= super_effective_multiplier
        if offensive_type in TYPECHART[defensive_type]["resistances"]:
            multiplier[offensive_type] /= super_effective_multiplier
        if offensive_type in TYPECHART[defensive_type]["immunities"]:
            multiplier[offensive_type] /= (super_effective_multiplier ** 2)
    return multiplier


def best_damage_multiplier(
    offensive_types: set[str],
    defensive_types: set[str],
    super_effective_multiplier: float = 1.6,
):
    return max(
        get_damage_multiplier(
            offensive_types,
            defensive_types,
            super_effective_multiplier=super_effective_multiplier
        ).values()
    )


def score(object_a, object_b, **kwargs):
    if not type(object_a) == type(object_b):
        msg = f"objects do not have the same type : {type(object_a)} and {type(object_b)}"
        logging.error(msg)
        raise TypeError(msg)
    if type(object_a) == DoubleType:
        return _score_doubletype(object_a, object_b)
    if type(object_a) == AdvancedDoubleType:
        return _score_advanceddoubletype(object_a, object_b, **kwargs)
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


def _score_advanceddoubletype(object_a, object_b, stab=1.2):
    multiplier_fast_move_first_on_second = get_damage_multiplier(object_a.get_fast_move_type(), object_b.get_types())
    multiplier_fast_move_first_on_second = {type: value*stab if type in object_a.get_types() else value for type, value in multiplier_fast_move_first_on_second.items()}
    multiplier_fast_move_first_on_second = max(multiplier_fast_move_first_on_second.values())

    multiplier_fast_move_second_on_first = get_damage_multiplier(object_b.get_fast_move_type(), object_a.get_types())
    multiplier_fast_move_second_on_first = {type: value*stab if type in object_a.get_types() else value for type, value in multiplier_fast_move_second_on_first.items()}
    multiplier_fast_move_second_on_first = max(multiplier_fast_move_second_on_first.values())

    multiplier_charge_move_first_on_second = get_damage_multiplier(object_a.get_charge_move_types(), object_b.get_types())
    multiplier_charge_move_first_on_second = {type: value*stab if type in object_a.get_types() else value for type, value in multiplier_charge_move_first_on_second.items()}
    multiplier_charge_move_first_on_second = max(multiplier_charge_move_first_on_second.values())

    multiplier_charge_move_second_on_first = get_damage_multiplier(object_b.get_charge_move_types(), object_a.get_types())
    multiplier_charge_move_second_on_first = {type: value*stab if type in object_a.get_types() else value for type, value in multiplier_charge_move_second_on_first.items()}
    multiplier_charge_move_second_on_first = max(multiplier_charge_move_second_on_first.values())

    multiplier_first_on_second = (multiplier_fast_move_first_on_second+multiplier_charge_move_first_on_second)/2
    multiplier_second_on_first = (multiplier_fast_move_second_on_first+multiplier_charge_move_second_on_first)/2

    if multiplier_first_on_second - multiplier_second_on_first > 0:
        return 1
    if multiplier_first_on_second - multiplier_second_on_first < 0:
        return -1
    return 0

import itertools
import json

from utils import set_to_tuple


def best_damage_multiplier(offensive_types, defensive_types, typechart):
    multiplier = {offensive_type: 0 for offensive_type in offensive_types}
    for offensive_type, defensive_type in itertools.product(offensive_types, defensive_types):
        if offensive_type in typechart[defensive_type]["weaknesses"]:
            multiplier[offensive_type] += 1
        if offensive_type in typechart[defensive_type]["resistances"]:
            multiplier[offensive_type] -= 1
        if offensive_type in typechart[defensive_type]["weaknesses"]:
            multiplier[offensive_type] -= 2
    return max(multiplier.values())


def score_types(f_types, s_types, typechart):
    multiplier_first_on_second = best_damage_multiplier(f_types, s_types, typechart)
    multiplier_second_on_first = best_damage_multiplier(s_types, f_types, typechart)
    if multiplier_first_on_second - multiplier_second_on_first > 0:
        return 1
    if multiplier_first_on_second - multiplier_second_on_first < 0:
        return -1
    return 0


if __name__ == '__main__':

    with open("types.json", "r") as f:
        TYPECHART = json.load(f)
    ALL_TYPES = [val for val in TYPECHART]

    double_types = [{a, b} for a, b in itertools.product(ALL_TYPES, ALL_TYPES)]
    single_types = [{a} for a in ALL_TYPES]

    types_scoring = {set_to_tuple(double_type): 0 for double_type in double_types}
    for first_types, second_types in itertools.product(double_types, double_types):
        types_scoring[set_to_tuple(first_types)] = (
            types_scoring.get(set_to_tuple(first_types)) +
            score_types(first_types, second_types, TYPECHART)
        )
        types_scoring[set_to_tuple(second_types)] = (
            types_scoring.get(set_to_tuple(second_types)) +
            score_types(second_types, first_types, TYPECHART)
        )

    types_scoring_formatted = {
        "/".join([p for p in k]): v
        for k, v
        in sorted(types_scoring.items(), key=lambda x: x[1])
    }

    with open("result.json", "w") as f:
        json.dump(types_scoring_formatted, f, indent=4)

import itertools
import json
import logging

from elo import rate_1vs1
from random import shuffle

from utils import set_to_tuple

TYPECHART = json.load(open('types.json', 'r'))
ALL_TYPES = TYPECHART.keys()
BANLIST = [{"Normal"}]

logging.basicConfig(level=logging.INFO)


def best_damage_multiplier(offensive_types, defensive_types, typechart):
    multiplier = {offensive_type: 0 for offensive_type in offensive_types}
    for offensive_type, defensive_type in itertools.product(offensive_types, defensive_types):
        if offensive_type in typechart[defensive_type]["weaknesses"]:
            multiplier[offensive_type] += 1
        if offensive_type in typechart[defensive_type]["resistances"]:
            multiplier[offensive_type] -= 1
        if offensive_type in typechart[defensive_type]["immunities"]:
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


def iter_scoring(dic_scoring, typechart, max_iter=10):
    if max_iter == 0:
        return dic_scoring

    old_dic_scoring = dic_scoring.copy()
    matches = list(itertools.product(dic_scoring.keys(), dic_scoring.keys()))
    shuffle(matches)
    for first_types, second_types in matches:
        score = score_types(first_types, second_types, typechart)
        if score == 1:
            elo_shift = rate_1vs1(dic_scoring[first_types], dic_scoring[second_types])
            dic_scoring[first_types] = elo_shift[0]
            dic_scoring[second_types] = elo_shift[1]
        elif score == -1:
            elo_shift = rate_1vs1(dic_scoring[second_types], dic_scoring[first_types])
            dic_scoring[second_types] = elo_shift[0]
            dic_scoring[first_types] = elo_shift[1]

    max_diff = max([
        abs(dic_scoring[key] - old_dic_scoring[key])
        for key in dic_scoring
    ])

    logging.info(f"max difference observed : {max_diff}")
    logging.info(f"min/max elo : {min(dic_scoring.values())}/{max(dic_scoring.values())}")

    return iter_scoring(dic_scoring, TYPECHART, max_iter=max_iter - 1)


if __name__ == '__main__':

    double_types = [{a, b} for a, b in itertools.product(ALL_TYPES, ALL_TYPES) if {a, b} not in BANLIST]

    types_scoring = {set_to_tuple(double_type): 1000 for double_type in double_types}
    types_scoring = iter_scoring(types_scoring, TYPECHART, max_iter=900)

    types_scoring_formatted = {
        "/".join([p for p in k]): round(v)
        for k, v
        in sorted(types_scoring.items(), key=lambda x: x[1])
    }

    with open("result.json", "w") as f:
        json.dump(types_scoring_formatted, f, indent=4)

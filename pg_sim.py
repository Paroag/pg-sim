import itertools
import logging
from pprint import pprint

import matplotlib.pyplot as plt
from elo import rate_1vs1

from pgsim.evolution import get_child, mutated
from pgsim.iter_evolution import mutate_group
from pgsim.iter_scoring import iter_scoring
from pgsim.pokemon import AdvancedDoubleType
from pgsim.scoring import score
from resources import ALL_TYPES, COLORS

BANLIST = {"Normal"}
logging.basicConfig(level=logging.INFO)


def format_score(table_score, reverse=True):
    return {
        str(k): round(v)
        for k, v
        in sorted_score(table_score, reverse=reverse)
    }


def sorted_score(table_score, reverse=True):
    return {
        k: v
        for k, v
        in sorted(table_score.items(), key=lambda x: x[1], reverse=reverse)
    }


def count_types_occurence(type_scoring):
    dic = {type:0 for type in ALL_TYPES}
    for pokemon in type_scoring:
        types = pokemon.get_types()
        for type in types :
            dic[type]+=1
    return dic


if __name__ == '__main__':

    double_types = {
        AdvancedDoubleType(
            a,
            b,
            fast_move_type=a if a is not None else b,
            charge_move1_type=a if a is not None else b,
            charge_move2_type=b if b is not None else a,
        )
        for a, b in itertools.combinations(ALL_TYPES+[None], 2)
        if a != b
    }

    types_scoring = {double_type: 1000 for double_type in double_types}
    plot = {type: [] for type in ALL_TYPES}

    for generation_number in range(1, 100):
        print(f"Starting generation {generation_number}")

        types_scoring = iter_scoring(
            types_scoring,
            fight_function=score,
            update_score_function=rate_1vs1,
            max_iter=10,
        )
        types_scoring = sorted_score(types_scoring)

        new_group = mutate_group(
            list(types_scoring.keys()),
            mutation_function=mutated,
            reproduction_function=get_child,
            conservation=130,
            mutation=3,
            reproduction=38,
        )

        types_scoring = {a: 1000 for a in new_group}

        count = count_types_occurence(types_scoring)
        for type, c in count.items():
            plot[type].append(c)

fig, ax = plt.subplots()
for type, serie in plot.items() :
    ax.plot(serie, color=COLORS[type]["color"], label=type, marker = COLORS[type]["marker"])
leg = ax.legend(loc='upper left', frameon=False, ncol=3)
plt.show()
"""with open("result.json", "w") as f:
    json.dump(format_score(types_scoring), f, indent=4)"""

#TODO : Refacto stab dans scoring, lib pour evolution, hyperparameters twiking
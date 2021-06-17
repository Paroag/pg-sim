import itertools
import json
import logging

from elo import rate_1vs1

from pgsim.scoring import score
from pgsim.iter_scoring import iter_scoring
from resources import ALL_TYPES
from pgsim.pokemon import DoubleType, AdvancedDoubleType

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

    for generation_number in range(1, 5):
        print(f"Starting generation {generation_number}")

        types_scoring = {double_type: 1000 for double_type in double_types}
        types_scoring = iter_scoring(
            types_scoring,
            fight_function=score,
            update_score_function=rate_1vs1,
            max_iter=20,
        )
        types_scoring = sorted_score(types_scoring)

        ####### KEEPING TOP 70%
        top_type_scoring = {
            k: v
            for k,v
            in types_scoring.items()[:120]
        }
        ####### DESENDENCE WITH ALL
        child_type_scoring={

        }

        ####### SMALL VARIATION RANDOM
        ####### FULL RANDOM, ADD LEFT

    with open("result.json", "w") as f:
        json.dump(format_score(types_scoring), f, indent=4)

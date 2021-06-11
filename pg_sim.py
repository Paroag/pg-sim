import itertools
import json
import logging

from elo import rate_1vs1

from pgsim.scoring import score
from pgsim.iter_scoring import iter_scoring
from resources import ALL_TYPES
from pgsim.pokemon import DoubleType

BANLIST = {"Normal"}
logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':

    double_types = {
        DoubleType(a, b)
        for a, b in itertools.product(ALL_TYPES, ALL_TYPES)
        if {a, b} not in BANLIST and a != b
    }.union({
        DoubleType(a)
        for a in ALL_TYPES
        if a not in BANLIST
    })

    types_scoring = {double_type: 1000 for double_type in double_types}
    types_scoring = iter_scoring(
        types_scoring,
        fight_function=score,
        update_score_function=rate_1vs1,
        max_iter=15,
    )

    types_scoring_formatted = {
        str(k): round(v)
        for k, v
        in sorted(types_scoring.items(), key=lambda x: x[1])
    }

    with open("result.json", "w") as f:
        json.dump(types_scoring_formatted, f, indent=4)

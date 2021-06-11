from itertools import product


def iter_scoring(types_scoring, fight_function=None, update_score_function=None, max_iter=20):
    if max_iter == 0:
        return types_scoring
    matches = list(product(types_scoring.keys(), types_scoring.keys()))
    for first_types, second_types in matches:
        score = fight_function(first_types, second_types)
        if score == 1:
            types_scoring[first_types], types_scoring[second_types] = (
                update_score_function(types_scoring[first_types], types_scoring[second_types])
            )
        elif score == -1:
            types_scoring[second_types], types_scoring[first_types] = (
                update_score_function(types_scoring[second_types], types_scoring[first_types])
            )
    return iter_scoring(
        types_scoring,
        fight_function=fight_function,
        update_score_function=update_score_function,
        max_iter=max_iter-1
    )

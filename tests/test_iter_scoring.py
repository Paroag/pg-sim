from pgsim.iter_scoring import iter_scoring


def test_iter_scoring():

    initial_score = {
        "a": 10,
        "b": 10,
        "c": 10,
    }
    fight_function = str.__gt__

    def update_score_function(val1, val2):
        if val2 > 0:
            return val1+1, val2-1
        return val1, val2

    score = iter_scoring(
        initial_score,
        fight_function=fight_function,
        update_score_function=update_score_function,
        max_iter=2,
    )

    assert score == {
        "a": 6,
        "b": 10,
        "c": 14,
    }

from pgsim.evolution import get_child
from pgsim.pokemon import AdvancedDoubleType


ADVANCED_DOUBLE_TYPE1 = AdvancedDoubleType(
    "Water",
    "Ground",
    fast_move_type="Electric",
    charge_move1_type="Water",
    charge_move2_type="Grass",
)
ADVANCED_DOUBLE_TYPE2 = AdvancedDoubleType(
    "Ghost",
    "Dark",
    fast_move_type="Bug",
    charge_move1_type="Fairy",
    charge_move2_type="Fire",
)


def test_get_child():

    first_child = get_child(
        advanced_double_type1=ADVANCED_DOUBLE_TYPE1,
        advanced_double_type2=ADVANCED_DOUBLE_TYPE2,
    )

    assert first_child.get_types() in [
        {'Water'}, {'Ground'}, {'Ghost'}, {'Dark'},
        {'Water', 'Ground'}, {'Water', 'Ghost'}, {'Water', 'Dark'},
        {'Ground', 'Ghost'}, {'Ground', 'Dark'}, {'Ghost', 'Dark'}
    ]
    assert first_child.get_fast_move_type() in [
        {'Bug'}, {'Electric'}
    ]
    assert first_child.get_charge_move_types() in [
        {'Water', 'Grass'}, {'Water', 'Fairy'}, {'Water', 'Fire'},
        {'Grass', 'Fairy'}, {'Grass', 'Fire'}, {'Fairy', 'Fire'}
    ]

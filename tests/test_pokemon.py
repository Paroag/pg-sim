import pytest

from lib.pokemon import DoubleType, AdvancedDoubleType


def test_init():

    DoubleType("Water")
    DoubleType("Water", "Grass")

    with pytest.raises(ValueError):
        DoubleType("Iron")
    with pytest.raises(ValueError):
        DoubleType("Water", "Water")
    with pytest.raises(ValueError):
        DoubleType("Water", "Iron")

    AdvancedDoubleType(
        "Water",
        "Grass",
        fast_move_type="Grass",
        charge_move1_type="Water",
        charge_move2_type="Grass"
    )


def test_str():

    double_type1 = DoubleType("Water")
    double_type2 = DoubleType("Grass")
    double_type3 = DoubleType("Flying", "Rock")
    double_type4 = DoubleType("Ghost", "Fairy")

    assert str(double_type1) == "Water"
    assert str(double_type2) == "Grass"
    assert str(double_type3) == "Flying/Rock"
    assert str(double_type4) == "Ghost/Fairy"

    advanced_double_type1 = AdvancedDoubleType(
        "Fighting",
        "Flying",
        fast_move_type="Fighting",
        charge_move1_type="Fighting",
        charge_move2_type="Fighting"
    )

    assert(str(advanced_double_type1)) == "Fighting/Flying | Fighting | Fighting/Fighting"

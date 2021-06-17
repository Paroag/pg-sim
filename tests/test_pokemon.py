import pytest
import random

from pgsim.pokemon import DoubleType, AdvancedDoubleType


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

    assert(str(advanced_double_type1)) == "Fighting/Flying  | Fighting | Fighting/Fighting"


def test_eq():
    assert DoubleType("Water", "Ground") == DoubleType("Ground", "Water")
    assert DoubleType("Water", "Ground") != DoubleType("Water")

    advanced_double_type1 = AdvancedDoubleType(
        "Water",
        "Ground",
        fast_move_type="Water",
        charge_move1_type="Water",
        charge_move2_type="Grass",
    )
    advanced_double_type2 = AdvancedDoubleType(
        "Ground",
        "Water",
        fast_move_type="Water",
        charge_move1_type="Grass",
        charge_move2_type="Water",
    )
    advanced_double_type3 = AdvancedDoubleType(
        "Ground",
        "Water",
        fast_move_type="Water",
        charge_move1_type="Grass",
        charge_move2_type="Electric",
    )
    assert advanced_double_type1 == advanced_double_type2
    assert advanced_double_type1 != advanced_double_type3


def test_get_types():
    assert DoubleType("Water", "Ground").get_types() == {"Water", "Ground"}
    assert DoubleType("Water").get_types() == {"Water"}


def test_get_fast_move_type():
    advanced_double_type = AdvancedDoubleType(
        "Water",
        "Ground",
        fast_move_type="Water",
        charge_move1_type="Water",
        charge_move2_type="Grass",
    )
    assert advanced_double_type.get_fast_move_type() == {"Water"}


def test_get_charge_move_types():
    advanced_double_type = AdvancedDoubleType(
        "Water",
        "Ground",
        fast_move_type="Water",
        charge_move1_type="Water",
        charge_move2_type="Grass",
    )
    assert advanced_double_type.get_charge_move_types() == {"Water", "Grass"}


def test_mutate():
    random.seed(0)
    advanced_double_type = AdvancedDoubleType(
        "Water",
        "Ground",
        fast_move_type="Electric",
        charge_move1_type="Poison",
        charge_move2_type="Steel",
    )
    advanced_double_type_mutated = AdvancedDoubleType(
        "Water",
        "Ground",
        fast_move_type="Fighting",
        charge_move1_type="Poison",
        charge_move2_type="Steel",
    )
    advanced_double_type_mutated_twice = AdvancedDoubleType(
        "Water",
        "Normal",
        fast_move_type="Fighting",
        charge_move1_type="Poison",
        charge_move2_type="Steel",
    )
    advanced_double_type.mutate()
    assert advanced_double_type == advanced_double_type_mutated
    advanced_double_type.mutate()
    assert advanced_double_type == advanced_double_type_mutated_twice

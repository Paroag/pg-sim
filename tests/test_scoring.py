import pytest

from pgsim.scoring import best_damage_multiplier, score
from pgsim.pokemon import DoubleType


def test_best_damage_multiplier():
    assert best_damage_multiplier(["Water", "Ground"], ["Grass", "Flying"]) == pytest.approx(0.625)
    assert best_damage_multiplier(["Fire", "Electric"], ["Ground"]) == pytest.approx(1)
    assert best_damage_multiplier(["Grass", "Bug"], ["Dark", "Ghost"]) == pytest.approx(1)
    assert best_damage_multiplier(["Grass", "Water"], ["Water", "Electric"]) == pytest.approx(1.6)
    assert best_damage_multiplier(["Grass"], ["Water", "Electric"]) == pytest.approx(1.6)
    assert best_damage_multiplier(["Fighting", "Ice"], ["Ice", "Rock"]) == pytest.approx(2.56)
    assert best_damage_multiplier(["Fighting"], ["Fairy", "Steel"]) == pytest.approx(1)
    assert best_damage_multiplier(["Poison"], ["Ground", "Steel"]) == pytest.approx(0.244140625)


def test_score():
    assert score(DoubleType("Water", "Ground"), DoubleType("Grass", "Flying")) == -1
    assert score(DoubleType("Fire", "Electric"), DoubleType("Ground")) == -1
    assert score(DoubleType("Grass", "Bug"), DoubleType("Dark", "Ghost")) == 0
    assert score(DoubleType("Grass", "Water"), DoubleType("Water", "Electric")) == 1
    assert score(DoubleType("Grass"), DoubleType("Water", "Electric")) == 1
    assert score(DoubleType("Fighting", "Ice"), DoubleType("Ice", "Rock")) == 1
    assert score(DoubleType("Fighting"), DoubleType("Fairy", "Steel")) == -1

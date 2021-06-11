import pytest

from lib.scoring import best_damage_multiplier, score_types


def test_best_damage_multiplier():
    assert best_damage_multiplier(["Water", "Ground"], ["Grass", "Flying"]) == pytest.approx(0.625)
    assert best_damage_multiplier(["Fire", "Electric"], ["Ground"]) == pytest.approx(1)
    assert best_damage_multiplier(["Grass", "Bug"], ["Dark", "Ghost"]) == pytest.approx(1)
    assert best_damage_multiplier(["Grass", "Water"], ["Water", "Electric"]) == pytest.approx(1.6)
    assert best_damage_multiplier(["Grass"], ["Water", "Electric"]) == pytest.approx(1.6)
    assert best_damage_multiplier(["Fighting", "Ice"], ["Ice", "Rock"]) == pytest.approx(2.56)
    assert best_damage_multiplier(["Fighting"], ["Fairy", "Steel"]) == pytest.approx(1)
    assert best_damage_multiplier(["Poison"], ["Ground", "Steel"]) == pytest.approx(0.244140625)


def test_score_types():
    assert score_types(["Water", "Ground"], ["Grass", "Flying"]) == -1
    assert score_types(["Fire", "Electric"], ["Ground"]) == -1
    assert score_types(["Grass", "Bug"], ["Dark", "Ghost"]) == 0
    assert score_types(["Grass", "Water"], ["Water", "Electric"]) == 1
    assert score_types(["Grass"], ["Water", "Electric"]) == 1
    assert score_types(["Fighting", "Ice"], ["Ice", "Rock"]) == 1
    assert score_types(["Fighting"], ["Fairy", "Steel"]) == -1

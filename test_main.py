import json

from main import best_damage_multiplier, score_types

with open("types.json", "r") as f:
    TYPECHART = json.load(f)


def test_best_damage_multiplier():
    assert best_damage_multiplier(["Water", "Ground"], ["Grass", "Flying"], TYPECHART) == -1
    assert best_damage_multiplier(["Fire", "Electric"], ["Ground"], TYPECHART) == 0
    assert best_damage_multiplier(["Grass", "Bug"], ["Dark", "Ghost"], TYPECHART) == 0
    assert best_damage_multiplier(["Grass", "Water"], ["Water", "Electric"], TYPECHART) == 1
    assert best_damage_multiplier(["Grass"], ["Water", "Electric"], TYPECHART) == 1
    assert best_damage_multiplier(["Fighting", "Ice"], ["Ice", "Rock"], TYPECHART) == 2
    assert best_damage_multiplier(["Fighting"], ["Fairy", "Steel"], TYPECHART) == 0


def test_score_types():
    assert score_types(["Water", "Ground"], ["Grass", "Flying"], TYPECHART) == -1
    assert score_types(["Fire", "Electric"], ["Ground"], TYPECHART) == -1
    assert score_types(["Grass", "Bug"], ["Dark", "Ghost"], TYPECHART) == 0
    assert score_types(["Grass", "Water"], ["Water", "Electric"], TYPECHART) == 1
    assert score_types(["Grass"], ["Water", "Electric"], TYPECHART) == 1
    assert score_types(["Fighting", "Ice"], ["Ice", "Rock"], TYPECHART) == 1
    assert score_types(["Fighting"], ["Fairy", "Steel"], TYPECHART) == -1

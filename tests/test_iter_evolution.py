import random

from pgsim.evolution import get_child
from pgsim.evolution import mutated
from pgsim.iter_evolution import mutate_group
from pgsim.pokemon import AdvancedDoubleType


def test_mutate_group():
    random.seed(0)
    advanced_double_type1 = AdvancedDoubleType(
        "Ground",
        "Water",
        fast_move_type="Ground",
        charge_move1_type="Ground",
        charge_move2_type="Water",
    )
    advanced_double_type2 = AdvancedDoubleType(
        "Grass",
        "Electric",
        fast_move_type="Grass",
        charge_move1_type="Grass",
        charge_move2_type="Electric",
    )
    advanced_double_type3 = AdvancedDoubleType(
        "Ghost",
        "Dark",
        fast_move_type="Ghost",
        charge_move1_type="Ghost",
        charge_move2_type="Dark",
    )
    population_group = [advanced_double_type1, advanced_double_type2, advanced_double_type3]

    population_group1 = mutate_group(
        population_group,
        mutation_function=mutated,
        reproduction_function=get_child,
        conservation=2,
        mutation=1,
        reproduction=0,
    )
    assert len(population_group) == len(population_group1)
    assert population_group1[0] == population_group[0]
    assert population_group1[1] == population_group[1]
    assert population_group1[2] == AdvancedDoubleType(
        "Grass",
        "Electric",
        fast_move_type="Ghost",
        charge_move1_type="Grass",
        charge_move2_type="Electric",
    )

    population_group2 = mutate_group(
        population_group,
        mutation_function=mutated,
        reproduction_function=get_child,
        conservation=2,
        mutation=0,
        reproduction=1,
    )
    assert len(population_group) == len(population_group2)
    assert population_group2[0] == population_group[0]
    assert population_group2[1] == population_group[1]
    assert population_group2[2] != population_group[2]

import logging
import random


def iter_evolution():
    pass


def mutate_group(
        population_group,
        mutation_function=None,
        reproduction_function=None,
        conservation=0,
        mutation=0,
        reproduction=0,
):
    if conservation+mutation+reproduction != len(population_group):
        logging.warning(
            "sum of conservation, mutation and reproduction factor not equal to 1"
            ", population size may change"
        )

    top_population_group = population_group[:conservation]
    reproducted_population_group = (
        [
            reproduction_function(*random.sample(top_population_group, 2))
            for _
            in range(reproduction)
        ]
    )
    mutated_population_group = (
        [
            mutation_function(*random.sample(top_population_group, 1))
            for _
            in range(mutation)
        ]
    )

    return top_population_group+reproducted_population_group+mutated_population_group

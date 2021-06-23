import copy
import random

from pgsim.pokemon import AdvancedDoubleType


def get_child(advanced_double_type1: AdvancedDoubleType, advanced_double_type2: AdvancedDoubleType):

    parent_types = (
        list(advanced_double_type1.get_types())
        + list(advanced_double_type2.get_types())
    )
    parent_fast_move_types = (
        list(advanced_double_type1.get_fast_move_type())
        + list(advanced_double_type2.get_fast_move_type())
    )
    parent_charge_move_types = (
        list(advanced_double_type1.get_charge_move_types())
        + list(advanced_double_type2.get_charge_move_types())
    )

    type1, type2 = random.sample(parent_types, 2)
    type2 = type2 if type1 != type2 else None
    fast_move_type, = random.sample(parent_fast_move_types, 1)
    charge_move1_type, charge_move2_type = random.sample(parent_charge_move_types, 2)

    return AdvancedDoubleType(
        type1,
        type2,
        fast_move_type=fast_move_type,
        charge_move1_type=charge_move1_type,
        charge_move2_type=charge_move2_type,
    )


def mutated(advanced_double_type: AdvancedDoubleType):
    advanced_double_type_mutated = copy.deepcopy(advanced_double_type)
    advanced_double_type_mutated.mutate()
    return advanced_double_type_mutated

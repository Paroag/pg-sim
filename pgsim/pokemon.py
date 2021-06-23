import random

from resources import ALL_TYPES


class DoubleType:

    type1 = None
    type2 = None

    def __init__(self, type1, *args):
        if type1 not in ALL_TYPES:
            raise ValueError(f"type1 is not a valid type: {type1}")
        type2 = args[0] if args else None
        if type2 not in ALL_TYPES and type2 is not None:
            raise ValueError(f"type2 is not a valid type or None: {type2}")
        if type1 == type2:
            raise ValueError(f"type1 and type2 can not be both {type1}")
        self.type1 = type1
        self.type2 = type2

    def get_types(self):
        return {t for t in (self.type1, self.type2) if t is not None}

    def mutate(self, pickable_type=None):
        pickable_type = ALL_TYPES if pickable_type is None else pickable_type
        mutable_attributes = ["type"]
        attribute_to_mutate = random.choice(mutable_attributes)
        if attribute_to_mutate == "type":
            self._mutate_type(pickable_type=pickable_type)

    def _mutate_type(self, pickable_type=None):
        new_type = random.choice(pickable_type)
        num = random.randint(1, 2)
        setattr(self, f"type{num}", new_type)

    def __str__(self):
        return "/".join([t for t in (self.type1, self.type2) if t is not None])

    def __repr__(self):
        return self.__str__()

    def __eq__(self, double_type):
        return set(self.get_types()) == set(double_type.get_types())

    __hash__ = object.__hash__


class AdvancedDoubleType(DoubleType):

    fast_move_type = None
    charge_move1_type = None
    charge_move2_type = None

    def __init__(self, *args, **kwargs):
        if not isinstance(kwargs["fast_move_type"], str):
            raise ValueError(f"fast move type should be a string")
        if not isinstance(kwargs["charge_move1_type"], str) or not isinstance(kwargs["charge_move2_type"], str):
            raise ValueError(f"both charge move type should be strings")
        self.fast_move_type = kwargs.pop("fast_move_type")
        self.charge_move1_type = kwargs.pop("charge_move1_type")
        self.charge_move2_type = kwargs.pop("charge_move2_type")
        super().__init__(*args, **kwargs)

    def get_fast_move_type(self):
        return {self.fast_move_type}

    def get_charge_move_types(self):
        return {t for t in (self.charge_move1_type, self.charge_move2_type)}

    def mutate(self, pickable_type=None):
        pickable_type = ALL_TYPES if pickable_type is None else pickable_type
        mutable_attributes = ["type", "fast_move_type", "charge_move_type"]
        attribute_to_mutate = random.choice(mutable_attributes)
        if attribute_to_mutate == "type":
            self._mutate_type(pickable_type=pickable_type)
        if attribute_to_mutate == "fast_move_type":
            self._mutate_fast_move(pickable_type=pickable_type)
        if attribute_to_mutate == "charge_move_type":
            self._mutate_charge_move(pickable_type=pickable_type)

    def _mutate_fast_move(self, pickable_type=None):
        new_fast_move_type = random.choice(pickable_type)
        setattr(self, "fast_move_type", new_fast_move_type)

    def _mutate_charge_move(self, pickable_type=None):
        new_type = random.choice(pickable_type)
        num = random.randint(1, 2)
        setattr(self, f"charge_move{num}_type", new_type)

    def __str__(self):
        type_str = super().__str__()
        return (
            f"{type_str.ljust(17)}| "
            f"{self.fast_move_type.ljust(9)}| "
            f"{self.charge_move1_type}/{self.charge_move2_type}"
        )

    def __eq__(self, advanced_double_type):
        return (
            self.get_charge_move_types() == advanced_double_type.get_charge_move_types()
            and self.get_fast_move_type() == advanced_double_type.get_fast_move_type()
            and super().__eq__(advanced_double_type)
        )

    __hash__ = object.__hash__

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

    def __str__(self):
        return "/".join([t for t in (self.type1, self.type2) if t is not None])

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

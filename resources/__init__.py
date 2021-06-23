import json

from pathlib import Path

__location__ = Path(__file__)
TYPECHART = json.load(open(__location__.with_name('types.json'), 'r'))
ALL_TYPES = list(TYPECHART.keys())
COLORS = json.load(open(__location__.with_name('type_colors.json'), 'r'))

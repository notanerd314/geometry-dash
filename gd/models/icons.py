from dataclasses import dataclass
from .enums import *

@dataclass
class Icon:
    id: int
    gamemode: Gamemode

@dataclass
class Color:
    id: int
    part: ColorType
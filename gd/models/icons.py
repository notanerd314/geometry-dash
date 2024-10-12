from dataclasses import dataclass
from .enums import *

@dataclass
class Icon:
    """
    A **dataclass** representing the icon of a specific gamemode and ID.

    :param id: The ID of the icon.
    :type id: int
    :param gamemode: The gamemode type of the icon.
    :type gamemode: Gamemode
    """
    id: int
    gamemode: Gamemode

@dataclass
class Color:
    """
    A **dataclass** representing color ID of a specific part of the Icon.

    :param id: The ID of the color.
    :type id: int
    :param part: The part of the color.
    :type part: ColorType
    """
    id: int
    part: ColorType
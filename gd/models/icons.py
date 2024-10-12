"""
## .models.icons

The module containing all the classes and methods related to customization and icons.
"""

from dataclasses import dataclass
from .enums import *

@dataclass
class Icon:
    """
    A **dataclass** representing the icon of a specific gamemode and ID.

    Attributes
    ----------
    id : int
        The ID of the icon
    gamemode : Gamemode
        The gamemode of the icon
    """
    id: int
    gamemode: Gamemode

@dataclass
class Color:
    """
    A **dataclass** representing color ID of a specific part of the Icon.

    Attributes
    ----------
    id : int
        The ID of the color
    part : ColorType
        The part of the color
    """
    id: int
    part: ColorType
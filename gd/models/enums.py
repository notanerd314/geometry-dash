"""
# .models.enums

A module containing all enumerations of various things.
"""

from enum import IntEnum, Enum

# Enum
class Difficulty(Enum):
    """
    Enum representing the non-demon difficulty levels in Geometry Dash.
    """
    NA = 0
    EASY = 1
    NORMAL = 2
    HARD = 3
    HARDER = 4
    INSANE = 5
    DEMON = 6
    AUTO = 7

class DemonDifficulty(Enum):
    """
    Enum representing the demon difficulty levels in Geometry Dash.
    - EASY_DEMON (3): Easy Demon difficulty.
    - MEDIUM_DEMON (4): Medium Demon difficulty.
    - HARD_DEMON (0): Hard Demon difficulty.
    - INSANE_DEMON (5): Insane Demon difficulty.
    - EXTREME_DEMON (6): Extreme Demon difficulty.
    """
    HARD_DEMON = 0
    EASY_DEMON = 3
    MEDIUM_DEMON = 4
    INSANE_DEMON = 5
    EXTREME_DEMON = 6

class Length(IntEnum):
    """
    An **Enum** class representing the length of a Geometry Dash level.

    - `TINY` (0): Very short level.
    - `SHORT` (1): Short level.
    - `MEDIUM` (2): Medium length.
    - `LONG` (3): Long level.
    - `XL` (4): Extra long level.
    - `PLATFORMER` (5): Platformer level type.
    """
    
    TINY = 0
    SHORT = 1
    MEDIUM = 2
    LONG = 3
    XL = 4
    PLATFORMER = 5


class LevelRating(Enum):
    """
    An **Enum** class representing the rating of a Geometry Dash level.

    - `NO_RATE` (-2): No rating given.
    - `RATED` (-1): Rated level.
    - `FEATURED` (0): Featured level.
    - `EPIC` (1): Epic-rated level.
    - `MYTHIC` (2): Mythic-rated level.
    - `LEGENDARY` (3): Legendary-rated level.
    """
    
    NO_RATE = -2
    RATED = -1
    FEATURED = 0
    EPIC = 1
    MYTHIC = 2
    LEGENDARY = 3


class ModLevel(IntEnum):
    """
    An **Enum** class representing the moderator status of a Geometry Dash level.

    - `NONE` (0): No moderator status.
    - `MOD` (1): Moderator.
    - `ELDER_MOD` (2): Elder moderator.
    """
    
    NONE = 0
    MOD = 1
    ELDER_MOD = 2


class Gamemode(Enum):
    """
    An **Enum** class representing the different game modes in Geometry Dash.

    - `CUBE` (0): Cube mode.
    - `SHIP` (1): Ship mode.
    - `BALL` (2): Ball mode.
    - `UFO` (3): UFO mode.
    - `WAVE` (4): Wave mode.
    - `ROBOT` (5): Robot mode.
    - `SPIDER` (6): Spider mode.
    - `SWING` (7): Swingcopter mode.
    - `JETPACK` (8): Jetpack mode.
    """
    
    CUBE = 0
    SHIP = 1
    BALL = 2
    UFO = 3
    WAVE = 4
    ROBOT = 5
    SPIDER = 6
    SWING = 7
    JETPACK = 8


class ColorType(Enum):
    """
    An **Enum** class representing icon color parts in Geometry Dash.

    - `PRIMARY` (1): Primary color.
    - `SECONDARY` (2): Secondary color.
    - `GLOW` (3): Glow color.
    """
    
    PRIMARY = 1
    SECONDARY = 2
    GLOW = 3


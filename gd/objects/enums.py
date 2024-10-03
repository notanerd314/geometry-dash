from enum import Enum

# Enum

class Difficulty(Enum):
    """
    An **Enum** class representing the different difficulty levels in Geometry Dash.

    ### Difficulties:
        - `NA` (0): No difficulty assigned.
        - `EASY` (1): Easy level.
        - `NORMAL` (2): Normal level.
        - `HARD` (3): Hard level.
        - `HARDER` (4): Harder level.
        - `INSANE` (5): Insane level.
        - `EASY_DEMON` (6.3): Easy Demon difficulty.
        - `MEDIUM_DEMON` (6.4): Medium Demon difficulty.
        - `HARD_DEMON` (6.0): Hard Demon difficulty.
        - `INSANE_DEMON` (6.5): Insane Demon difficulty.
        - `EXTREME_DEMON` (6.6): Extreme Demon difficulty.
        - `AUTO` (7): Automatic level that plays itself.
    """

    NA = 0
    EASY = 1
    NORMAL = 2
    HARD = 3
    HARDER = 4
    INSANE = 5
    EASY_DEMON = 6.3
    MEDIUM_DEMON = 6.4
    HARD_DEMON = 6.0
    INSANE_DEMON = 6.5
    EXTREME_DEMON = 6.6
    AUTO = 7


class Length(Enum):
    """
    An **Enum** class representing the length of a Geometry Dash level.

    ### Lengths:
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

    ### Ratings:
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


class ModLevel(Enum):
    """
    An **Enum** class representing the moderator status of a Geometry Dash level.

    ### Moderator Levels:
        - `NONE` (0): No moderator status.
        - `MOD` (1): Moderated level.
        - `ELDER_MOD` (2): Elder moderator level.
        - `RUBRUB` (3): Robtop itself.
    """
    
    NONE = 0
    MOD = 1
    ELDER_MOD = 2
    RUBRUB = 3


class Gamemode(Enum):
    """
    An **Enum** class representing the different game modes in Geometry Dash.

    ### Gamemodes:
        - `CUBE` (1): Cube mode.
        - `SHIP` (2): Ship mode.
        - `BALL` (3): Ball mode.
        - `UFO` (4): UFO mode.
        - `WAVE` (5): Wave mode.
        - `ROBOT` (6): Robot mode.
        - `SPIDER` (7): Spider mode.
        - `SWING` (8): Swingcopter mode.
        - `JETPACK` (9): Jetpack mode.
    """
    
    CUBE = 1
    SHIP = 2
    BALL = 3
    UFO = 4
    WAVE = 5
    ROBOT = 6
    SPIDER = 7
    SWING = 8
    JETPACK = 9


class ColorType(Enum):
    """
    An **Enum** class representing color types in Geometry Dash.

    ### Color Types:
        - `primary` (1): Primary color.
        - `secondary` (2): Secondary color.
        - `glow` (3): Glow effect.
    """
    
    primary = 1
    secondary = 2
    glow = 3


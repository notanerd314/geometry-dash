from enum import Enum

# Enum

class Difficulty(Enum):
    """
    A **Enum** class representing the difficulties in Geometry Dash.

    ### Difficulties:
        `NA` (0): No difficulty
        `EASY` (1): Easy
        `NORMAL` (2): Normal
        `HARD` (3): Hard
        `HARDER` (4): Harder
        `INSANE` (5): Insane
        `EASY_DEMON` to `EXTREME_DEMON` (6.3 - 6.6): Demon Difficulties
        `AUTO` (7): Auto, plays itself.
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
    A class respresenting a level length from Tiny to XL.

    ### Lengths:
        TINY (0): Very short length
        SHORT (1): Short length
        MEDIUM (2): Medium length
        LONG (3): Long length
        XL (4): Very long length
        PLATFORMER (5): Platformer level
    """
    TINY = 0
    SHORT = 1
    MEDIUM = 2
    LONG = 3
    XL = 4
    PLATFORMER = 5

class LevelRating(Enum):
    """
    A class respresenting the rating of the level.
    """
    NO_RATE = -2
    RATED = -1
    FEATURED = 0
    EPIC = 1
    MYTHIC = 2
    LEGENDARY = 3

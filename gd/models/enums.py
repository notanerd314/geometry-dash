"""
# .models.enums

A module containing all enumerations of various things.
"""

from enum import IntEnum, Enum, StrEnum

# Enum
class Difficulty(Enum):
    """
    Enum representing the non-demon difficulty levels in Geometry Dash.
    """
    NA = 0
    """No difficulty."""
    EASY = 1
    """Easy difficulty."""
    NORMAL = 2
    """Normal difficulty."""
    HARD = 3
    """Hard difficulty."""
    HARDER = 4
    """Harder difficulty."""
    INSANE = 5
    """Insane difficulty."""
    DEMON = 6
    """Demon difficulty."""
    AUTO = 7
    """Auto difficulty."""

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
    """Hard demon."""
    EASY_DEMON = 3
    """Easy demon."""
    MEDIUM_DEMON = 4
    """Medium demon."""
    INSANE_DEMON = 5
    """Insane demon."""
    EXTREME_DEMON = 6
    """Extreme demon."""

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
    """Tiny length."""
    SHORT = 1
    """Short length."""
    MEDIUM = 2
    """Medium length."""
    LONG = 3
    """Long length."""
    XL = 4
    """Extra long length."""
    PLATFORMER = 5
    """Platformer level type."""


class LevelRating(Enum):
    """
    An **Enum** class representing the rating of a Geometry Dash level.

    - `NO_RATE` (-2): No rating given.
    - `RATED` (-1): Rated level.
    - `FEATURED` (0): Featured level.
    - `EPIC` (1): Epic-rated level.
    - `MYTHIC` (3): Mythic-rated level.
    - `LEGENDARY` (2): Legendary-rated level.
    """
    
    NO_RATE = -2
    """No rating specified."""
    RATED = -1
    """Rated but not featured."""
    FEATURED = 0
    """Featured level."""
    EPIC = 1
    """Epic level."""
    MYTHIC = 3
    """Mythic level."""
    LEGENDARY = 2
    """Legendary level."""


class ModRank(IntEnum):
    """
    An **Enum** class representing the moderator status of a Geometry Dash level.

    - `NONE` (0): No moderator status.
    - `MOD` (1): Moderator.
    - `ELDER_MOD` (2): Elder moderator.
    """
    
    NONE = 0
    """Not a moderator."""
    MOD = 1
    """Moderator."""
    ELDER_MOD = 2
    """Elder moderator."""


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
    """Primary icon color."""
    SECONDARY = 2
    """Secondary icon color."""
    GLOW = 3
    """Glow icon color."""

class SearchFilter(IntEnum):
    """
    An **Enum** class representing sorting options in Geometry Dash.
    """

    MOST_DOWNLOADED = 1
    """Sort to most downloaded."""
    MOST_LIKED = 2
    """Sort to most liked. (default)"""
    TRENDING = 3
    """Sort to trending."""
    RECENT = 4
    """Sort to recent."""
    FEATURED = 6
    """Sort to featured tab."""
    TOP_LISTS = 6
    """Sort top lists."""
    MAGIC = 7
    """Sort to magic."""
    AWARDED = 11
    """Sort to recently rated."""
    HALL_OF_FAME = 16
    """Hall of Fame."""
    GD_WORLD = 17
    """GD World."""
    DAILY = 21
    """Filter daily levels."""
    WEEKLY = 22
    """Filter weekly levels."""
    LIST_SENT = 27
    """Filter lists sent by moderators."""
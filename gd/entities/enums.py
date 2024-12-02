"""
# .entities.enums

A module containing all enumerations of various things.
"""

from enum import IntEnum, Enum, StrEnum, auto
from typing import Literal, Union

# Literals
SpecialLevel = Literal["DAILY", "WEEKLY", "EVENT"]
ChestType = Literal["SMALL", "LARGE"]


# Enum
class Difficulty(Enum):
    """
    Represents the non-demon difficulty levels.
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
    Represents the demon difficulty levels.
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
    Represents the length of a level.
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
    Represents the rating of a level.
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
    Represents the moderator status of a level.
    """

    NONE = 0
    """Not a moderator."""
    MOD = 1
    """Moderator."""
    ELDER_MOD = 2
    """Elder moderator."""


class Gamemode(Enum):
    """
    Represents the different gamemodes.
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


class SearchFilter(IntEnum):
    """
    Represents search options.
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
    LIST_OF_LEVELS = 10
    """Get the display information for levels. (Seperated by a comma)"""
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
    EVENT = 23
    """Filter event levels."""
    LIST_SENT = 27
    """Filter lists sent by moderators."""
    FRIENDS = 13
    """Filter levels made by friends. (Login required)"""

    DEFAULT = MOST_DOWNLOADED


class Leaderboard(StrEnum):
    """
    Represents the leaderboard types.
    """

    TOP = auto()
    """Gets the top 100 in the global leaderboard."""
    RELATIVE = auto()
    """Gets the surrounding leaderboard of your rank."""
    FRIENDS = auto()
    """Gets the leaderboard of your friends."""
    CREATORS = auto()
    """Gets the leaderboard of creators."""

    DEFAULT = TOP


class Item(Enum):
    """
    Represents items/collectables.
    """

    DIAMOND = 1
    ORBS = 2
    STARS = 3
    MOONS = 4
    USERCOIN = 5
    SHARDS = 6
    DEMON_KEY = 7

    @staticmethod
    def from_extra_id(item_id: int) -> Union["Item.DEMON_KEY", "Shard", None]:
        """
        Returns the corresponding `Item` or `Shard` from the given `item_id` in the chest response.

        :param item_id: The `item_id` returned from the chest response.
        :type item_id: int
        :return: The corresponding `Item` or `Shard`.
        :rtype: Union["Item.DEMON_KEY", "Shard", None]
        """
        if item_id == 0:
            return None
        if item_id == 5:
            return Item.DEMON_KEY

        return Shard(item_id)


class Shard(Enum):
    """
    Represents shards.
    """

    FIRE = 1
    ICE = 2
    POISON = 3
    SHADOW = 4
    LAVA = 5
    EARTH = 10
    BLOOD = 11
    METAL = 12
    LIGHT = 13
    SOUL = 14

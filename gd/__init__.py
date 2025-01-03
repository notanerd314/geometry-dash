"""
Access the Geometry Dash API programmatically.
"""

__title__: str = "gdapi"
__author__: str = "notanerd"
__license__: str = "MIT"
__copyright__: str = "Copyright 2024 notanerd"
__version__: str = "0.1.0"

__description__ = "An API wrapper for Geometry Dash."
__url__ = "https://github.com/notanerd314/geometry"

from collections import namedtuple

from gd.client import SECRET, LOGIN_SECRET, MODERATOR_SECRET, Client
from gd.errors import (
    LoadError,
    InvalidID,
    LoginError,
    NoPremission,
)
from gd.cryptography import (
    Salt,
    XorKey,
    gjp2,
    generate_chk,
    cyclic_xor,
    singular_xor,
    generate_udid,
    decrypt_gamesave,
)
from gd.entities.enums import (
    Length,
    LevelRating,
    SearchFilter,
    DemonDifficulty,
    Difficulty,
    SpecialLevel,
    ChestType,
    Leaderboard,
    ModRank,
    Gamemode,
    Item,
    OfficialSong,
)
from gd.entities.level import Level, LevelDisplay, Comment, MapPack, LevelList, Gauntlet
from gd.entities.song import (
    MusicLibrary,
    SoundEffectLibrary,
    Song,
    SoundEffect,
)
from gd.entities.user import Account, Player, AccountComment, Quest, Chest
from gd.entities.cosmetics import Icon, IconSet, colors

__all__ = [
    # Main client
    "Client",
    # Exceptions
    "LoadError",
    "InvalidID",
    "LoginError",
    "NoPremission",
    # Enums
    "Length",
    "LevelRating",
    "SearchFilter",
    "DemonDifficulty",
    "Difficulty",
    "SpecialLevel",
    "ChestType",
    "Leaderboard",
    "ModRank",
    "Gamemode",
    "Item",
    "OfficialSong",
    # Entities - Levels
    "Level",
    "LevelDisplay",
    "Comment",
    "MapPack",
    "LevelList",
    "Gauntlet",
    # Entities - Songs
    "MusicLibrary",
    "SoundEffectLibrary",
    "Song",
    "SoundEffect",
    # Entities - Users
    "Account",
    "Player",
    "AccountComment",
    "Quest",
    "Chest",
    # Entities - Cosmetics
    "Icon",
    "IconSet",
    # Constants
    "SECRET",
    "LOGIN_SECRET",
    "MODERATOR_SECRET",
    "colors",
    # Cryptography
    "gjp2",
    "generate_chk",
    "Salt",
    "XorKey",
    "cyclic_xor",
    "singular_xor",
    "generate_udid",
    "decrypt_gamesave",
]

VersionInfo: namedtuple = namedtuple("VersionInfo", "major minor micro")

version_info: tuple[int] = VersionInfo(major=0, minor=1, micro=0)

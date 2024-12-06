"""
# `gdapi`

Access the Geometry Dash API programmatically.

# Usage
### Downloading a level:
```py
>>> from gd import Client
>>> client = Client()
>>> level = await client.download_level(13519)
>>> level.name
"The Nightmare"
>>> level.difficulty
<DemonDifficulty.EASY_DEMON: 3>
>>> level.description
"Hard map by Jax. 7813"
>>> level.official_song
<OfficialSong.POLARGEIST: 2>
```

### Fetching a song and downloading it:
```py
>>> from gd import Client
>>> client = Client()
>>> song = await client.get_song(1)
>>> song.name
"Chilled 1"
>>> song.size
0.07
>>> song.link
"http://audio.ngfiles.com/0/1_newgrounds_consin.mp3"
>>> await song.download_to("chilled.mp3") # Download the song in the relative path
```

### Getting the Music Library:
```py
>>> from gd import Client
>>> client = Client()
>>> library = await client.music_library()
>>> library.version
127
>>> library.artists
{10002716: Artist(id=10002716, name='Raul Ojamaa', website=None, youtube_channel_id=None),
 10002717: Artist(id=10002717, name='Malou', website=None, youtube_channel_id=None), ...}
>>> library.tags
{234: '8bit', 251: 'action', 239: 'ambiance', 246: 'ambient', 247: 'battle', ...}
```

### Login and comment:
```py
>>> from gd import Client
>>> client = Client()
>>> credientals = await client.login("notanerd1", "****") # Password is hidden for security
>>> credientals
Account(account_id=24514763, player_id=218839712, name='notanerd1', password=****)
>>> comment_id = await client.comment("I am high", level_id=111663149, percentage=0)
2994273
```
"""

__title__: str = "gdapi"
__author__: str = "notanerd"
__license__: str = "MIT"
__copyright__: str = "Copyright 2024 notanerd"
__version__: str = "0.1.0"

__description__ = "API wrapper for Geometry Dash written in Python 3."
__url__ = "https://github.com/notanerd314/gdapi"

from collections import namedtuple

import gd.thirdparty
from gd.client import SECRET, LOGIN_SECRET, Client
from gd.exceptions import (
    LoadError,
    InvalidID,
    LoginError,
    NoPremission,
    OnCooldown,
)
from gd.cryptography import (
    Salt,
    XorKey,
    gjp2,
    generate_chk,
    cyclic_xor,
    singular_xor,
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
from gd.entities.cosmetics import Icon, IconSet, COLORS_LIST

__all__ = [
    # Main client
    "Client",
    # Exceptions
    "LoadError",
    "InvalidID",
    "LoginError",
    "NoPremission",
    "OnCooldown",
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
    "COLORS_LIST",
    # Cryptography
    "gjp2",
    "generate_chk",
    "Salt",
    "XorKey",
    "cyclic_xor",
    "singular_xor",
    # Thirdparty
    "thirdparty",
]

VersionInfo: namedtuple = namedtuple("VersionInfo", "major minor micro")

version_info: tuple[int] = VersionInfo(major=0, minor=1, micro=0)

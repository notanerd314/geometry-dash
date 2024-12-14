__doc__ = """
# gd.type_hints

A module containing user type hints for the module.
"""

from typing import Union

PlayerId = Union[int, str]
"""Type hint for Player ID."""

AccountId = Union[int, str]
"""Type hint for Account ID."""

LevelId = Union[int, str]
"""Type hint for Level ID."""

LevelOrListId = Union[int, str]
"""Type hint for Level or List ID. (List ID is negative)"""

ListId = Union[int, str]
"""Type hint for List ID."""

AccountCommentId = Union[int, str]
"""Type hint for Post ID."""

CommentId = Union[int, str]
"""Type hint for Comment ID."""

SongId = Union[int, str]
"""Type hint for Song ID."""

ArtistId = Union[int, str]
"""Type hint for Artist ID."""

MusicLibrarySongId = Union[int, str]
"""Type hint for Music Library Song ID."""

MusicLibraryArtistId = Union[int, str]
"""Type hint for Music Library Artist ID."""

SoundEffectFolderId = Union[int, str]
"""Type hint for Sound Effect Folder ID."""

SoundEffectId = Union[int, str]
"""Type hint for Sound Effect ID."""

ColorHex = int
"""Type hint for Color Hex."""

ColorId = int
"""Type hint for Color Id."""

IconId = int
"""Type hint for Icon Id."""

Udid = str
"""Universally Unique Identifier"""

SongFileHubId = str
"""Type hint for a Song File Hub Id."""

IconTrailId = int
IconShipTrailId = int
IconDeathEffectId = int

LeaderboardPercentage = int
LeaderboardPoints = int
LeaderboardTime = int

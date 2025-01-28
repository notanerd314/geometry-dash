__doc__ = """
# gd.type_hints

A module containing user type hints for the module.
"""

from typing import Any

PlayerId = int
"""Type hint for Player ID."""

AccountId = int
"""Type hint for Account ID."""

LevelId = int
"""Type hint for Level ID."""

LevelOrListId = int
"""Type hint for Level or List ID. (List ID is negative)"""

ListId = int
"""Type hint for List ID."""

AccountCommentId = int
"""Type hint for Post ID."""

CommentId = int
"""Type hint for Comment ID."""

CustomSongId = int
"""Type hint for Song ID."""

ArtistId = int
"""Type hint for Song Artist ID."""

MusicLibrarySongId = int
"""Type hint for Music Library Song ID."""

MusicLibraryArtistId = int
"""Type hint for Music Library Artist ID."""

SoundEffectFolderId = int
"""Type hint for Sound Effect Folder ID."""

SoundEffectId = int
"""Type hint for Sound Effect ID."""

ColorHex = int
"""Type hint for Color Hex."""

ColorId = int
"""Type hint for Color Id."""

IconId = int
"""Type hint for Icon Id."""

Udid = str
"""Universally Unique Identifier."""

SongFileHubId = str
"""Type hint for a Song File Hub ID."""

IconTrailId = int
"""Icon trail ID."""

IconShipTrailId = int
"""Icon ship trail ID."""

IconDeathEffectId = int
"""Icon death effect ID."""

LeaderboardValue = Any
"""Leaderboard time, percentage or points."""

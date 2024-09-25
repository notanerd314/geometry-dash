from ..ext import *
from .enums import *
from typing import *
from urllib.parse import unquote

# Level

class Level:
    """
    **A class representation of a Geometry Dash level.**

    **Parameters:**
    - raw_str - *(required)* The response from the server, not decrypted yet.
    """
    def __init__(self, raw_str: str):
        if not isinstance(raw_str, str):
            raise ValueError("Level string must be a str!")
            
        self.raw = raw_str
        try:
            self.parsed = parse_level_data(self.raw)
        except Exception as e:
            raise RuntimeError(f"Failed to parse level string: {e}. Maybe you made a mistake?")
        
        # Level Properties
        self.ID: int = self.parsed.get("1", None)
        self.NAME: str = self.parsed.get("2", None)
        self.DESCRIPTION: str = self.parsed.get("3", None)
        self.LEVEL_DATA: str = self.parsed.get("4", None)
        self.VERSION: int = self.parsed.get("5", None)
        self.CREATOR_ID: int = self.parsed.get("6", None)
        self.DOWNLOADS: int = self.parsed.get("10", 0)
        self.LIKES: int = self.parsed.get("14")
        self.COPYABLE: bool = True if self.parsed.get("27") else False
        self.LENGTH: Length = Length(self.parsed.get("15"))
        self.REQUESTED_STARS: int = self.parsed.get('39', None)
        self.STARS: int = self.parsed.get("18", None)
        self.COINS: int = self.parsed.get("37", 0)

        try: self.SONG_LIST: list[int] = self.parsed.get("52", "").split(",") 
        except AttributeError: self.SONG_LIST: int = self.parsed.get("52", None)

        try: self.SFX_LIST: list[int] = self.parsed.get("53", "").split(",")
        except AttributeError: self.SFX_LIST: int = self.parsed.get("53", None)

        self.DAILY_ID: int = self.parsed.get("41", -1)
        self.COPIED_LEVEL_ID: int = self.parsed.get("30", None)

        # Booleans
        self.LOW_DETAIL_MODE: bool = True if self.parsed.get("40", None) else False
        self.TWO_PLAYER: bool = True if self.parsed.get("31", None) else False
        self.VERIFIED_COINS: bool = True if self.parsed.get("38", None) else False
        self.IN_GUANTLET: bool = True if self.parsed.get("44", None) else False
        self.DAILY: bool = True if 0 <= self.DAILY_ID <= 100000 else False
        self.WEEKLY: bool = True if self.DAILY_ID >= 100000 else False

        if self.parsed.get("42", 0) >= 1:
            self.RATING: LevelRating = LevelRating(self.parsed.get("42"))
        elif self.parsed.get("19", 0) >= 1:
            self.RATING: LevelRating = LevelRating.FEATURED
        elif self.STARS != 0:
            self.RATING: LevelRating = LevelRating.RATED
        else:
            self.RATING: LevelRating = LevelRating.NO_RATE

        # Difficulty
        if self.parsed.get("17"):
            self.DIFFICULTY: LevelRating = Difficulty(6 + self.parsed.get("43") / 10)
        elif self.parsed.get("25"):
            self.DIFFICULTY: LevelRating = Difficulty.AUTO
        else:
            self.DIFFICULTY: LevelRating = Difficulty(self.parsed.get("9") / 10)

        #! SECRETS!
        self.LEVEL_PASSWORD = self.parsed.get("27") if not isinstance(self.parsed.get("27"), bool) else None

class Song:
    """
    The class representation of a Newgroundssong.

    Parameters:
        - raw_str - *(required)* The song string object from the servers.
    """

    def __init__(self, raw_str: str) -> None:
        self.raw = raw_str
        self.parsed = parse_song_data(self.raw)

        self.NEWGROUNDS_ID: int = self.parsed.get('1', None)
        self.NAME: str = self.parsed.get('2', None)
        self.ARTIST_ID: int = self.parsed.get('3', None)
        self.ARTIST_NAME: str = self.parsed.get('4', None)
        self.ARTIST_VERIFIED: bool = True if self.parsed.get('8', None) == 1 else False

        self.SONG_SIZE_MB: float = float(self.parsed.get('5', 0.0))
        self.YOUTUBE_LINK: str = f"https://youtu.be/watch?v={self.parsed["7"]}" if self.parsed.get("7", None) is not None else None
        self.NEWGROUNDS_LINK: str = unquote(self.parsed["10"]) if self.parsed.get("10", None) else None

class SearchedLevel(Level):
    """
    The class representation of the level search result.

    Parameters:
        - raw_str - *(required)* The response from the server.
    """

    def __init__(self, parsed_str: dict):
        super().__init__(parsed_str["level"])

        self.CREATOR_NAME = parsed_str["creator"]["playerName"]
        self.SONG_DATA = Song(parsed_str["song"])
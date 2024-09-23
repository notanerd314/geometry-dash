from ..ext import *
from .enums import *

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
        # print(self.raw)
        self.parsed = parse(self.raw)
        
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
        self.LENGTH = Length(self.parsed.get("15"))
        self.REQUESTED_STARS: int = self.parsed.get('39', None)
        self.STARS: int = self.parsed.get("18", None)
        self.COINS: int = self.parsed.get("37", 0)
        self.SONG_LIST: list[int] = self.parsed.get("52", "").split(",")
        self.SFX_LIST: list[int] = self.parsed.get("53", "").split(",")
        self.DAILY_ID: int = self.parsed.get("41", -1)
        self.COPIED_LEVEL_ID: int = self.parsed.get("30", None)

        # Booleans
        self.LOW_DETAIL: bool = True if self.parsed.get("40", None) else False
        self.TWO_PLAYER: bool = True if self.parsed.get("31", None) else False
        self.VERIFIED_COINS: bool = True if self.parsed.get("38", None) else False
        self.IN_GUANTLET: bool = True if self.parsed.get("44", None) else False
        self.DAILY: bool = True if 0 <= self.DAILY_ID <= 100000 else False
        self.WEEKLY: bool = True if self.DAILY_ID >= 100000 else False

        if self.parsed.get("42", 0) >= 1:
            self.RATING = LevelRating(self.parsed.get("42"))
        elif self.parsed.get("19", 0) >= 1:
            self.RATING = LevelRating.FEATURED
        elif self.STARS != 0:
            self.RATING = LevelRating.RATED
        else:
            self.RATING = LevelRating.NO_RATE

        # Difficulty
        if self.parsed.get("17"):
            self.DIFFICULTY = Difficulty(6 + self.parsed.get("43") / 10)
        elif self.parsed.get("25"):
            self.DIFFICULTY = Difficulty.AUTO
        else:
            self.DIFFICULTY = Difficulty(self.parsed.get("9") / 10)

        #! SECRETS!
        self.LEVEL_PASSWORD = self.parsed.get("27") if not isinstance(self.parsed.get("27"), bool) else None

from ..ext import *
from .enums import *
from typing import List, Optional
from .song import *


class DownloadedLevel:
    """
    A class representation of a Geometry Dash level.

    Parameters:
    - raw_str (str): The response from the server, not decrypted yet.
    - searched_level_data (dict, optional): Data for the song object and the creator's name.
    """

    def __init__(self, raw_str: str, searched_level_data: dict = None) -> None:
        if not isinstance(raw_str, str):
            raise ValueError("Level string must be a str!")

        self.raw = raw_str
        try:
            self.parsed = parse_level_data(self.raw)
        except Exception as e:
            raise RuntimeError(f"Failed to parse level string: {e}. Please check the input format.")

        # Level Properties
        self.id: Optional[int] = self.parsed.get("1")
        self.name: Optional[str] = self.parsed.get("2")
        self.description: Optional[str] = self.parsed.get("3")
        self.level_data: Optional[str] = self.parsed.get("4")
        self.version: Optional[int] = self.parsed.get("5")
        self.creator_id: Optional[int] = self.parsed.get("6")
        self.downloads: int = self.parsed.get("10", 0)
        self.likes: Optional[int] = self.parsed.get("14")
        self.copyable: bool = bool(self.parsed.get("27"))
        self.length: Length = Length(self.parsed.get("15"))
        self.requested_stars: Optional[int] = self.parsed.get("39")
        self.stars: Optional[int] = self.parsed.get("18")
        self.coins: int = self.parsed.get("37", 0)
        
        self.custom_song_id: int = self.parsed.get("35", None)
        self.song_list_ids: List[int] = self._parse_comma_separated_int_list("52")
        self.sfx_list_ids: List[int] = self._parse_comma_separated_int_list("53")

        self.daily_id: int = self.parsed.get("41", -1)
        self.copied_level_id: Optional[int] = self.parsed.get("30")

        # Boolean flags
        self.low_detail_mode: bool = bool(self.parsed.get("40"))
        self.two_player_mode: bool = bool(self.parsed.get("31"))
        self.verified_coins: bool = bool(self.parsed.get("38"))
        self.in_gauntlet: bool = bool(self.parsed.get("44"))
        self.daily: bool = 0 <= self.daily_id <= 100000
        self.weekly: bool = self.daily_id >= 100000

        # Rating
        self.rating: LevelRating = self._determine_rating()

        # Difficulty
        self.difficulty: Difficulty = self._determine_difficulty()

        # Level Password
        self.level_password: Optional[str] = None if isinstance(self.parsed.get("27"), bool) else self.parsed.get("27")

    def _parse_comma_separated_int_list(self, key: str) -> List[int]:
        """Helper method to parse a comma-separated list of integers."""
        try:
            return [int(x) for x in self.parsed.get(key, "").split(",") if x.isdigit()]
        except AttributeError:
            return []

    def _determine_rating(self) -> LevelRating:
        """Determines the level rating."""
        if self.parsed.get("42", 0) >= 1:
            return LevelRating(self.parsed.get("42"))
        elif self.parsed.get("19", 0) >= 1:
            return LevelRating.FEATURED
        elif self.stars != 0:
            return LevelRating.RATED
        return LevelRating.NO_RATE

    def _determine_difficulty(self) -> Difficulty:
        """Determines the level difficulty."""
        if self.parsed.get("17"):
            return Difficulty(6 + self.parsed.get("43", 0) / 10)
        elif self.parsed.get("25"):
            return Difficulty.AUTO
        return Difficulty(self.parsed.get("9", 0) / 10)


    async def load_song_data(self) -> Union[NewgroundsSong, MusicLibrary.Song]:
        """Loads the song data for this level."""
        if is_newgrounds_song(self.custom_song_id):
            response = await send_post_request(
                url="http://boomlings.com/database/getGJSongInfo.php",
                data={'secret': self.secret, "songID": self.custom_song_id}  # Corrected 'id' to 'self.custom_song_id'
            )
            self.custom_song_data = response
        else:
            response = await send_get_request(
                url="https://geometrydashfiles.b-cdn.net/music/musiclibrary_02.dat",
            )
            if response.status_code == 200:  # Check if the request was successful
                music_library_encoded = response.content
                music_library = MusicLibrary(decrypt_data(music_library_encoded, "base64_decompress"))
                self.custom_song_data = music_library.songs.get(str(self.custom_song_id))  # Use .get() for safety
            else:
                raise RuntimeError(f"Failed to load music library, status code: {response.status_code}")
        
        return self.custom_song_dataa
        

class SearchedLevel(DownloadedLevel):
    """
    The class representation of a level search result.

    Parameters:
    - parsed_str (dict): The parsed response data from the server.
    """

    def __init__(self, parsed_str: dict):
        super().__init__(parsed_str["level"])

        self.creator_name: Optional[str] = parsed_str["creator"]["playerName"]
        self.song_data: NewgroundsSong = NewgroundsSong(parsed_str["song"])

    async def download_level(self) -> Union[DownloadedLevel, None]:
        """
        Downloads the level using the current level ID of the class.
        """
        try:
            response = await send_post_request(
                url="http://www.boomlings.com/database/downloadGJLevel22.php",
                data={"levelID": self.id, "secret": self.secret}
            )
            return DownloadedLevel(raw_str=response, searched_level_data=self.song_data)
        except Exception as e:
            raise RuntimeError(f"Could not download level, {e}")

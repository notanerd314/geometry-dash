from .ext import *
from .objects.level import *
from .objects.song import *
from .objects.users import *
from datetime import timedelta
from typing import Union, Tuple

_secret = "Wmfd2893gb7"

class GeometryDash:
    def __init__(self, secret: str = _secret) -> None:
        self.secret = secret

    async def download_level(self, id: int, ng_song_data: bool = False) -> DownloadedLevel:
        """Downloads a specific level from the Geometry Dash servers using the provided ID."""
        if not isinstance(id, int):
            raise ValueError("ID must be an int.")

        try:
            response = await send_post_request(
                url="http://www.boomlings.com/database/downloadGJLevel22.php", 
                data={"levelID": id, "secret": self.secret}
            )
            return DownloadedLevel.from_raw(response)
        except RuntimeError as e:
            raise RuntimeError(f"Failed to download level: {e}")

    async def get_daily_level(self, weekly: bool = False, get_time_left: bool = False) -> Union[DownloadedLevel, Tuple[DownloadedLevel, timedelta]]:
        """Downloads the daily or weekly level from the Geometry Dash servers."""
        try:
            level = await self.download_level(-2 if weekly else -1)
            
            if get_time_left:
                daily_data: str = await send_post_request(
                    url="http://www.boomlings.com/database/getGJDailyLevel.php", 
                    data={"secret": self.secret, "weekly": "1" if weekly else "0"}
                )
                daily_data = daily_data.split("|")
                return level, timedelta(seconds=int(daily_data[1]))
            
            return level
        except RuntimeError as e:
            raise RuntimeError(f"Failed to get daily level: {e}")

    async def search_level(self, query: str) -> List[SearchedLevel]:
        """Searches for levels matching the given query string."""
        search_data: str = await send_post_request(
            url="http://www.boomlings.com/database/getGJLevels21.php", 
            data={"secret": self.secret, "str": query, "type": 0}
        )
        
        parsed_results = parse_search_results(search_data)
        return [SearchedLevel.from_raw(result) for result in parsed_results]

    async def get_music_library(self) -> MusicLibrary:
        """Gets the current music library in RobTop's servers."""
        response = await send_get_request(
            url="https://geometrydashfiles.b-cdn.net/music/musiclibrary_02.dat",
        )
        music_library_encoded = response.content
        music_library = decrypt_data(music_library_encoded, "base64_decompress")
        return MusicLibrary.from_raw(music_library)
    
    async def get_sfx_library(self) -> SFXLibrary:
        """Gets the current SFX library in RobTop's servers"""
        response = await send_get_request(
            url="https://geometrydashfiles.b-cdn.net/sfx/sfxlibrary.dat",
        )
        music_library_encoded = response.content
        music_library = decrypt_data(music_library_encoded, "base64_decompress")
        return SFXLibrary.from_raw(music_library)

    async def get_song_data(self, id: int) -> Union[LevelSong, MusicLibrarySong]:
        """Gets song data by ID, either from Newgrounds or the music library."""
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJSongInfo.php",
            data={'secret': self.secret, "songID": id}
        )
        return LevelSong.from_raw(response)

    async def get_user_profile(self, account_id: int) -> UserProfile:
        """Get user profile by account ID."""
        if isinstance(account_id, int):
            url = "http://www.boomlings.com/database/getGJUserInfo20.php"
            data = {'secret': self.secret, "targetAccountID": account_id}
        else:
            raise ValueError("ID must be int")

        response = await send_post_request(url=url, data=data)
        return UserProfile.from_raw(response)

    async def search_user(self, username: str) -> UserProfile:
        """Search for a user by their username. Note that this doesn't return the full information."""
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJUsers20.php",
            data={'secret': self.secret, "str": username}
        )
        return UserProfile.from_raw(response)

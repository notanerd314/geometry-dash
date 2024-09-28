from .ext import *
from .objects.level import *
from .objects.song import *
from datetime import timedelta
from typing import Tuple

_secret = "Wmfd2893gb7"

class GeometryDash:
    def __init__(self, secret: str = "") -> None:
        self.secret = secret

    async def download_level(self, id: int, ng_song_data: bool = False) -> DownloadedLevel:
        """
        Downloads a specific level from the Geometry Dash servers using the provided ID.

        Parameters:
            id (int, required): The ID of the level to download.
            ng_son_data (bool, optional): Also fetches the data of the song the level used.
        """

        if not isinstance(id, int):
            raise ValueError("ID must be an int.")

        # try:
        #     response = await send_post_request(
        #         url="http://www.boomlings.com/database/downloadGJLevel.php",
        #         data={"levelID": id, "includesNGSong": "1" if includes_ng_song else "0", "secret": self.secret}
        #     )
        #     return DownloadedLevel(response)

        try:
            response = await send_post_request(
                url="http://www.boomlings.com/database/downloadGJLevel22.php", 
                data={"levelID": id, "secret": self.secret}
            )
            return DownloadedLevel(response)
        except Exception as e:
            raise RuntimeError(f"Failed to download level: {e}")

    async def get_daily_level(self, weekly: bool = False, get_time_left: bool = False) -> DownloadedLevel | Tuple[DownloadedLevel, timedelta]:
        """
        Downloads the daily/weekly level from the Geometry Dash servers with the time left for it.

        Parameters:
            weekly (int, optional): Put `True` to get the weekly level, otherwise daily.
            get_time_left (bool, optional): If `True`, the method will also return the time left in timedelta inside a tuple with the `Level` object. Defaults to `False`.
        """

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
        except Exception as e:
            raise RuntimeError(f"Failed to get daily level: {e}")

    async def search_level(self, query: str):
        search_data: str = await send_post_request(
            url="http://www.boomlings.com/database/getGJLevels21.php", 
            data={"secret": self.secret, "str": query, "type": 0}
        )
        
        search_data = parse_search_results(search_data)
        for search in search_data:
            search_data[search_data.index(search)] = SearchedLevel(search)

        return search_data

    async def get_music_library(self) -> MusicLibrary:
        """
        Gets the current music library in RobTop's servers.
        """
        response = await send_get_request(
            url="https://geometrydashfiles.b-cdn.net/music/musiclibrary_02.dat",
        )
        # print(response.content)
        music_library_encoded = response.content
        music_library = decrypt_data(music_library_encoded, "base64_decompress")
        return MusicLibrary(music_library)

    async def get_song_data(self, id: int) -> Union[NewgroundsSong, MusicLibrary.Song]:
        if is_newgrounds_song(id):
            response = await send_post_request(
                url="http://boomlings.com/database/getGJSongInfo.php",
                data={'secret': self.secret, "songID": id}
            )
            return NewgroundsSong(response)
        else:
            music_library = await self.get_music_library()
            try:
                return music_library.songs[str(id)]
            except KeyError:
                raise RuntimeError(f"Cannot find song in the music library with id {id}")
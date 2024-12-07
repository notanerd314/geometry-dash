__doc__ = """
# `gd.thirdparty.sfh`

SFH stands for **Song File Hub**. This is a database for storing NONGs (Not On NewGrounds) songs replacements.
"""

from dataclasses import dataclass
from enum import StrEnum
from typing import Literal, Union

from gd.helpers import send_get_request
from gd.type_hints import SongFileHubId, SongId, LevelId

# * Literals, Enums
StateLiteral = Literal["rated", "unrated", "mashup", "challenge", "loop", "remix"]


class State(StrEnum):
    """
    An enumeration representing the state of a Song in Song File Hub.
    """

    RATED = "rated"
    UNRATED = "unrated"
    MASHUP = "mashup"
    CHALLENGE = "challenge"
    MENU_LOOP = "loop"
    REMIX = "remix"


# * Dataclasses
@dataclass
class Song:
    """
    A class representing a Song in Song File Hub.
    """

    id: SongFileHubId
    level_name: str
    url: str
    name: str
    replacement_song_id: SongId
    state: State
    file_type: str
    download_url: str
    level_ids: list[LevelId]
    downloads: int


class SongList(tuple):
    """
    A class representing a list of songs. (Not to be confused with SongFileHub)

    This class is inherited from **list** in Python. It has added additional searching and filtering methods.
    """
    def __new__(cls, songs: list[Song]) -> "SongList":
        if not all(isinstance(song, Song) for song in songs):
            raise ValueError("All items must be instances of sfh.Song.")

        return super().__new__(cls, songs)

    def search(
        self,
        query: Union[str, SongId],
        category: Literal["LEVEL_NAME", "SONG_NAME", "SONG_ID"],
    ) -> "SongList":
        """
        Search for songs by the query.

        :param query: The query for the search.
        :type query: str
        :param category: The category to search in ("LEVEL_NAME", "SONG_NAME", "SONG_ID").
        :type category: Literal["LEVEL_NAME", "SONG_NAME", "SONG_ID"]
        :return: A new SongList with songs that match the query.
        :rtype: SongList
        """
        search_results = []
        for song in self:
            if category == "LEVEL_NAME":
                if query.lower() in song.level_name.lower():
                    search_results.append(song)
            elif category == "SONG_NAME":
                if query.lower() in song.name.lower():
                    search_results.append(song)
            elif category == "SONG_ID":
                if str(query) == str(song.id):
                    search_results.append(song)

        return SongList(search_results)

    def sort_by_level_name(self, reverse: bool = False) -> "SongList":
        """
        Sort the songs by level name in ascending order.

        :param reverse: Whether to sort in descending order. Defaults to False.
        :type reverse: bool
        :return: A new SongList instance.
        :rtype: SongList
        """
        return SongList(sorted(self, key=lambda song: song.level_name, reverse=reverse))

    def sort_by_downloads(self, reverse: bool = False) -> "SongList":
        """
        Sort the songs by downloads in ascending order.

        :param reverse: Whether to sort in descending order. Defaults to False.
        :type reverse: bool
        :return: A new SongList instance.
        :rtype: SongList
        """
        return SongList(sorted(self, key=lambda song: song.downloads, reverse=reverse))

    def filter_by_state(self, state: Union[State, StateLiteral]) -> "SongList":
        """
        Filter songs by state.

        :param state: The state to filter by.
        :type state: Union[State, StateLiteral]
        :return: A new SongList instance.
        :rtype: SongList
        """
        filtered_songs = []
        for song in self:
            if song.state == state:
                filtered_songs.append(song)

        return SongList(filtered_songs)


# * Main client
class SongFileHub:
    """
    Song File Hub is a database for storing NONGs (Not On NewGrounds) songs replacements.
    """

    def __init__(self) -> None:
        pass

    async def songs(
        self,
        name: str = None,
        song_id: SongId = None,
        level_id: LevelId = None,
        state: Union[State, StateLiteral] = None,
        sort: Literal[None, "LEVEL_NAME", "DOWNLOADS"] = None,
        sort_reverse: bool = False
    ) -> SongList:
        """
        Get all songs from the Song File Hub.

        :param name: The name of the song to search for. (Returns exact matches)
        :type name: str
        :param song_id: The ID of the song to search for.
        :type song_id: SongId
        :param level_id: The ID of the level to search for.
        :type level_id: LevelId
        :param state: The state of the song to search for.
        :type state: Union[State, StateLiteral]
        :param sort: The sorting order of the songs. Can be "LEVEL_NAME" or "DOWNLOADS".
        :type sort: Literal[None, "LEVEL_NAME", "DOWNLOADS"]
        :param sort_reverse: Whether to sort in descending order. Defaults to False.
        :type sort_reverse: bool
        :return: SongList instance.
        :rtype: SongList
        """
        params = {
            "name": name,
            "songID": song_id,
            "levelID": level_id,
            "states": state,
        }

        response = await send_get_request(
            url="https://api.songfilehub.com/v2/songs",
            params={key: value for key, value in params.items() if value is not None},
        )
        response = response.json()

        list_song = []
        for song in response:
            list_song.append(
                Song(
                    id=song["_id"],
                    level_name=song["name"],
                    url=song["songURL"],
                    name=song["songName"],
                    replacement_song_id=song["songID"],
                    state=State(song["state"]),
                    file_type=song["filetype"],
                    download_url=song["downloadUrl"],
                    level_ids=[int(level_id) for level_id in song["levelID"]],
                    downloads=song["downloads"],
                )
            )

        songlist = SongList(list_song)
        if sort == "LEVEL_NAME":
            return songlist.sort_by_level_name(reverse=sort_reverse)
        if sort == "DOWNLOADS":
            return songlist.sort_by_downloads(reverse=sort_reverse)

        return SongList(sorted(songlist, reverse=sort_reverse))

    async def search_songs(
        self,
        query: Union[str, SongId],
        category: Literal["LEVEL_NAME", "SONG_NAME", "SONG_ID"],
    ) -> SongList:
        """
        Search for songs by the query.

        :param query: The query for the search.
        :type query: str
        :param category: The category to search in ("LEVEL_NAME", "SONG_NAME", "SONG_ID").
        :type category: Literal["LEVEL_NAME", "SONG_NAME", "SONG_ID"]
        :return: A new SongList with songs that match the query.
        :rtype: SongList
        """
        songs = await self.songs()
        return songs.search(query=query, category=category)

    async def filter_by_state(self, state: Union[State, StateLiteral]) -> SongList:
        """
        Filter songs by state.

        :param state: The state to filter by.
        :type state: Union[State, StateLiteral]
        :return: A new SongList instance.
        :rtype: SongList
        """
        songs = await self.songs()
        return songs.filter_by_state(state=state)

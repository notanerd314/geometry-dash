__doc__ = """
# `gd.thirdparty.sfh`

SFH stands for **Song File Hub**. This is a database for storing NONGs (Not On NewGrounds) songs replacements.
"""

from dataclasses import dataclass
from enum import Enum

from gd.helpers import send_get_request
from gd.type_hints import SongFileHubId, SongId, LevelId


class State(Enum):
    """
    An enumeration representing the state of a Song in Song File Hub.
    """

    RATED = "rated"
    UNRATED = "unrated"
    MASHUP = "mashup"
    CHALLENGE = "challenge"
    MENU_LOOP = "loop"
    REMIX = "remix"


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
        state: State = None,
    ) -> list[Song]:
        """
        Get all songs from the Song File Hub.

        :return: A list of Song objects.
        :rtype: list[Song]
        """
        response = await send_get_request(
            url="https://api.songfilehub.com/v2/songs/",
            params={
                "name": name,
                "songID": song_id,
                "levelID": level_id,
                "states": state.value if state else None,
            },
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

        return list_song

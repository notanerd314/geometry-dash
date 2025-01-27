"""
## .objects.song
A module containing all the classes and methods related to songs in Geometry Dash.
"""

from urllib.parse import unquote
from typing import Optional, Union, List

import attr

from gd.parse import parse_song_data
from gd.type_hints import (
    SongId,
    SoundEffectId,
    MusicLibrarySongId,
    MusicLibraryArtistId,
    SoundEffectFolderId,
    ArtistId,
)
from gd.gdobject import Downloadable
from gd.enums import Folders, Tags

__all__ = ["MusicLibrary", "SoundEffectLibrary", "SoundEffect", "Song"]

# Music Library


@attr.define(slots=True)
class MusicLibrary:
    """
    A class representing the whole entire music library.

    Attributes
    ----------
    version : int
        The version number of the library.
    artists : list[MusicLibrary.Artist]
        The artists of the library.
    songs : list[MusicLibrary.Song]
        The songs of the library.
    tags : list[str]
        The tags of the library.
    """

    version: int
    """The version number of the library."""
    artists: list["MusicLibrary.Artist"] = attr.field(default=list)
    """The version number of the library."""
    songs: list["MusicLibrary.Song"] = attr.field(default=list)
    """The songs of the library."""
    tags: dict[int, str] = attr.field(default=list)
    """The tags of the library."""

    @attr.define(slots=True)
    class Artist:
        """
        A class representing an artist in the music library.

        Attributes
        ----------
        id : MusicLibraryArtistId
            The ID of the artist.
        name : str
            The name of the artist.
        website : Union[str | None]
            The official website of the artist.
        youtube_channel_id : Union[str | None]
            The artist's YouTube channel ID.
        """

        id: MusicLibraryArtistId
        """The ID of the artist."""
        name: str
        """The name of the artist."""
        website: Optional[str] = None
        """The website of the artist."""
        youtube_channel_id: Optional[str] = None
        """The youtube channel ID of the artist."""

        @staticmethod
        def from_raw(raw_str: str) -> "MusicLibrary.Artist":
            """
            A static method that creates a `MusicLibrary.Artist`  from raw data.

            :param raw_str: The raw str returned from the servers.
            :type raw_str: str
            :return: A `MusicLibraryArtist` instance.
            """

            parsed = raw_str.strip().split(",")
            return MusicLibrary.Artist(
                id=int(parsed[0]),
                name=parsed[1],
                website=unquote(parsed[2]) if parsed[2].strip() else None,
                youtube_channel_id=parsed[3] if parsed[3].strip() else None,
            )

    @attr.define(slots=True)
    class Song(Downloadable):
        """
        A class representing a song in the music library.

        Attributes
        ----------
        id : MusicLibrarySongId
            The ID of the song.
        name : str
            The name of the song.
        artist : Optional["MusicLibrary.Artist"]
            The artist of the song, returns None if it doesn't exist.
        tags : set[str]
            The tags associated with the song.
        size : float
            The size of the song in bytes.
        duration_seconds : int
            The duration of the song in seconds.
        is_ncs : bool
            If the song was made by NCS.
        """

        id: MusicLibrarySongId
        name: str
        artist: Optional["MusicLibrary.Artist"]
        tags: set[Tags]
        size: float
        duration_seconds: int
        is_ncs: bool
        link: str
        external_link: str

        @staticmethod
        def from_raw(
            raw_str: str,
            artists_list: list["MusicLibrary.Artist"],
            tags_list: list[str] = None,
        ) -> "MusicLibrary.Song":
            """
            A static method that converts raw string to a `MusicLibrary.Song` instance.

            :param raw_str: The raw str returned from the servers.
            :type raw_str: str
            :param artists_list: A dictionary of artist IDs to `MusicLibraryArtist` instances.
            :type artists_list: dict[int, MusicLibraryArtist]
            :return: An instance of a MusicLibrarySong.
            """

            parsed = raw_str.strip().split(",")

            song_artist = None
            for artist in artists_list:
                if str(artist.id) == parsed[2]:
                    song_artist = artist

            raw_song_tag_list = parsed[5].split(".")
            song_tag_list = {
                tags_list.get(tag) for tag in raw_song_tag_list if tag.strip()
            }

            return MusicLibrary.Song(
                id=int(parsed[0]),
                name=parsed[1],
                artist=song_artist,
                tags=song_tag_list,
                size=float(parsed[3]),
                duration_seconds=int(parsed[4]),
                is_ncs=parsed[6] == "1",
                link=f"https://geometrydashfiles.b-cdn.net/music/{parsed[0]}.ogg",
                external_link=f"https://{unquote(parsed[8])}",
            )

    @staticmethod
    def from_raw(raw_str: str) -> "MusicLibrary":
        """
        A static method that converts a raw string from the servers to a `MusicLibrary` instance.

        :param raw_str: The raw data returned from the servers.
        :type raw_str: str
        :return: An instance of a MusicLibrary.
        """

        parsed = tuple(raw_str.strip().split("|"))
        version = int(parsed[0])

        artists = [
            MusicLibrary.Artist.from_raw(artist)
            for artist in parsed[1].split(";")
            if artist.strip()
        ]

        tags = {
            tag.split(",")[0].strip(): tag.split(",")[1].strip()
            for tag in parsed[3].split(";")
            if tag.strip()
        }

        songs = [
            MusicLibrary.Song.from_raw(song, artists, tags)
            for song in parsed[2].split(";")
            if song.strip()
        ]

        return MusicLibrary(version=version, artists=artists, songs=songs, tags=tags)

    def search_songs(
        self,
        filter_tags: Optional[Union[set[Tags], Tags]] = None,
        filter_artists: Optional[Union[set[str], str]] = None,
    ) -> list[Song]:
        """
        Get all songs with the tags specified.

        :param tags: The name of tags to filter by.
        :type tags: set[str]
        :return: A list of songs that have the specified tags.
        :rtype: list[Song]
        """
        songs = []

        if isinstance(filter_tags, str):
            filter_tags = {filter_tags}

        if isinstance(filter_artists, str):
            filter_artists = {filter_artists}

        for song in self.songs:
            print(song.tags)
            if filter_tags and not filter_tags.issubset(song.tags):
                continue
            if filter_artists and song.artist.name not in filter_artists:
                continue

            songs.append(song)

        return songs

    def get_song_by_id(self, song_id: MusicLibrarySongId) -> Optional[Song]:
        """
        Get a song by it's ID.

        :param song_id: The ID of the song.
        :type song_id: MusicLibrarySongId
        :return: A `MusicLibrarySong` instance if found, otherwise None.
        :rtype: Optional[Song]
        """
        for song in self.songs:
            if song_id == song.id:
                return song
        return None


# SFX Library


@attr.define(slots=True)
class SoundEffectLibrary:
    """
    A class representing the sound effect library.

    Attributes
    ----------
    version : Optional[int]
        The version of the library.
    folders : list[SoundEffectLibrary.Folder]
        All the folders of the SoundEffectLibrary that also contains the songs in each value.
    creators : list[SoundEffectLibrary.Creator]
        The list of all the creators in the library.
    sfx : list[SoundEffect]
        The list of all sound effects in the library.
    """

    version: Optional[int]
    folders: list["SoundEffectLibrary.Folder"]
    creators: list["SoundEffectLibrary.Creator"]
    sfx: list["SoundEffect"]

    @attr.define(slots=True)
    class Folder:
        """
        A class representing a folder in the SFX library.

        Attributes
        ----------
        id : int
            The id of the folder.
        name : str
            The name of the folder.
        """

        id: SoundEffectFolderId
        name: str

        @staticmethod
        def from_raw(raw_str: str) -> "SoundEffectLibrary.Folder":
            """
            A static method to create a SoundEffectLibrary.Folder from raw data.

            :param raw_str: The raw data of the folder.
            :type raw_str: str
            :return: An instance of the SoundEffectLibrary.Folder class.
            :rtype: SoundEffectLibrary.Folder
            """
            parsed = raw_str.strip().split(",")
            return SoundEffectLibrary.Folder(id=int(parsed[0]), name=parsed[1])

    @attr.define(slots=True)
    class Creator:
        """
        A class representing a creator in the SFX library.

        Attributes
        ----------
        name : str
            The name of the creator.
        url : Union[str, None]
            The website of the creator.
        """

        name: str
        url: Union[str, None]

        @staticmethod
        def from_raw(raw_str: str) -> "SoundEffectLibrary.Creator":
            """
            A static method that creates a SoundEffectLibrary.Creator from raw data.

            :param raw_str: The raw data of the creator.
            :type raw_str: str
            :return: An instance of the SoundEffectLibrary.Creator class.
            :rtype: SoundEffectLibrary.Creator
            """
            parsed = raw_str.strip().split(",")
            return SoundEffectLibrary.Creator(name=parsed[0], url=unquote(parsed[1]))

    @staticmethod
    def from_raw(raw_str: str) -> "SoundEffectLibrary":
        """
        A static method that converts raw data to a SoundEffectLibrary instance.

        :param raw_str: The raw data returned from the servers.
        :type raw_str: str
        :return: An instance of the SoundEffectLibrary class.
        :rtype: SoundEffectLibrary
        """
        # Split raw data once and strip unnecessary spaces
        parsed = raw_str.strip().split("|")
        parsed_sfx = parsed[0].split(";")
        parsed_creators = parsed[1].split(";")

        version_name = None
        folders = []
        sfx = []

        # Iterate over sound effects and folders
        for entity in parsed_sfx:
            entity = entity.strip()
            if not entity:  # Skip empty entries
                continue

            parts = entity.split(",")
            is_folder = parts[2] == "1"  # Direct comparison instead of slicing

            if is_folder:
                folder = SoundEffectLibrary.Folder.from_raw(entity)
                if folder.id == 1:
                    version_name = folder.name
                else:
                    folders.append(folder)
            else:
                soundeffect = SoundEffect.from_raw(entity)
                sfx.append(soundeffect)

        # Filter creators directly to remove empty strings
        creators = [
            SoundEffectLibrary.Creator.from_raw(creator)
            for creator in parsed_creators
            if creator.strip()
        ]

        # Return the SoundEffectLibrary instance
        return SoundEffectLibrary(
            version=int(version_name) if version_name else None,
            folders=folders,
            creators=creators,
            sfx=sfx,
        )

    def _find_by_attribute(
        self, collection: list[any], attribute: str, value: any
    ) -> Union[object, None]:
        """
        A helper function to find an item by an attribute.

        :param collection: The collection of items to search.
        :type collection: list
        :param attribute: The attribute of the item to compare.
        :type attribute: str
        :param value: The value to match against the attribute.
        :return: The found object or None if not found.
        :rtype: object or None
        """
        for item in collection:
            if getattr(item, attribute) == value:
                return item
        return None

    def get_folder_by_id(
        self, folder_id: SoundEffectFolderId
    ) -> Optional["SoundEffectLibrary.Folder"]:
        """
        Get a folder by it's ID.

        :param folder_id: The ID of the folder.
        :type folder_id: int
        :return: A SoundEffectLibrary.Folder class, if not found, returns NoneType.
        :rtype: SoundEffectLibrary.Folder
        """
        return self._find_by_attribute(self.folders, "id", folder_id)

    def get_sfx_by_id(self, sfx_id: SoundEffectId) -> Optional["SoundEffect"]:
        """
        Get a sound effect by it's ID.

        :param sfx_id: The ID of the sound effect.
        :type sfx_id: int
        :return: A SoundEffect class, if not found, returns NoneType.
        :rtype: SoundEffect
        """
        return self._find_by_attribute(self.sfx, "id", sfx_id)

    def open_folder(self, folder_name: Folders) -> List["SoundEffect"]:
        """
        Returns all sound effects in a folder.

        :param folder_name: The name of the folder.
        :type folder_name: Folders
        :return: A list of SoundEffect classes, if not found, raises a ValueError.
        """
        for folder in self.folders:
            if folder.name == folder_name:
                sfx = []
                for sfx in self.sfx:
                    if sfx.parent_folder_id == folder.id:
                        return sfx

        raise ValueError(f"Folder '{folder_name}' not found")


@attr.define(slots=True)
class SoundEffect(Downloadable):
    """
    A class representing a sound effect in the SFX library.

    Attributes
    ----------
    id : SoundEffectId
        The id of the sound effect.
    name : str
        The name of the sound effect.
    parent_folder_id : SoundEffectFolderId
        The folder id of the sound effect belongs to.
    size : float
        The size of the sound effect.
    link : str
        The link to the sound effect.
    duration : int
        The duration of the sound effect in seconds.
    """

    id: SoundEffectId
    name: str
    parent_folder_id: SoundEffectFolderId
    size: float
    link: str
    duration_seconds: int

    @staticmethod
    def from_raw(raw_str: str) -> "SoundEffect":
        """
        A static method that converts the raw data from the servers into a SFX .

        :param raw_str: The raw data from the servers.
        :type raw_str: str
        :return: An instance of the SFX class.
        """
        parsed = raw_str.strip().split(",")
        return SoundEffect(
            id=int(parsed[0]),
            name=parsed[1],
            parent_folder_id=int(parsed[3]),
            size=float(parsed[4]),
            link=f"https://geometrydashfiles.b-cdn.net/sfx/s{parsed[0]}.ogg",
            duration_seconds=int(parsed[5]) / 100,
        )


# Level song


@attr.define(slots=True)
class Song(Downloadable):
    """
    A class representing a level song in the Geometry Dash level.

    Attributes
    ----------
    id : SongId
        The ID of the song.
    name : str
        The name of the song.
    artist_id : Optional[ArtistId]
        The ID of the song's artist.
    artist_name : Optional[str]
        The name of the song's artist.
    artist_verified : Optional[bool]
        If the artist is verified.
    song_size_mb : float
        The size of the song in megabytes.
    youtube_link : Optional[str]
        The YouTube link to the song.
    link : Optional[str]
        The link to the song.
    is_ncs : Optional[bool]
        If the song was made by NCS.
    is_in_library : Optional[bool]
        If the song belongs to the music library.
    """

    id: SongId
    name: str
    artist_id: Optional[ArtistId]
    artist_name: Optional[str]
    artist_verified: Optional[bool]
    size: float
    youtube_link: Optional[str]
    link: Optional[str]
    is_ncs: Optional[bool]
    is_in_library: Optional[bool]

    @staticmethod
    def from_raw(raw_str: str) -> "Song":
        """
        A static method that converts the raw data from the servers into a Song .

        :param raw_str: The raw data from the servers.
        :type raw_str: str
        :return: An instance of the Song class.
        """
        parsed = parse_song_data(raw_str)
        return Song.from_parsed(parsed)

    @staticmethod
    def from_parsed(parsed_str: dict[str, any]) -> "Song":
        """
        A static method that converts the parsed string into a Song object.

        :param parsed_str: The parsed string from the servers.
        :type parsed_str: str
        :return: An instance of the Song class.
        """
        parsed = parsed_str
        link = unquote(parsed.get("10"))

        if link == "CUSTOMURL":
            link = f"https://geometrydashfiles.b-cdn.net/music/{parsed.get('1')}.ogg"

        return Song(
            id=int(parsed.get("1")),
            name=parsed.get("2"),
            artist_id=parsed.get("3"),
            artist_name=parsed.get("4"),
            artist_verified=parsed.get("8") == 1,
            size=float(parsed.get("5", 0.0)),
            youtube_link=(
                f"https://youtu.be/watch?v={parsed.get('6')}"
                if parsed.get("6")
                else None
            ),
            link=link,
            is_ncs=parsed.get("11") == 1,
            is_in_library=int(parsed.get("1")) >= 10000000,
        )

"""
## .models.song
A module containing all the classes and methods related to songs in Geometry Dash.
"""

from urllib.parse import unquote
from typing import Dict, Optional, List
from datetime import timedelta
from ..helpers import *
from dataclasses import dataclass, field
from enum import Enum
from aiofiles import open as aioopen
import os

# Music Library

@dataclass
class MusicLibrary:
    """
    A class representing the whole entire music library.

    Attributes
    ----------
    version : int
        The version number of the library.
    artists : Dict[int, MusicLibraryArtist]
        The artists of the library.
    songs : Dict[int, MusicLibrarySong]
        The songs of the library.
    tags : Dict[int, str]
        The tags of the library.
    """

    version: int
    artists: Dict[int, 'MusicLibrary.Artist'] = field(default_factory=dict)
    songs: Dict[int, 'MusicLibrary.Song'] = field(default_factory=dict)
    tags: Dict[int, str] = field(default_factory=dict)

    @dataclass
    class Artist:
        """
        A class representing an artist in the music library.

        Attributes
        ----------
        id : int
            The ID of the artist.
        name : str
            The name of the artist.
        website : Union[str | None]
            The official website of the artist.
        youtube_channel_id : Union[str | None]
            The artist's YouTube channel ID.
        """
        id: int
        name: str
        website: Optional[str] = None
        youtube_channel_id: Optional[str] = None

        @staticmethod
        def from_raw(raw_str: str) -> 'MusicLibrary.Artist':
            """
            A static method that converts a raw string from the servers to a `MusicLibraryArtist` instance.

            :param raw_str: The raw str returned from the servers.
            :type raw_str: str
            :return: A `MusicLibraryArtist` instance.
            """

            try:
                parsed = raw_str.strip().split(",")
                return MusicLibrary.Artist(
                    id=int(parsed[0]),
                    name=parsed[1],
                    website=unquote(parsed[2]) if parsed[2].strip() else None,
                    youtube_channel_id=parsed[3] if parsed[3].strip() else None
                )
            except Exception as e:
                raise ParseError(f"Cannot parse the data provided, error: {e}")

    @dataclass
    class Song:
        """
        A class representing a song in the music library.

        Attributes
        ----------
        id : int
            The ID of the song.
        name : str
            The name of the song.
        artist : Union[MusicLibraryArtist, None]
            The artist of the song, returns None if it doesn't exist.
        tags : set[str]
            The tags associated with the song.
        size : float
            The size of the song in bytes.
        duration_seconds : timedelta
            The duration of the song in seconds.
        is_ncs : bool
            If the song was made by NCS.
        """

        id: int
        name: str
        artist: Optional['MusicLibrary.Artist']
        tags: set[str]
        size: float
        duration_seconds: timedelta
        is_ncs: bool
        link: str
        external_link: str

        @staticmethod
        def from_raw(raw_str: str, artists_list: Dict[int, 'MusicLibrary.Artist'] = {}, tags_list: Dict[int, str] = None) -> 'MusicLibrary.Song':
            """
            A static method that converts a raw string from the servers to a `MusicLibrarySong` instance.

            :param raw_str: The raw str returned from the servers.
            :type raw_str: str
            :param artists_list: A dictionary of artist IDs to `MusicLibraryArtist` instances.
            :type artists_list: Dict[int, MusicLibraryArtist]
            :return: An instance of a MusicLibrarySong.
            """

            try:
                parsed = raw_str.strip().split(",")
                try:
                    artist_id = int(parsed[2]) if parsed[2].strip() else None
                except ValueError:
                    artist_id = None

                raw_song_tag_list = [tag for tag in parsed[5].split(".") if tag]
                song_tag_list = {tags_list.get(int(tag)) for tag in raw_song_tag_list}

                return MusicLibrary.Song(
                    id=int(parsed[0]),
                    name=parsed[1],
                    artist=artists_list.get(artist_id),
                    tags=song_tag_list,
                    size=float(parsed[3]),
                    duration_seconds=timedelta(seconds=int(parsed[4])),
                    is_ncs=parsed[6] == '1',
                    link=f"https://geometrydashfiles.b-cdn.net/music/{parsed[0]}.ogg",
                    external_link=f"https://{unquote(parsed[8])}"
                )
            except Exception as e:
                raise ParseError(f"Cannot parse the data provided, error: {e}")
        
        async def download_to(self, file: str = None, path: str = None) -> None:
            """
            A static method that converts a raw string from the servers to a `MusicLibraryArtist` instance.

            :param raw_str: The raw str returned from the servers.
            :type raw_str: str
            :return: A `MusicLibraryArtist` instance.
            """

            if not file:
                file = f"{self.id}.ogg"
            
            if not file.endswith(".ogg"):
                raise ValueError("file must end with .ogg!")

            # Set the path to the current working directory if not specified
            if path is None:
                path = os.getcwd()

            # Ensure the directory exists
            os.makedirs(path, exist_ok=True)

            try:
                response = await send_get_request(decode=False, url=self.link)
                async with aioopen(os.path.join(path, file), "wb") as file:
                    await file.write(response)
            except Exception as e:
                raise DownloadSongError(f"Error downloading song: {e}")
        
    @staticmethod
    def from_raw(raw_str: str) -> 'MusicLibrary':
        """
        A static method that converts a raw string from the servers to a `MusicLibrary` instance.

        :param raw_str: The raw data returned from the servers.
        :type raw_str: str
        :return: An instance of a MusicLibrary.
        """

        parsed = raw_str.strip().split("|")
        version = int(parsed[0])

        artists = {
            int(artist.split(",")[0]): MusicLibrary.Artist.from_raw(artist)
            for artist in parsed[1].split(";") if artist.strip()
        }

        tags = {
            int(tag.split(",")[0]): tag.split(",")[1].strip()
            for tag in parsed[3].split(";") if tag.strip()
        }

        songs = {
            int(song.split(",")[0]): MusicLibrary.Song.from_raw(song, artists, tags)
            for song in parsed[2].split(";") if song.strip()
        }

        return MusicLibrary(version=version, artists=artists, songs=songs, tags=tags)
    
    def filter_song_by_tags(self, tags: set[str]) -> List[Song]:
        """
        Get all songs with the tags specified.

        :param tags: The name of tags to filter by.
        :type tags: set[str]
        :return: A list of songs that have the specified tags.
        """
        songs = []
        tags = {tag.lower() for tag in tags}

        for tag in tags:
            if tag not in [tag.lower() for tag in self.tags.values()]:
                raise ValueError(f"The tag {tag} doesn't exist in the music library!")
        
        for song in self.songs.values():
            song_tag = {tag.lower() for tag in song.tags}
            if tags.issubset(song_tag) and song_tag:
                songs.append(song)
        return songs

    def get_song_by_name(self, name: str) -> Song | None:
        """
        Get a song by it's name.

        :param name: The name of the song to search for.
        :type name: str
        :return: A `MusicLibrarySong` instance if found, otherwise None.
        """
        for song in self.songs.values():
            if song.name.lower() == name.lower():
                return song
        return None

    def get_song_by_id(self, id: int) -> Song | None:
        """
        Get a song by it's ID.

        :param id: The ID of the song.
        :type id: int
        :return: A `MusicLibrarySong` instance if found, otherwise None.
        """
        for song in self.songs.values():
            if id == song.id:
                return song
        return None
    
    def search_songs(self, query: str) -> list[Song]:
        """
        Find all songs that contains the query in it's name. (Different from `.get_song_by_name`!)

        :param query: The query string to search for.
        :type query: str
        :return: A list of songs that match the query.
        """
        query = query.rstrip()
        songs = []

        for song in self.songs.values():
            if query.lower() in song.name.lower():
                songs.append(song)
        return songs
    
    def filter_song_by_artist(self, artist: str) -> list[Song]:
        """
        Filter songs by artist's name.

        :param artist: The name of the artist to filter by.
        :type artist: str
        :return: A list of songs made by the artist.
        """
        songs = []

        for song in self.songs.values():
            try:
                if song.artist.name.lower() == artist.lower():
                    songs.append(song)
            except AttributeError:
                pass
        return songs

# SFX Library

@dataclass
class SoundEffectLibrary:
    """
    A class representing the sound effect library.

    Attributes
    ----------
    version : int
        The version of the library.
    folders : List[SoundEffectLibrary.Folder]
        All the folders of the SoundEffectLibrary that also contains the songs in each value.
    creators : List[Creator]
        The list of all the creators in the library.
    """

    version: int
    folders: List['SoundEffectLibrary.Folder']
    creators: List['Creator']
    sfx: List['SoundEffect']
    
    @dataclass
    class Folder:
        """
        A class representing a folder in the SFX library.
        
        Attributes
        ----------
        id : int
            The id of the folder.
        name : str
            The name of the folder.
        sfx : List[SFX]
            The sound effects that the folder contains.
        """
        id: int
        name: str

        @staticmethod
        def from_raw(raw_str: str) -> 'SoundEffectLibrary.Folder':
            """
            A static method to create a SoundEffectLibrary.Folder from raw data.
            
            :param raw_str: The raw data of the folder.
            :type raw_str: str
            :return: An instance of the SoundEffectLibrary.Folder class.
            """
            parsed = raw_str.strip().split(",")
            return SoundEffectLibrary.Folder(
                id=int(parsed[0]),
                name=parsed[1],
            )

    @dataclass
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
        def from_raw(raw_str: str) -> 'SoundEffectLibrary.Creator':
            parsed = raw_str.strip().split(",")
            return SoundEffectLibrary.Creator(
                name=parsed[0],
                url=unquote(parsed[1])
            )

    @staticmethod
    def from_raw(raw_str: str) -> 'SoundEffectLibrary':
        """
        A static method that converts the raw data returned from the servers to a SoundEffectLibrary instance.

        :param raw_str: The raw data returned from the servers.
        :type raw_str: str
        :return: An instance of the SoundEffectLibrary class.
        """
        parsed = raw_str.strip().split("|")
        parsed_sfx = parsed[0].split(";")
        parsed_creators = parsed[1].split(";")

        # Extract the version name from folder with id 1
        folders = []
        for folder_str in parsed_sfx:
            try:
                is_folder = folder_str.strip().split(",")[2] == "1"
            except IndexError:
                is_folder = False

            if is_folder:
                folder = SoundEffectLibrary.Folder.from_raw(folder_str)
                if folder.id == 1:
                    version_name = folder.name  # Folder with id 1 contains the version name
                else:
                    folders.append(folder)

        # Inject SFX into the appropriate folders
        sfx = []
        for raw_sfx in parsed_sfx:
            try:
                is_not_folder = raw_sfx.strip().split(",")[2] != "1"
            except IndexError:
                is_not_folder = False
            
            sfx_object = SoundEffect.from_raw(raw_sfx)
            if is_not_folder:
                sfx_folder_id = sfx_object.parent_folder_id

                for folder in folders:
                    if folder.id == sfx_folder_id:
                        folder.add_sfx(raw_sfx)
                        break

            sfx.append(sfx_object)

        creators = [SoundEffectLibrary.Creator.from_raw(creator) for creator in parsed_creators if creator != ""]

        return SoundEffectLibrary(version=int(version_name), folders=folders, creators=creators, sfx=sfx)

    def get_folder_by_name(self, name: str) -> Union['SoundEffectLibrary.Folder', None]:
        """
        Get a folder by it's name.

        :param name: The name of the folder.
        :type name: str
        :return: A SoundEffectLibrary.Folder class, if not found, returns NoneType.
        """
        for folder in self.folders:
            if folder.name.lower() == name.lower():
                return folder
            
        return None
    
    def get_folder_by_id(self, id: int) -> Union['SoundEffectLibrary.Folder', None]:
        """
        Get a folder by it's ID.

        :param id: The ID of the folder.
        :type id: int
        :return: A SoundEffectLibrary.Folder class, if not found, returns NoneType.
        """
        for folder in self.folders:
            if folder.id == id:
                return folder
            
        return None
    
    def get_sfx_by_id(self, id: int) -> Union['SoundEffect', None]:
        """
        Get a sound effect by it's ID.

        :param id: The ID of the sound effect.
        :type id: int
        :return: A SoundEffect class, if not found, returns NoneType.
        """
        for sfx in self.sfx:
            if sfx.id == id:
                return sfx
            
        return None
    
    def search_folders(self, query: str) -> List['SoundEffectLibrary.Folder']:
        """
        Filter folders by the query. (Different from `.get_folder_by_name`!)

        :param query: The query for the search.
        :type query: str
        :return: A list of SoundEffectLibrary.Folder.
        """

        folders = []
        for folder in self.folders:
            if query.lower() in folder.name.lower():
                folders.append(folder)

        return folders
    
    def search_folders_and_sfx(self, query: str) -> List[Union['SoundEffectLibrary.Folder', 'SoundEffect']]:
        """
        Filter folders and sfx by the query.

        :param query: The query for the search.
        :type query: str
        :return: A list of SoundEffectLibrary.Folder and SoundEffect.
        """

        result = []
        folder_sfx = self.folders + self.sfx
        for item in folder_sfx:
            if query.lower() in item.name.lower():
                result.append(item)

        return result
    
    def filter_sfx_by_folder(self, folder_id: int) -> List['SoundEffect']:
        """
        Filter folders and sfx by the query.

        :param folder_id: The folder ID to filter.
        :type folder_id: int
        :return: A list of SoundEffect.
        """
        result = []
        for item in self.sfx:
            if item.parent_folder_id == folder_id:
                result.append(item)

        return result

@dataclass
class SoundEffect:
    """
    A class representing a sound effect in the SFX library.

    Attributes
    ----------
    id : int
        The id of the sound effect.
    name : str
        The name of the sound effect.
    parent_folder_id : int
        The folder id of the sound effect belongs to.
    size : float
        The size of the sound effect.
    url : str
        The link to the sound effect.
    duration : timedelta
        The duration of the sound effect in seconds.
    """
    id: int
    name: str
    parent_folder_id: str
    size: float
    url: str
    duration: timedelta

    @staticmethod
    def from_raw(raw_str: str) -> 'SoundEffect':
        """
        A static method that converts the raw data from the servers into a SFX object.

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
            url=f"https://geometrydashfiles.b-cdn.net/sfx/s{parsed[0]}.ogg",
            duration=timedelta(seconds=int(parsed[5])//100)
        )
    
    async def download_to(self, file: str = None, path: str = None) -> None:
        """
        A method that downloads the song to a specific path location.

        :param file: The name of the file to save the song as. Default is the song ID.
        :type file: Optional[str]
        :param path: The path to save the song. Default is the current working directory.
        :type path: Optional[str]
        :raises DownloadSongError: If an error occurs during downloading the song.
        :return: None
        """
        if not file:
            file = f"{self.id}.ogg"
        
        if not file.endswith(".ogg"):
            raise ValueError("file must end with .ogg!")

        # Set the path to the current working directory if not specified
        if path is None:
            path = os.getcwd()

        # Ensure the directory exists
        os.makedirs(path, exist_ok=True)

        try:
            response = await send_get_request(decode=False, url=self.url)
            async with aioopen(os.path.join(path, file), "wb") as file:
                await file.write(response)
        except Exception as e:
            raise DownloadSongError(f"Error downloading song: {e}")

# Level song

@dataclass
class Song:
    """
    A class representing a level song in the Geometry Dash level.

    Attributes
    ----------
    id : int
        The ID of the song.
    name : str
        The name of the song.
    artist_id : Optional[int]
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
    id: int
    name: str
    artist_id: Optional[int]
    artist_name: Optional[str]
    artist_verified: Optional[bool]
    size: float
    youtube_link: Optional[str]
    link: Optional[str]
    is_ncs: Optional[bool]
    is_in_library: Optional[bool]

    @staticmethod
    def from_raw(raw_str: str) -> 'Song':
        """
        A static method that converts the raw data from the servers into a Song object.
        
        :param raw_str: The raw data from the servers.
        :type raw_str: str
        :return: An instance of the Song class.
        """
        parsed = parse_song_data(raw_str)
        return Song.from_parsed(parsed)

    @staticmethod
    def from_parsed(parsed_str: Dict) -> 'Song':
        """
        A static method that converts the parsed string into a Song object.

        :param parsed_str: The parsed string from the servers.
        :type parsed_str: str
        :return: An instance of the Song class.
        """
        parsed = parsed_str
        return Song(
            id=int(parsed.get('1')),
            name=parsed.get('2'),
            artist_id=parsed.get('3'),
            artist_name=parsed.get('4'),
            artist_verified=parsed.get('8') == 1,
            size=float(parsed.get('5', 0.0)),
            youtube_link=f"https://youtu.be/watch?v={parsed.get('6')}" if parsed.get("6") else None,
            link=unquote(parsed.get("10", '')) if parsed.get("10") else None,
            is_ncs=parsed.get('11') == 1,
            is_in_library=int(parsed.get('1')) >= 10000000
        )

    async def download_to(self, file: str = None, path: str = None) -> None:
        """
        A method that downloads the song to a specific path location.

        :param file: The name of the file to save the song. Default is the song ID.
        :type file: Optional[str]
        :param path: The path to save the song. Default is the current working directory.
        :type path: Optional[str]
        :raises DownloadSongError: If an error occurs during downloading the song.
        :return: None
        """
        if not file:
            file = f"{self.id}.mp3"

        # Set the path to the current working directory if not specified
        if path is None:
            path = os.getcwd()

        # Ensure the directory exists
        os.makedirs(path, exist_ok=True)

        try:
            response = await send_get_request(decode=False, url=self.link)
            async with aioopen(os.path.join(path, file), "wb") as file:
                await file.write(response)
        except Exception as e:
            raise DownloadSongError(f"Error downloading song: {e}")

class OfficialSong(Enum):
    """
    An **Enum** class representing official songs in the game.
    """
    STAY_INSIDE_ME = -1
    STEREO_MADNESS = 0
    BACK_ON_TRACK = 1
    POLARGEIST = 2
    DRY_OUT = 3
    BASE_AFTER_BASE = 4
    CANT_LET_GO = 5
    JUMPER = 6
    TIME_MACHINE = 7
    CYCLES = 8
    XSTEP = 9
    CLUTTERFUNK = 10
    THEORY_OF_EVERYTHING = 11
    ELECTROMAN_ADVENTURES = 12
    CLUBSTEP = 13
    ELECTRODYNAMIX = 14
    HEXAGON_FORCE = 15
    BLAST_PROCESSING = 16
    THEORY_OF_EVERYTHING_2 = 17
    GEOMETRICAL_DOMINATOR = 18
    DEADLOCKED = 19
    FINGERDASH = 20
    DASH = 21
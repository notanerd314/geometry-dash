from urllib.parse import unquote
from typing import Dict, Optional, List
from datetime import timedelta
from ..helpers import *
from dataclasses import dataclass, field
from enum import Enum

# Music Library

@dataclass
class MusicLibraryArtist:
    id: int
    name: str
    website: Optional[str] = None
    youtube_channel_id: Optional[str] = None

    @staticmethod
    def from_raw(raw_str: str) -> 'MusicLibraryArtist':
        parsed = raw_str.strip().split(",")
        return MusicLibraryArtist(
            id=int(parsed[0]),
            name=parsed[1],
            website=unquote(parsed[2]) if parsed[2].strip() else None,
            youtube_channel_id=parsed[3] if parsed[3].strip() else None
        )

@dataclass
class MusicLibrarySong:
    id: int
    name: str
    artist: Optional[MusicLibraryArtist]
    tags: set[str]
    file_size_bytes: float
    duration_seconds: timedelta
    is_ncs: bool

    @staticmethod
    def from_raw(raw_str: str, artists_list: Dict[int, MusicLibraryArtist] = None, tags_list: Dict[int, str] = None) -> 'MusicLibrarySong':
        parsed = raw_str.strip().split(",")
        try:
            artist_id = int(parsed[2]) if parsed[2].strip() else None
        except ValueError:
            artist_id = None

        raw_song_tag_list = [tag for tag in parsed[5].split(".") if tag]
        song_tag_list = {tags_list.get(int(tag)) for tag in raw_song_tag_list}

        return MusicLibrarySong(
            id=int(parsed[0]),
            name=parsed[1],
            artist=artists_list.get(artist_id),
            tags=song_tag_list,
            file_size_bytes=float(parsed[3]),
            duration_seconds=timedelta(seconds=int(parsed[4])),
            is_ncs=parsed[6] == '1'
        )


@dataclass
class MusicLibrary:
    version: int
    artists: Dict[int, MusicLibraryArtist] = field(default_factory=dict)
    songs: Dict[int, MusicLibrarySong] = field(default_factory=dict)
    tags: Dict[int, str] = field(default_factory=dict)

    @staticmethod
    def from_raw(raw_str: str) -> 'MusicLibrary':
        parsed = raw_str.strip().split("|")
        version = int(parsed[0])

        artists = {
            int(artist.split(",")[0]): MusicLibraryArtist.from_raw(artist)
            for artist in parsed[1].split(";") if artist.strip()
        }

        tags = {
            int(tag.split(",")[0]): tag.split(",")[1].strip()
            for tag in parsed[3].split(";") if tag.strip()
        }

        songs = {
            int(song.split(",")[0]): MusicLibrarySong.from_raw(song, artists, tags)
            for song in parsed[2].split(";") if song.strip()
        }

        return MusicLibrary(version=version, artists=artists, songs=songs, tags=tags)
    
    def filter_song_by_tags(self, tags: set[str]) -> List[MusicLibrarySong]:
        """Get all songs with the tags specified."""
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

    def get_song_by_name(self, name: str) -> MusicLibrarySong | None:
        """Get song by it's name."""
        for song in self.songs.values():
            if song.name.lower() == name.lower():
                return song
        return None

    def get_song_by_id(self, id: int) -> MusicLibrarySong | None:
        """Get song by it's ID."""
        for song in self.songs.values():
            if id == song.id:
                return song
        return None
    
    def search_songs(self, query: str) -> list[MusicLibrarySong]:
        """Search songs by name."""
        query = query.rstrip()
        songs = []

        for song in self.songs.values():
            if query.lower() in song.name.lower():
                songs.append(song)
        return songs
    
    def filter_song_by_artist(self, artist: str) -> list[MusicLibrarySong]:
        """Get song by the name of the artist."""
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
class SFXLibrary:
    version: int
    folders: List['SFXLibraryFolder']
    creators: List['SFXLibraryCreator']

    @staticmethod
    def from_raw(raw_str: str) -> 'SFXLibrary':
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
                folder = SFXLibraryFolder.from_raw(folder_str)
                if folder.id == 1:
                    version_name = folder.name  # Folder with id 1 contains the version name
                else:
                    folders.append(folder)

        # Inject SFX into the appropriate folders
        for raw_sfx in parsed_sfx:
            try:
                is_not_folder = raw_sfx.strip().split(",")[2] != "1"
            except IndexError:
                is_not_folder = False

            if is_not_folder:
                parsed_sfx_obj = SFX.from_raw(raw_sfx)
                sfx_folder_id = parsed_sfx_obj.parent_folder_id

                for folder in folders:
                    if folder.id == sfx_folder_id:
                        folder.inject_sfx(raw_sfx)
                        break

        creators = [SFXLibraryCreator.from_raw(creator) for creator in parsed_creators if creator != ""]

        return SFXLibrary(version=int(version_name), folders=folders, creators=creators)

    def get_folder_by_name(self, name: str):
        for folder in self.folders:
            if folder.name == name:
                return folder
        return None


@dataclass
class SFXLibraryCreator:
    name: str
    url: str

    @staticmethod
    def from_raw(raw_str: str) -> 'SFXLibraryCreator':
        parsed = raw_str.strip().split(",")
        return SFXLibraryCreator(
            name=parsed[0],
            url=unquote(parsed[1])
        )

@dataclass
class SFX:
    id: int
    name: str
    parent_folder_id: str
    file_size: float
    url: str
    duration: timedelta

    @staticmethod
    def from_raw(raw_str: str) -> 'SFX':
        parsed = raw_str.strip().split(",")
        return SFX(
            id=int(parsed[0]),
            name=parsed[1],
            parent_folder_id=int(parsed[3]),
            file_size=float(parsed[4]),
            url=f"https://geometrydashfiles.b-cdn.net/sfx/s{parsed[0]}.ogg",
            duration=timedelta(seconds=int(parsed[5])//100)
        )

@dataclass
class SFXLibraryFolder:
    id: int
    name: str
    sfx: List[SFX] = field(default_factory=list)  # Initialize sfx list

    @staticmethod
    def from_raw(raw_str: str) -> 'SFXLibraryFolder':
        parsed = raw_str.strip().split(",")
        return SFXLibraryFolder(
            id=int(parsed[0]),
            name=parsed[1],
        )
    
    def inject_sfx(self, raw_str_song: str) -> None:
        """Helper function to add a sound effect to the folder."""
        injected_sfx: SFX = SFX.from_raw(raw_str_song)

        if injected_sfx.parent_folder_id != self.id:  # Compare folder names
            raise ValueError(f"Cannot inject an sfx that belongs to a different folder ({injected_sfx.parent_folder.name}).")
        
        self.sfx.append(injected_sfx)

    def get_song_by_name(self, name: str) -> SFX:
        """Find a sound effect by name."""
        for sfx in self.sfx:
            if sfx.name == name:
                return sfx
        return None
    
    def get_song_by_id(self, id: int) -> SFX | None:
        """Find a sound effect by id."""
        for sfx in self.sfx:
            if sfx.id == id:
                return sfx
        return None


# Level song

@dataclass
class LevelSong:
    id: int
    name: str
    artist_id: Optional[int]
    artist_name: Optional[str]
    artist_verified: Optional[bool]
    song_size_mb: float
    youtube_link: Optional[str]
    song_link: Optional[str]
    is_ncs: Optional[bool]
    is_library_song: Optional[bool]

    @staticmethod
    def from_raw(raw_str: str) -> 'LevelSong':
        parsed = parse_song_data(raw_str.strip())
        return LevelSong(
            id=int(parsed.get('1')),
            name=parsed.get('2'),
            artist_id=parsed.get('3'),
            artist_name=parsed.get('4'),
            artist_verified=parsed.get('8') == 1,
            song_size_mb=float(parsed.get('5', 0.0)),
            youtube_link=f"https://youtu.be/watch?v={parsed.get('6')}" if parsed.get("6") else None,
            song_link=unquote(parsed.get("10", '')) if parsed.get("10") else None,
            is_ncs=parsed.get('11') == 1,
            is_library_song=int(parsed.get('1')) >= 10000000
        )

class OfficialSong(Enum):
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
    EXPLORERS = 22

        



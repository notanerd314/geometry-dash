from urllib.parse import unquote
from typing import Dict, Optional, List
from datetime import timedelta
from ..ext import *
from dataclasses import dataclass, field
from enum import Enum

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
            website=parsed[2] if parsed[2].strip() else None,
            youtube_channel_id=parsed[3] if parsed[3].strip() else None
        )

@dataclass
class MusicLibrarySong:
    id: int
    name: str
    artist: Optional[MusicLibraryArtist]
    file_size_bytes: float
    duration_seconds: timedelta
    is_ncs: bool

    @staticmethod
    def from_raw(raw_str: str, artists: Dict[int, MusicLibraryArtist]) -> 'MusicLibrarySong':
        parsed = raw_str.strip().split(",")
        artist_id = int(parsed[2]) if parsed[2].strip() else None
        return MusicLibrarySong(
            id=int(parsed[0]),
            name=parsed[1],
            artist=artists.get(artist_id),
            file_size_bytes=float(parsed[3]),
            duration_seconds=timedelta(seconds=int(parsed[4])),
            is_ncs=parsed[6] == '1'
        )

@dataclass
class MusicLibraryTag:
    id: int
    name: str

    @staticmethod
    def from_raw(raw_str: str) -> 'MusicLibraryTag':
        parsed = raw_str.strip().split(",")
        return MusicLibraryTag(
            id=int(parsed[0]),
            name=parsed[1]
        )

@dataclass
class MusicLibrary:
    version: int
    artists: Dict[int, MusicLibraryArtist] = field(default_factory=dict)
    songs: Dict[int, MusicLibrarySong] = field(default_factory=dict)
    tags: Dict[int, MusicLibraryTag] = field(default_factory=dict)

    @staticmethod
    def from_raw(raw_str: str) -> 'MusicLibrary':
        parsed = raw_str.strip().split("|")
        version = int(parsed[0])

        artists = {
            int(artist.split(",")[0]): MusicLibraryArtist.from_raw(artist)
            for artist in parsed[1].split(";") if artist.strip()
        }

        songs = {
            int(song.split(",")[0]): MusicLibrarySong.from_raw(song, artists)
            for song in parsed[2].split(";") if song.strip()
        }

        tags = {
            int(tag.split(",")[0]): MusicLibraryTag.from_raw(tag)
            for tag in parsed[3].split(";") if tag.strip()
        }

        return MusicLibrary(version=version, artists=artists, songs=songs, tags=tags)

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
    STAY_INSIDE_ME = LevelSong(id=-1, name="Stay Inside Me", artist_name="OcularNebula")
    STEREO_MADNESS = LevelSong(id=0, name="Stereo Madness", artist_name="ForeverBound")
    BACK_ON_TRACK = LevelSong(id=1, name="Back On Track", artist_name="DJVI")
    POLARGEIST = LevelSong(id=2, name="Polargeist", author_name="Step")
    DRY_OUT = LevelSong(id=3, name="Dry Out", artist_name="DJVI")
    BASE_AFTER_BASE = LevelSong(id=4, name="Base after Base", artist_name="DJVI")
    CANT_LET_GO = LevelSong(id=5, name="Cant Let Go", artist_name="DJVI")
    JUMPER = LevelSong(id=6, name="Jumper", artist_name="Waterflame")
    TIME_MACHINE = LevelSong(id=7, name="Time Machine", artist_name="Waterflame")
    CYCLES = LevelSong(id=8, name="Cycles", artist_name="DJVI")
    XSTEP = LevelSong(id=9, name="xStep", artist_name="DJVI")
    CLUTTERFUNK = LevelSong(id=10, name="Clutterfunk", artist_name="Waterflame")
    THEORY_OF_EVERYTHING = LevelSong(id=11, name="Theory of Everything", artist_name="DJ-Nate")
    ELECTROMAN_ADVENTURES = LevelSong(id=12, name="Electroman Advantures", artist_name="Waterflame")
    CLUBSTEP = LevelSong(id=13, name="Clubstep", artist_name="DJ-Nate")
    ELECTRODYNAMIX = LevelSong(id=14, name="Electrodynamix", artist_name="DJ-Nate")
    HEXAGON_FORCE = LevelSong(id=15, name="Hexagon Force", artist_name="Waterflame")
    BLAST_PROCESSING = LevelSong(id=16, name="Blast Processing", artist_name="Waterflame")
    THEORY_OF_EVERYTHING_2 = LevelSong(id=17, name="Theory of Everything 2", artist_name="DJ-Nate")
    GEOMETRICAL_DOMINATOR = LevelSong(id=18, name="Geometrical Dominator", artist_name="Waterflame")
    DEADLOCKED = LevelSong(id=19, name="Deadlocked", artist_name="F-777")
    FINGERDASH = LevelSong(id=20, name="Fingerdash", artist_name="MDK")
    DASH = LevelSong(id=21, name="Dash", artist_name="MDK")
    EXPLORERS = LevelSong(id=22, name="Explorers", artist_name="Hinkik")
    
    @classmethod
    def from_id(cls, id: int) -> type[Enum]:
        for song in cls:
            if song.value.id == id:
                return song
        raise ValueError("Song not found!")
        



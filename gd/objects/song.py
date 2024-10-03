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

        



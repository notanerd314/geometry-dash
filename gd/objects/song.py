from urllib.parse import unquote
from typing import Dict, Optional, List
from ..ext import *
from datetime import timedelta

class MusicLibrary:
    class Artist:
        def __init__(self, raw_str: str):
            self.raw = raw_str.strip()  # Trim whitespace
            self.parsed = self.raw.split(",")
            
            self.id = int(self.parsed[0])
            self.name = self.parsed[1]
            self.website = self.parsed[2] if self.parsed[2].strip() else None
            self.youtube_channel_id = self.parsed[3] if self.parsed[3].strip() else None

    class Song:
        def __init__(self, raw_str: str, library_instance: 'MusicLibrary'):
            self.raw = raw_str.strip()  # Trim whitespace
            self.parsed = self.raw.split(",")
            self.id: int = int(self.parsed[0])
            self.name: str = self.parsed[1]

            # Safely access the artist
            artist_id = self.parsed[2].strip() if self.parsed[2] != " NOEP)" else None
            self.artist: MusicLibrary.Artist = library_instance.artists.get(artist_id) if artist_id else None
            
            self.file_size_bytes: float = float(self.parsed[3])
            self.duration_seconds: timedelta = timedelta(seconds=int(self.parsed[4]))
            self.is_ncs: bool = self.parsed[6] == '1'  # More concise boolean expression
    
    class Tag:
        def __init__(self, raw_str: str):
            self.raw = raw_str.strip()  # Trim whitespace
            self.parsed = self.raw.split(",")
            
            self.id: int = int(self.parsed[0])
            self.name: str = self.parsed[1]

    def __init__(self, raw_str: str):
        self.raw = raw_str.strip()  # Trim whitespace
        self.parsed = self.raw.split("|")

        self.version: int = int(self.parsed[0])
        self.artists: Dict[str, self.Artist] = {}
        for artist in self.parsed[1].split(";"):
            if artist.strip():
                self.artists[artist.split(",")[0]] = self.Artist(artist)

        self.songs: Dict[str, self.Song] = {}
        for song in self.parsed[2].split(";"):
            if song.strip():
                self.songs[song.split(",")[0]] = self.Song(song, self)

        self.tags_list: Dict[str, self.Tag] = {}
        for tag in self.parsed[3].split(";"):
            if tag.strip():
                self.tags_list[tag.split(",")[1]] = self.Tag(tag)


class NewgroundsSong:
    """Class representation of a Newgrounds song."""
    
    def __init__(self, raw_str: str) -> None:
        self.raw = raw_str.strip()  # Trim whitespace
        self.parsed = parse_song_data(self.raw)

        self.newgrounds_id: Optional[int] = self.parsed.get('1')
        self.name: Optional[str] = self.parsed.get('2')
        self.artist_id: Optional[int] = self.parsed.get('3')
        self.artist_name: Optional[str] = self.parsed.get('4')
        self.artist_verified: bool = bool(self.parsed.get('8') == 1)

        self.song_size_mb: float = float(self.parsed.get('5', 0.0))
        self.youtube_link: Optional[str] = f"https://youtu.be/watch?v={self.parsed.get('7')}" if self.parsed.get("7") else None
        self.newgrounds_link: Optional[str] = unquote(self.parsed.get("10", '')) if self.parsed.get("10") else None

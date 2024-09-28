from urllib.parse import unquote
from typing import *
from ..ext import *
from datetime import timedelta

class MusicLibrary:
    class Artist:
        def __init__(self, raw_str: str):
            self.raw = raw_str
            self.parsed = self.raw.split(",")
            
            self.id = int(self.parsed[0])
            self.name = self.parsed[1]
            self.website = self.parsed[2] if self.parsed[2] != " " else None
            self.youtube_channel_id = self.parsed[3] if self.parsed[3] != " " else None

    class Song:
        def __init__(self, raw_str: str, library_instance: 'MusicLibrary'):
            self.raw = raw_str
            self.parsed = self.raw.split(",")
            self.id: int = int(self.parsed[0])
            self.name: str = self.parsed[1]

            try:
                self.artist: MusicLibrary.Artist = library_instance.artists[self.parsed[2]] if self.parsed[2] != " NOEP)" else None
            except KeyError:
                self.artist = None
            self.file_size_bytes: float = float(self.parsed[3])
            self.duration_seconds: timedelta = timedelta(seconds=int(self.parsed[4]))
            # self.tags: list[MusicLibrary.Tag] = [library_instance.tags_list[tag] for tag in self.parsed[5].split('.')]
            self.is_ncs: bool = True if self.parsed[6] == '1' else False
    
    class Tag:
        def __init__(self, raw_str: str):
            self.raw = raw_str
            self.parsed = self.raw.split(",")
            
            self.id: int = int(self.parsed[0])
            self.name: str = self.parsed[1]

    def __init__(self, raw_str: str):
        self.raw = raw_str
        self.parsed = self.raw.split("|")

        self.version: int = int(self.parsed[0])
        self.artists: Dict[str, self.Artist] = {}
        for artist in self.parsed[1].split(";"):
            if artist:
                self.artists[artist.split(",")[0]] = self.Artist(artist)

        self.songs: Dict[str, self.Song] = {}
        for song in self.parsed[2].split(";"):
            if song:
                self.songs[song.split(",")[0]] = self.Song(song, self)

        self.tags_list: Dict[str, self.Tag] = {}
        for tag in self.parsed[3].split(";"):
            if tag:
                self.tags_list[tag.split(",")[1]] = self.Tag(tag)



class NewgroundsSong:
    """
    The class representation of a Newgrounds song.

    Parameters:
    - raw_str (str): The song string data from the server.
    """

    def __init__(self, raw_str: str) -> None:
        self.raw = raw_str
        self.parsed = parse_song_data(self.raw)

        self.newgrounds_id: Optional[int] = self.parsed.get('1')
        self.name: Optional[str] = self.parsed.get('2')
        self.artist_id: Optional[int] = self.parsed.get('3')
        self.artist_name: Optional[str] = self.parsed.get('4')
        self.artist_verified: bool = bool(self.parsed.get('8') == 1)

        self.song_size_mb: float = float(self.parsed.get('5', 0.0))
        self.youtube_link: Optional[str] = f"https://youtu.be/watch?v={self.parsed['7']}" if self.parsed.get("7") else None
        self.newgrounds_link: Optional[str] = unquote(self.parsed["10"]) if self.parsed.get("10") else None
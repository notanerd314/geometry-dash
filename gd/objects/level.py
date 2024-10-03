from ..ext import *
from .enums import *
from typing import List, Optional, Union
from .song import *
from dataclasses import dataclass, field

@dataclass
class DownloadedLevel:
    """
    A class representing a downloaded level in Geometry Dash.
    
    ### Attributes:
        - `raw_str` (str): The raw string containing level data.
        - `id` (Optional[int]): The unique ID of the level.
        - `name` (Optional[str]): The name of the level.
        - `description` (Optional[str]): A description of the level.
        - `level_data` (Optional[str]): The data representing the level structure.
        - `version` (Optional[int]): The version of the level.
        - `creator_id` (Optional[int]): The ID of the level creator.
        - `downloads` (int): The number of times the level has been downloaded.
        - `likes` (Optional[int]): The number of likes the level has received.
        - `copyable` (bool): Whether the level is copyable or not.
        - `length` ('Length'): The length of the level.
        - `requested_stars` (Optional[int]): The number of stars the creator has requested for the level.
        - `stars` (Optional[int]): The number of stars the level has been awarded.
        - `coins` (int): The number of coins in the level.
        - `custom_song_id` (Optional[int]): The ID of the custom song used in the level.
        - `song_list_ids` (List[int]): The list of song IDs used in the level.
        - `sfx_list_ids` (List[int]): The list of sound effect IDs used in the level.
        - `daily_id` (int): The ID of the daily challenge the level is part of.
        - `copied_level_id` (Optional[int]): The ID of the level from which this level was copied.
        - `low_detail_mode` (bool): Whether the level has a low-detail mode.
        - `two_player_mode` (bool): Whether the level supports two-player mode.
        - `verified_coins` (bool): Whether the coins in the level have been verified.
        - `in_gauntlet` (bool): Whether the level is part of a gauntlet challenge.
        - `daily` (bool): Whether the level is a daily challenge.
        - `weekly` (bool): Whether the level is a weekly challenge.
        - `rating` ('LevelRating'): The rating of the level.
        - `difficulty` ('Difficulty'): The difficulty level of the level.
        - `level_password` (Optional[str]): The password for editing the level, if applicable.
        - `official_song` (Optional[OfficialSong]): The official song used in the level, if applicable.
    
    ### Methods:
        - `from_raw`: Parses a raw level string into a `DownloadedLevel` object.
        - `_parse_comma_separated_int_list`: Helper method to parse comma-separated integers from a string.
        - `_determine_rating`: Determines the rating of the level based on parsed data.
        - `_determine_difficulty`: Determines the difficulty of the level based on parsed data.
    """
    
    raw_str: str
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    level_data: Optional[str]
    version: Optional[int]
    creator_id: Optional[int]
    downloads: int
    likes: Optional[int]
    copyable: bool
    length: 'Length'
    requested_stars: Optional[int]
    stars: Optional[int]
    coins: int
    custom_song_id: Optional[int]
    song_list_ids: List[int]
    sfx_list_ids: List[int]
    daily_id: int
    copied_level_id: Optional[int]
    low_detail_mode: bool
    two_player_mode: bool
    verified_coins: bool
    in_gauntlet: bool
    daily: bool
    weekly: bool
    rating: 'LevelRating'
    difficulty: 'Difficulty'
    level_password: Optional[str]
    official_song: Optional[OfficialSong]

    @staticmethod
    def from_raw(raw_str: str) -> 'DownloadedLevel':
        """
        Converts a raw level string into a DownloadedLevel object.
        
        Args:
            raw_str (str): The raw string representing the level data.
            
        Returns:
            DownloadedLevel: A `DownloadedLevel` instance created from the parsed data.
        """

        if not isinstance(raw_str, str):
            raise ValueError("Level string must be a str!")

        parsed = parse_level_data(raw_str)
        return DownloadedLevel(
            raw_str=raw_str,
            id=parsed.get("1"),
            name=parsed.get("2"),
            description=parsed.get("3"),
            level_data=parsed.get("4"),
            version=parsed.get("5"),
            creator_id=parsed.get("6"),
            downloads=parsed.get("10", 0),
            likes=parsed.get("14"),
            copyable=bool(parsed.get("27")),
            length=Length(parsed.get("15")),
            requested_stars=parsed.get("39"),
            stars=parsed.get("18"),
            coins=parsed.get("37", 0),
            custom_song_id=parsed.get("35", None),
            song_list_ids=DownloadedLevel._parse_comma_separated_int_list(parsed.get("52")),
            sfx_list_ids=DownloadedLevel._parse_comma_separated_int_list(parsed.get("53")),
            daily_id=parsed.get("41", -1),
            copied_level_id=parsed.get("30"),
            low_detail_mode=bool(parsed.get("40")),
            two_player_mode=bool(parsed.get("31")),
            verified_coins=bool(parsed.get("38")),
            in_gauntlet=bool(parsed.get("44")),
            daily=0 <= parsed.get("41", -1) <= 100000,
            weekly=parsed.get("41", -1) >= 100000,
            rating=DownloadedLevel._determine_rating(parsed),
            difficulty=DownloadedLevel._determine_difficulty(parsed),
            level_password=None if isinstance(parsed.get("27"), bool) else parsed.get("27"),
            official_song=OfficialSong(parsed.get("12")) if parsed.get("12") else None
        )

    @staticmethod
    def _parse_comma_separated_int_list(key: str) -> List[int]:
        """
        Helper method to parse a comma-separated list of integers.
        
        Args:
            key (str): A string containing integers separated by commas.
            
        Returns:
            List[int]: A list of parsed integers.
        """
        try:
            return [int(x) for x in key.split(",") if x.isdigit()]
        except AttributeError:
            return []

    @staticmethod
    def _determine_rating(parsed) -> LevelRating:
        """
        Determines the level's rating based on parsed data.
        
        Args:
            parsed (dict): The parsed level data.
            
        Returns:
            LevelRating: The rating of the level.
        """

        if parsed.get("42", 0) >= 1:
            return LevelRating(parsed.get("42"))
        elif parsed.get("19", 0) >= 1:
            return LevelRating.FEATURED
        elif parsed.get("18", 0) != 0:
            return LevelRating.RATED
        
        return LevelRating.NO_RATE

    @staticmethod
    def _determine_difficulty(parsed) -> Difficulty:
        """
        Determines the level's difficulty based on parsed data.
        
        Args:
            parsed (dict): The parsed level data.
            
        Returns:
            Difficulty: The difficulty of the level.
        """

        if parsed.get("17"):
            return Difficulty(6 + parsed.get("43", 0) / 10)
        elif parsed.get("25"):

            return Difficulty.AUTO
        return Difficulty(parsed.get("9", 0) / 10)


@dataclass
class SearchedLevel(DownloadedLevel):
    """
    A class representing a level searched in Geometry Dash.
    
    ### Attributes:
        - `creator_name` (Optional[str]): The name of the level's creator.
        - `song_data` ('LevelSong'): Data about the song used in the level.
    
    ### Methods:
        - `from_raw`: Creates a `SearchedLevel` object from raw level data.
    """

    creator_name: Optional[str]
    song_data: 'LevelSong'

    @staticmethod
    def from_raw(parsed_str: dict) -> 'SearchedLevel':
        """
        Converts parsed level data into a SearchedLevel object.
        
        Args:
            parsed_str (dict): A dictionary containing parsed level data.
            
        Returns:
            SearchedLevel: A `SearchedLevel` instance created from the parsed data.
        """

        instance = DownloadedLevel.from_raw(parsed_str['level'])
        creator_name = parsed_str["creator"]["playerName"]
        song_data = LevelSong.from_raw(parsed_str["song"])
        
        return SearchedLevel(
            raw_str=parsed_str['level'],
            id=instance.id,
            name=instance.name,
            description=instance.description,
            version=instance.version,
            creator_id=instance.creator_id,
            downloads=instance.downloads,
            likes=instance.likes,
            copyable=instance.copyable,
            length=instance.length,
            requested_stars=instance.requested_stars,
            stars=instance.stars,
            coins=instance.coins,
            custom_song_id=instance.custom_song_id,
            copied_level_id=instance.copied_level_id,
            two_player_mode=instance.two_player_mode,
            verified_coins=instance.verified_coins,
            in_gauntlet=instance.in_gauntlet,
            daily=instance.daily,
            weekly=instance.weekly,
            rating=instance.rating,
            difficulty=instance.difficulty,
            creator_name=creator_name,
            song_data=song_data,
            level_data=None,
            song_list_ids=None,
            sfx_list_ids=None,
            daily_id=None,
            low_detail_mode=None,
            level_password=None,
        )

    # Note: Ensure LevelSong also has a `from_raw` method defined accordingly.

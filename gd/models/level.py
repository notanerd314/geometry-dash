"""
## .models.level

A module containing all the classes and methods related to levels in Geometry Dash.
"""

from ..helpers import *
from .enums import *
from .icons import *
from typing import List, Optional, Union
from .song import *
from dataclasses import dataclass

@dataclass
class DownloadedLevel:
    """
    A class representing a downloaded level in Geometry Dash.
    
    Attributes:
    ----------
    raw_str : str
        The original unparsed data from the servers.
    id : int
        The ID of the level.
    name : str
        The name of the level.
    description : str
        The description of the level.
    level_data : str
        The level's data.
    version : int
        The level's version.
    creator_id : int
        The ID of the creator of the level.
    downloads : int
        The download count of the level.
    likes : int
        The like count of the level.
    copyable : bool
        Whether the level can be copied or not.
    length : Length
        The length of the level. (Not the exact length)
    requested_stars : Optional[int]
        The level rating requested by the creator.
    stars : Optional[int]
        The star count for the level.
    coins : int
        The coins count for the level.
    custom_song_id : Union[int, None]
        The id for the custom song used for the level.
    song_list_ids : List[int]
        The list of the song IDs used in the level.
    sfx_list_ids : List[int]
        The list of the song IDs used in the level.
    is_daily : bool
        If the level was a daily level.
    is_weekly : bool
        If the level was a weekly level.
    rating : LevelRating
        The rating of the level. (None, Featured, Epic, etc.)
    difficulty : Difficulty
        The difficulty of the level.
    level_password: Union[int, None]
        The password for the level to copy.
    official_song: Union[OfficialSong, None]
        The official song used in the level. Returns None if the level uses a custom song.
    
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
    custom_song_id: Union[int, None]
    song_list_ids: List[int]
    sfx_list_ids: List[int]
    daily_id: int
    copied_level_id: Optional[int]
    low_detail_mode: bool
    two_player_mode: bool
    verified_coins: bool
    in_gauntlet: bool
    is_daily: bool
    is_weekly: bool
    rating: 'LevelRating'
    difficulty: 'Difficulty'
    level_password: Optional[str]
    official_song: Optional[OfficialSong]

    @staticmethod
    def from_raw(raw_str: str) -> 'DownloadedLevel':
        """
        A staticmethod that converts a raw level string into a DownloadedLevel object.
        
        :param raw_str: The raw string returned from the server.
        :type raw_str: str
        :return: A DownloadedLevel object created from the parsed data.
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
            is_daily=0 <= parsed.get("41", -1) <= 100000,
            is_weekly=parsed.get("41", -1) >= 100000,
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
    A class representing a level searched in Geometry Dash. It's a child class from DownloadedLevel.

    Note that some of the attributes that belong to DownloadedLevel were not present in SearchedLevel
    
    Attributes
    ----------
    creator_name : Optional[str]
        The creator name of the level.
    song_data : LevelSong
        The song object of the level.
    """

    creator_name: Optional[str]
    song_data: 'LevelSong'

    @staticmethod
    def from_dict(parsed_str: dict) -> 'SearchedLevel':
        """
        A staticmethod that converts parsed dict level data into a SearchedLevel object.
        
        :param parsed_str: The parsed str returned.
        :type parsed_str: dict
        :return: A SearchedLevel object created from the parsed data.
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
            is_daily=instance.daily,
            is_weekly=instance.weekly,
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

@dataclass
class LevelComment:
    """
    A class representing a comment in a level.

    Attributes
    ----------
    level_id : int
        The ID of the level the comment belongs to.
    content : str
        The content of the comment.
    likes : int
        The current likes count for the comment.
    comment_id : int
        The ID of the comment.
    is_spam : bool
        If the comment is spam.
    posted_ago : str
        The time the comment was posted in a human-readable format. Eg: `"5 months"`
    precentage : int
        The perecentage of the comment.
    mod_level : ModLevel
        The mod level of the author.
    author_player_id : int
        The ID of the author's player.
    author_account_id : int
        The ID of the author's account.
    author_name : str
        The name of the author.
    author_primary_color : Color
        The primary color of the author.
    author_secondary_color : Color
        The secondary color of the author.
    author_has_glow : bool
        If the author has a glow effect.
    author_icon : Icon
        The icon of the author.
    author_icon_display_gamemode : Gamemode
        The gamemode the author chooses to display in their comment.
    """
    level_id: int
    content: str
    likes: int
    comment_id: int
    is_spam: bool
    posted_ago: str
    precentage: int
    mod_level: ModLevel

    author_player_id: int
    author_account_id: int
    author_name: str
    author_primary_color: Color
    author_secondary_color: Color
    author_has_glow: bool
    author_icon: Icon
    author_icon_display_gamemode: Gamemode

    @staticmethod
    def from_raw(raw_str: str) -> 'LevelComment':
        """
        A staticmethod that parses the raw string and returns a LevelComment object.

        :param raw_str: Raw data returned from the servers.
        :type raw_str: str
        :return: A LevelComment object created from the raw data.
        """

        parsed = raw_str.split(":")
        user_value = parse_key_value_pairs(parsed[1], "~")
        comment_value = parse_key_value_pairs(parsed[0], '~')

        return LevelComment(
            level_id=int(comment_value.get("1", 0)),
            content=decrypt_data(comment_value.get("2", "")),
            author_player_id=int(comment_value.get("3", 0)),
            author_account_id=int(str(user_value.get("16", 0)).split("#")[0]),
            likes=int(comment_value.get("4", 0)),
            message_id=int(comment_value.get("6", 0)),
            is_spam=bool(int(comment_value.get("7", 0))),
            posted_ago=comment_value.get("9", None),
            precentage=int(comment_value.get("10", 0)),
            mod_level=ModLevel(int(comment_value.get("11", 0))),

            author_name=user_value.get("1", ""),
            author_icon=Icon(user_value.get("9", ""), gamemode=Gamemode(int(user_value.get("14", 0)))),
            author_icon_display_gamemode=Gamemode(int(user_value.get("14", 0))),
            author_primary_color=Color(int(user_value.get("10", 1)), ColorType.primary),
            author_secondary_color=Color(int(user_value.get("11", 1)), ColorType.secondary),
        )
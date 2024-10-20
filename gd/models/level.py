"""
## .models.level

A module containing all the classes and methods related to levels in Geometry Dash.
"""

from ..helpers import *
from .enums import *
from .icons import *
from typing import List, Optional, Union, Tuple
from .song import LevelSong, OfficialSong
from datetime import datetime
from dataclasses import dataclass
from json import load
from os import path

relative_path = path.dirname(__file__)

with open(path.join(relative_path, "spreadsheet", "gauntlets.json"), 'r') as guantlets_names_file:
    guantlets_names = load(guantlets_names_file)

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
    creator_player_id : int
        The player ID of the creator of the level.
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
    difficulty : Union[Difficulty, DemonDifficulty]
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
    creator_player_id: Optional[int]
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
            creator_player_id=parsed.get("6"),
            downloads=parsed.get("10", 0),
            likes=parsed.get("14"),
            copyable=bool(parsed.get("27")),
            length=Length(parsed.get("15")),
            requested_stars=parsed.get("39"),
            stars=parsed.get("18"),
            coins=parsed.get("37", 0),
            custom_song_id=parsed.get("35", None),
            song_list_ids=parse_comma_separated_int_list(parsed.get("52")),
            sfx_list_ids=parse_comma_separated_int_list(parsed.get("53")),
            daily_id=parsed.get("41", -1),
            copied_level_id=parsed.get("30"),
            low_detail_mode=bool(parsed.get("40")),
            two_player_mode=bool(parsed.get("31")),
            verified_coins=bool(parsed.get("38")),
            in_gauntlet=bool(parsed.get("44")),
            is_daily=0 <= parsed.get("41", -1) <= 100000,
            is_weekly=parsed.get("41", -1) >= 100000,
            rating=DownloadedLevel._determine_rating(parsed),
            difficulty=determine_difficulty(parsed),
            level_password=None if isinstance(parsed.get("27"), bool) else parsed.get("27"),
            official_song=OfficialSong(parsed.get("12")) if parsed.get("12") else None
        )

    @staticmethod
    def _determine_rating(parsed: dict) -> LevelRating:
        """d
        Determines the level's rating based on parsed data.
        
        :param parsed: Parsed data from the servers
        :type parsed: dict
        :return: `LevelRating`
        """

        if parsed.get("42", 0) >= 1:
            return LevelRating(parsed.get("42"))
        elif parsed.get("19", 0) >= 1:
            return LevelRating.FEATURED
        elif parsed.get("18", 0) != 0:
            return LevelRating.RATED
        
        return LevelRating.NO_RATE


@dataclass
class SearchedLevel(DownloadedLevel):
    """
    A class representing a level searched in Geometry Dash. It's a child class from DownloadedLevel.

    Note that some of the attributes that belong to DownloadedLevel were not present in SearchedLevel
    
    Attributes
    ----------
    creator_name : Optional[str]
        The creator name of the level.
    creator_account_id : Optional[int]
        The creator's account ID.
    song_data : Union[LevelSong, None]
        The custom song object of the level.
    """

    creator_name: Optional[str]
    creator_account_id: Optional[int]
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
        creator_account_id = parsed_str["creator"]["accountID"]
        song_data = LevelSong.from_raw(parsed_str["song"]) if parsed_str["song"] else None
        
        return SearchedLevel(
            raw_str=parsed_str['level'],
            id=instance.id,
            name=instance.name,
            description=instance.description,
            version=instance.version,
            creator_player_id=instance.creator_player_id,
            creator_account_id=creator_account_id,
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
            is_daily=instance.is_daily,
            is_weekly=instance.is_weekly,
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
            official_song=instance.official_song
        )

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
    author_primary_color_id: int
    author_secondary_color_id: int
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
            comment_id=int(comment_value.get("6", 0)),
            is_spam=bool(int(comment_value.get("7", 0))),
            posted_ago=comment_value.get("9", None),
            precentage=int(comment_value.get("10", 0)),
            mod_level=ModLevel(int(comment_value.get("11", 0))),

            author_name=user_value.get("1", ""),
            author_icon=Icon(
                user_value.get("9", ""), gamemode=Gamemode(int(user_value.get("14", 0))), 
                primary_color_id=int(user_value.get("10", 1)), secondary_color_id=int(user_value.get("11", 1))
            ),
            author_icon_display_gamemode=Gamemode(int(user_value.get("14", 0))),
            author_primary_color_id=int(user_value.get("10", 1)),
            author_secondary_color_id=int(user_value.get("11", 1)),
            author_has_glow=bool(int(user_value.get("15", 0)))
        )
    
@dataclass
class __ListOfLevels__:
    """
    A class representing a list of levels. (Used for inheritance, not for API.)
    
    Attributes
    ----------
    id : int
    name : str
    level_ids : List[int]
    """
    id: int
    name: str
    level_ids: List[int]

    async def get_display_info_all_levels(self) -> Tuple[SearchedLevel]:
        """
        A coroutine method that fetches and returns all the levels in the level list with their display information.
        
        :return: A tuple of SearchedLevel objects.
        """
        str_ids = ','.join([str(level) for level in self.levels_id])
        search_raw = await send_post_request(
            url="http://www.boomlings.com/database/getGJLevels21.php",
            data={'secret': "Wmfd2893gb7", "str": str_ids, "type": 10}
        )
        search_parsed = parse_search_results(search_raw)
        level_list = [SearchedLevel.from_dict(level) for level in search_parsed]
        return level_list
    
    async def download_level_by_index(self, index: int) -> DownloadedLevel:
        """
        A coroutine method that downloads a level from the level list based on the index.
        
        :param index: The index of the level to download.
        :type index: int
        :return: A DownloadedLevel object representing the downloaded level.
        """
        if index < 0 or index >= len(self.levels_id):
            raise IndexError("Invalid level index, index limit is 4.")
        
        level_id = self.levels_id[index]
        download_raw = await send_post_request(
            url="http://www.boomlings.com/database/downloadGJLevel22.php",
            data={'secret': "Wmfd2893gb7", "levelID": level_id}
        )
        return DownloadedLevel.from_raw(download_raw)

@dataclass
class LevelList(__ListOfLevels__):
    """
    A class representing a list.

    Attributes
    ----------
    id : int
        The list ID.
    name : str
        The name of the list.
    description : str
        The description of the list.
    difficulty : Difficulty
        The difficulty of the list.
    downloads : int
        The amount of downloads in the list.
    likes : int
        The amount of likes in the list.
    is_rated : bool
        If the level has a rating.
    upload_date : datetime
        The upload date of the list.
    last_update_date : datetime
        The last update date of the list
    author_account_id : int
        The author's account ID.
    author_name : str
        The author's name.
    level_ids : List[int]
        The list of level IDs inside the list.
    diamonds : int
        The amount of diamonds given when completing the list.
    minimum_levels : int
        The minimum of levels required to complete the list. 
    """

    description: str
    difficulty: Difficulty
    downloads: int
    likes: int
    is_rated: bool
    upload_date: datetime
    last_update_date: datetime
    author_account_id: int
    author_name: str
    diamonds: int
    minimum_levels: int

    @staticmethod
    def from_raw(raw_str: str) -> 'LevelList':
        """
        Converts a raw string to a LevelList object.

        :param raw_str: Raw data returned from the servers.
        :type raw_str: str
        :return: A LevelList object created from the raw data.
        """
        parsed = parse_key_value_pairs(raw_str)

        return LevelList(
            id=int(parsed.get("1", 0)),
            name=parsed.get("2", ""),
            level_ids=parse_comma_separated_int_list(parsed.get("51", "")),
            description=decrypt_data(parsed.get("3", "")),
            difficulty=determine_list_difficulty(parsed.get("7", None)),
            downloads=int(parsed.get("10", 0)),
            likes=int(parsed.get("14", 0)),
            is_rated=True if parsed.get("19") else False,
            upload_date=datetime.fromtimestamp(int(parsed.get("28", 0))),
            last_update_date=datetime.fromtimestamp(int(parsed.get("29", 0))),
            author_account_id=int(parsed.get("49", 0)),
            author_name=parsed.get("50", ""),
            diamonds=int(parsed.get("55", 0)),
            minimum_levels=int(parsed.get("56", 0))
        )

@dataclass
class MapPack(__ListOfLevels__):
    """
    A class representing a map pack.

    Attributes
    ----------
    id : int
        ID of the map pack
    name : str
        Name of the map pack
    level_ids : List[int]
        The list of the levels' id.
    stars : int
        The star count of the map pack
    coins : int
        The coin count of the map pack
    difficulty : Difficulty
        The difficulty of the map pack (`HARD_DEMON` it's just `DEMON`)
    text_rgb_color : List[int]
        The rgb color of the map pack's text
    progress_bar_rgb_color : List[int]
        The rgb color of the map pack's progress bar
    """

    stars: int
    coins: int
    difficulty: Difficulty
    text_rgb_color: List[int]
    progress_bar_rgb_color: List[int]

    @staticmethod
    def from_raw(raw_str: str) -> 'MapPack':
        """
        A static method that parses the raw string and returns a MapPack object.
        
        :param raw_str: Raw data returned from the servers.
        :type raw_str: str
        :return: A MapPack object created from the raw data.
        """
        parsed = parse_key_value_pairs(raw_str)
        return MapPack(
            id=int(parsed.get("1", 0)),
            name=parsed.get("2", ""),
            level_ids=parse_comma_separated_int_list(parsed.get("3", "")),
            stars=int(parsed.get("4", 0)),
            coins=int(parsed.get("5", 0)),
            difficulty=Difficulty(int(parsed.get("6", 0))),
            text_rgb_color=parse_comma_separated_int_list(parsed.get("7", "")),
            progress_bar_rgb_color=parse_comma_separated_int_list(parsed.get("8", ""))
        )

@dataclass
class Gauntlet(__ListOfLevels__):
    """
    A class representing a gauntlet.
    
    Attributes
    ----------
    id : int
        The ID of the gauntlet.
    name: str
        The name of the gauntlet.
    level_ids : List[int]
        The IDs of the levels.
    image_url : str
        The URL of the image (from gdbrowser.com)
    """
    image_url: str

    @staticmethod
    def from_raw(raw_str: str) -> 'Gauntlet':
        """
        A static method that parses the raw string and returns a Gauntlet object.
        
        :param raw_str: Raw data returned from the servers.
        :type raw_str: str
        :return: A Gauntlet object created from the raw data.
        """
        parsed: dict = parse_key_value_pairs(raw_str)
        name: str = guantlets_names[str(parsed.get("1"))]
        return Gauntlet(
            id=parsed.get("1", 0),
            name=name,
            level_ids=parse_comma_separated_int_list(parsed.get("3", "")),
            image_url=f"https://gdbrowser.com/assets/gauntlets/{name.lower().replace(" ", "_")}.png"
        )
    
    async def get_display_info_all_levels(self) -> Tuple[SearchedLevel]:
        """
        A coroutine method that fetches and returns all the levels in the gauntlet with their display information.
        
        :return: A tuple of SearchedLevel objects.
        """
        search_raw = await send_post_request(
            url="http://www.boomlings.com/database/getGJLevels21.php",
            data={'secret': "Wmfd2893gb7", "gauntlet": self.id}
        )
        search_parsed = parse_search_results(search_raw)
        level_list = [SearchedLevel.from_dict(level) for level in search_parsed]
        return level_list
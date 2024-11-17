"""
## .models.level

A module containing all the classes and methods related to levels in Geometry Dash.
"""

from typing import List, Optional, Union, Tuple
from datetime import datetime
from dataclasses import dataclass
from dateutil.relativedelta import relativedelta

from .song import Song, OfficialSong
from .entity import Entity
from ..helpers import require_client
from ..parse import (
    parse_level_data,
    parse_comma_separated_int_list,
    parse_key_value_pairs,
    determine_difficulty,
    determine_list_difficulty,
    str_to_delta,
)
from ..decode import base64_urlsafe_decode
from .enums import LevelRating, ModRank, Gamemode, Length, Difficulty, SearchFilter
from .cosmetics import Icon

__all__ = ["Level", "LevelDisplay", "LevelList", "Comment", "Gauntlet", "MapPack"]

# A dictionary containing all the names of gauntlets.
GAUNTLETS = {
    "1": "Fire",
    "2": "Ice",
    "3": "Poison",
    "4": "Shadow",
    "5": "Lava",
    "6": "Bonus",
    "7": "Chaos",
    "8": "Demon",
    "9": "Time",
    "10": "Crystal",
    "11": "Magic",
    "12": "Spike",
    "13": "Monster",
    "14": "Doom",
    "15": "Death",
    "16": "Forest",
    "17": "Rune",
    "18": "Force",
    "19": "Spooky",
    "20": "Dragon",
    "21": "Water",
    "22": "Haunted",
    "23": "Acid",
    "24": "Witch",
    "25": "Power",
    "26": "Potion",
    "27": "Snake",
    "28": "Toxic",
    "29": "Halloween",
    "30": "Treasure",
    "31": "Ghost",
    "32": "Gem",
    "33": "Inferno",
    "34": "Portal",
    "35": "Strange",
    "36": "Fantasy",
    "37": "Christmas",
    "38": "Surprise",
    "39": "Mystery",
    "40": "Cursed",
    "41": "Cyborg",
    "42": "Castle",
    "43": "Grave",
    "44": "Temple",
    "46": "World",
    "47": "Galaxy",
    "48": "Universe",
    "49": "Discord",
    "50": "Split",
    "51": "NCS I",
    "52": "NCS II",
}


@dataclass
class Level(Entity):
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
    """

    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    level_data: Optional[str] = None
    version: Optional[int] = None
    creator_player_id: Optional[int] = None
    downloads: int = None
    likes: Optional[int] = None
    copyable: bool = None
    length: "Length" = None
    requested_stars: Optional[int] = None
    stars: Optional[int] = None
    coins: int = None
    custom_song_id: Union[int, None] = None
    song_list_ids: List[int] = None
    sfx_list_ids: List[int] = None
    daily_id: Union[int, None] = None
    copied_level_id: Optional[int] = None
    low_detail_mode: bool = None
    two_player_mode: bool = None
    verified_coins: bool = None
    in_gauntlet: bool = None
    is_daily: bool = False
    is_weekly: bool = False
    is_event: bool = False
    rating: "LevelRating" = None
    difficulty: "Difficulty" = None
    level_password: Optional[str] = None
    official_song: Optional[OfficialSong] = None

    @staticmethod
    def from_raw(raw_str: str) -> "Level":
        """
        A staticmethod that converts a raw level string into a Level object.

        :param raw_str: The raw string returned from the server.
        :type raw_str: str
        :return: A Level object created from the raw data.
        """
        parsed = parse_level_data(raw_str)

        return Level.from_parsed(parsed)

    @staticmethod
    def from_parsed(parsed_str: str) -> "Level":
        """
        A staticmethod that converts a raw level string into a Level object.

        :param parsed_str: The raw string returned from the server.
        :type raw_str: str
        :return: A Level object created from the parsed data.
        """
        parsed = parsed_str
        return Level(
            # raw_str=parsed_str,
            id=parsed.get("1"),
            name=parsed.get("2"),
            description=parsed.get("3"),
            level_data=parsed.get("4"),
            version=parsed.get("5"),
            creator_player_id=parsed.get("6"),
            downloads=int(parsed.get("10", 0)),
            likes=int(parsed.get("14")),
            copyable=bool(parsed.get("27")),
            length=Length(parsed.get("15")),
            requested_stars=parsed.get("39"),
            stars=parsed.get("18"),
            coins=parsed.get("37", 0),
            custom_song_id=parsed.get("35", None),
            song_list_ids=parse_comma_separated_int_list(parsed.get("52")),
            sfx_list_ids=parse_comma_separated_int_list(parsed.get("53")),
            daily_id=parsed.get("41", None),
            copied_level_id=parsed.get("30"),
            low_detail_mode=bool(parsed.get("40")),
            two_player_mode=bool(parsed.get("31")),
            verified_coins=bool(parsed.get("38")),
            in_gauntlet=bool(parsed.get("44")),
            is_daily=0 <= int(parsed.get("41", -1)) <= 100000,
            is_weekly=int(parsed.get("41", -1)) >= 100000,
            rating=Level._determine_rating(parsed),
            difficulty=determine_difficulty(parsed),
            level_password=(
                None if isinstance(parsed.get("27"), bool) else parsed.get("27")
            ),
            official_song=(
                OfficialSong(parsed.get("12")) if parsed.get("12") else None
            ),
        )

    @staticmethod
    def _determine_rating(parsed: dict) -> LevelRating:
        """
        Determines the level's rating based on parsed data.

        :param parsed: Parsed data from the servers
        :type parsed: dict
        :return: `LevelRating`
        """

        if parsed.get("42", 0) >= 1:
            return LevelRating(parsed.get("42"))

        if parsed.get("19", 0) >= 1:
            return LevelRating.FEATURED

        if parsed.get("18", 0) != 0:
            return LevelRating.RATED

        return LevelRating.NO_RATE

    @require_client()
    async def comment(
        self, message: str, percentage: int = 0, client: int = None
    ) -> int:
        """
        Sends a comment to the level.

        Cooldown is 15 seconds.

        :param message: The message to send.
        :type message: str
        :param percentage: The percentage of the level completed. Defaults to 0.
        :type percentage: int
        :param client_index: The client index to send the comment as. Defaults to the priority.
        :type client_index: int
        :raises: gd.CommentError
        :return: The comment ID of the sent comment.
        :rtype: int
        """
        return await client.comment(
            message=message, level_id=self.id, percentage=percentage
        )


@dataclass
class LevelDisplay(Level):
    """
    A class representing a level displayed in the search results in Geometry Dash.

    Attributes
    ----------
    creator_name : Optional[str]
        The creator name of the level.
    creator_account_id : Optional[int]
        The creator's account ID.
    song_data : Union[Song, None]
        The custom song object of the level.
    """

    creator_name: Optional[str] = None
    creator_account_id: Optional[int] = None
    song_data: "Song" = None

    @staticmethod
    def from_parsed(parsed_str: dict) -> "LevelDisplay":
        """
        A staticmethod that converts parsed dict level data into a LevelDisplay object.

        :param parsed_str: The parsed str returned.
        :type parsed_str: dict
        :return: A LevelDisplay object created from the parsed data.
        """

        instance = Level.from_parsed(parsed_str["level"])
        creator_name = parsed_str["creator"]["playerName"]
        creator_account_id = parsed_str["creator"]["accountID"]
        song_data = (
            Song.from_parsed(parsed_str["song"])
            if parsed_str.get("song", None)
            else None
        )

        return LevelDisplay(
            # raw_str=parsed_str['level'],
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
            song_list_ids=instance.song_list_ids,
            sfx_list_ids=instance.sfx_list_ids,
            daily_id=instance.daily_id,
            low_detail_mode=instance.low_detail_mode,
            level_password=instance.level_password,
            official_song=instance.official_song,
        )


@dataclass
class Comment(Entity):
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
    posted_ago : relativedelta
        Time passed since the comment was posted.
    precentage : int
        The perecentage of the comment.
    mod_level : ModRank
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

    level_id: int = None
    content: str = None
    likes: int = None
    id: int = None
    is_spam: bool = None
    posted_ago: relativedelta = None
    precentage: int = None
    mod_level: ModRank = None

    author_player_id: int = None
    author_account_id: int = None
    author_name: str = None
    author_primary_color_id: int = None
    author_secondary_color_id: int = None
    author_has_glow: bool = None
    author_icon: Icon = None
    author_icon_display_gamemode: Gamemode = None

    @staticmethod
    def from_raw(raw_str: str) -> "Comment":
        """
        A staticmethod that parses the raw string and returns a Comment object.

        :param raw_str: Raw data returned from the servers.
        :type raw_str: str
        :return: A Comment object created from the raw data.
        """

        parsed = raw_str.split(":")
        user_value = parse_key_value_pairs(parsed[1], "~")
        comment_value = parse_key_value_pairs(parsed[0], "~")

        return Comment(
            level_id=int(comment_value.get("1", 0)),
            content=base64_urlsafe_decode(comment_value.get("2", "")),
            author_player_id=int(comment_value.get("3", 0)),
            author_account_id=int(user_value.get("16", 0)),
            likes=int(comment_value.get("4", 0)),
            id=int(comment_value.get("6", 0)),
            is_spam=bool(int(comment_value.get("7", 0))),
            posted_ago=str_to_delta(comment_value.get("9", "0 seconds")),
            precentage=int(comment_value.get("10", 0)),
            mod_level=ModRank(int(comment_value.get("11", 0))),
            author_name=user_value.get("1", ""),
            author_icon=Icon(
                user_value.get("9", ""),
                gamemode=Gamemode(int(user_value.get("14", 0))),
                primary_color_id=int(user_value.get("10", 1)),
                secondary_color_id=int(user_value.get("11", 1)),
                glow_color_id=None,
            ),
            author_icon_display_gamemode=Gamemode(int(user_value.get("14", 0))),
            author_primary_color_id=int(user_value.get("10", 1)),
            author_secondary_color_id=int(user_value.get("11", 1)),
            author_has_glow=bool(int(user_value.get("15", 0))),
        )


@dataclass
class ListLevels(Entity):
    """
    A class representing a list of levels. (Not to be confused with LevelList)

    Attributes
    ----------
    id : int
    name : str
    level_ids : List[int]
    """

    id: int = None
    name: str = None
    level_ids: List[int] = None

    @require_client()
    async def levels(self, client: int = None) -> Tuple[LevelDisplay]:
        """
        A method that gets all the levels in the list with their display information.

        :return: A tuple of LevelDisplay objects.
        """
        str_ids = ",".join([str(level) for level in self.levels_id])

        return await client.search_level(
            query=str_ids, src_filter=SearchFilter.LIST_OF_LEVELS
        )

    @require_client()
    async def download_level(self, index: int, client: int = None) -> Level:
        """
        A coroutine method that downloads a level from the level list based on the index.

        :param index: The index of the level to download.
        :type index: int
        :return: A Level object representing the downloaded level.
        """
        if index < 0 or index >= len(self.levels_id):
            raise IndexError("Invalid level index.")

        level_id = self.levels_id[index]
        return await client.download_level(level_id=level_id)


@dataclass
class LevelList(ListLevels):
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

    description: str = None
    difficulty: Difficulty = None
    downloads: int = None
    likes: int = None
    is_rated: bool = None
    upload_date: datetime = None
    last_update_date: datetime = None
    author_account_id: int = None
    author_name: str = None
    diamonds: int = None
    minimum_levels: int = None

    @staticmethod
    def from_raw(raw_str: str) -> "LevelList":
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
            description=base64_urlsafe_decode(parsed.get("3", "")),
            difficulty=determine_list_difficulty(parsed.get("7", None)),
            downloads=int(parsed.get("10", 0)),
            likes=int(parsed.get("14", 0)),
            is_rated=bool(parsed.get("19")),
            upload_date=datetime.fromtimestamp(int(parsed.get("28", 0))),
            last_update_date=datetime.fromtimestamp(int(parsed.get("29", 0))),
            author_account_id=int(parsed.get("49", 0)),
            author_name=parsed.get("50", ""),
            diamonds=int(parsed.get("55", 0)),
            minimum_levels=int(parsed.get("56", 0)),
        )


@dataclass
class MapPack(ListLevels):
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
        The difficulty of the map pack
    text_rgb_color : List[int]
        The rgb color of the map pack's text
    progress_bar_rgb_color : List[int]
        The rgb color of the map pack's progress bar
    """

    stars: int = None
    coins: int = None
    difficulty: Difficulty = None
    text_rgb_color: List[int] = None
    progress_bar_rgb_color: List[int] = None

    @staticmethod
    def from_raw(raw_str: str) -> "MapPack":
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
            text_rgb_color=tuple(parse_comma_separated_int_list(parsed.get("7", ""))),
            progress_bar_rgb_color=tuple(
                parse_comma_separated_int_list(parsed.get("8", ""))
            ),
        )


@dataclass
class Gauntlet(ListLevels):
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

    image_url: str = None

    @staticmethod
    def from_raw(raw_str: str) -> "Gauntlet":
        """
        A static method that parses the raw string and returns a Gauntlet object.

        :param raw_str: Raw data returned from the servers.
        :type raw_str: str
        :return: A Gauntlet object created from the raw data.
        """
        parsed: dict = parse_key_value_pairs(raw_str)
        name: str = GAUNTLETS[str(parsed.get("1"))]

        return Gauntlet(
            id=parsed.get("1", 0),
            name=name,
            level_ids=parse_comma_separated_int_list(parsed.get("3", "")),
            image_url=f"https://gdbrowser.com/assets/gauntlets/{name.lower().replace(" ", "_")}.png",
        )

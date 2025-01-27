"""
## .objects.level

A module containing all the classes and methods related to levels in Geometry Dash.
"""

from typing import Union, Optional
from datetime import datetime

import attr

from gd.song import Song
from gd.gdobject import GDItem
from gd.helpers import require_client
from gd.parse import (
    parse_level_data,
    parse_comma_separated_int_list,
    parse_key_value_pairs,
    determine_level_difficulty,
    determine_list_difficulty,
    string_to_seconds,
)
from gd.cryptography import base64_urlsafe_decode
from gd.enums import (
    LevelRating,
    ModRank,
    Gamemode,
    Length,
    Difficulty,
    SearchFilter,
    OfficialSong,
)
from gd.cosmetics import Icon
from gd.type_hints import (
    LevelId,
    PlayerId,
    SoundEffectId,
    SongId,
    AccountId,
    CommentId,
    ColorId,
)

__all__ = ["Level", "LevelDisplay", "LevelList", "Comment", "Gauntlet", "MapPack"]

# A dictionary containing all the names of gauntlets.
gauntlets: dict = {
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


@attr.define(slots=True)
class Level(GDItem):
    """
    A class representing a downloaded level in Geometry Dash.

    Attributes:
    ----------
    raw_str : str
        The original unparsed data from the servers.
    id : LevelId
        The ID of the level.
    name : str
        The name of the level.
    description : str
        The description of the level.
    level_data : str
        The level's data.
    version : int
        The level's version.
    creator_player_id : PlayerId
        The player ID of the creator of the level.
    downloads : int
        The download count of the level.
    likes : int
        The like count of the level.
    copyable : bool
        Whether the level can be copied or not.
    length : Length
        The length of the level. (Not the exact length)
    requested_stars : int
        The level rating requested by the creator.
    stars : int
        The star count for the level.
    coins : int
        The coins count for the level.
    custom_song_id : Optional[SongId]
        The id for the custom song used for the level.
    song_list_ids : list[SongId]
        The list of the song IDs used in the level.
    sfx_list_ids : list[SoundEffectId]
        The list of the song IDs used in the level.
    is_daily : bool
        If the level was a daily level.
    is_weekly : bool
        If the level was a weekly level.
    rating : LevelRating
        The rating of the level. (None, Featured, Epic, etc.)
    difficulty : Union[Difficulty, DemonDifficulty]
        The difficulty of the level.
    level_password: Optional[int]
        The password for the level to copy.
    official_song: Optional[OfficialSong]
        The official song used in the level. Returns None if the level uses a custom song.
    """

    id: LevelId = None
    name: str = None
    description: str = None
    level_data: str = None
    version: int = None
    creator_player_id: PlayerId = None
    downloads: int = None
    likes: int = None
    copyable: bool = None
    length: "Length" = None
    requested_stars: int = None
    stars: int = None
    coins: int = None
    custom_song_id: Optional[SongId] = None
    song_list_ids: list[SongId] = None
    sfx_list_ids: list[SoundEffectId] = None
    daily_id: Union[int, None] = None
    copied_level_id: int = None
    low_detail_mode: bool = None
    two_player_mode: bool = None
    verified_coins: bool = None
    in_gauntlet: bool = None
    is_daily: bool = False
    is_weekly: bool = False
    is_event: bool = False
    rating: "LevelRating" = None
    difficulty: "Difficulty" = None
    level_password: str = None
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
        :type parsed_str: str
        :return: A Level object created from the parsed data.
        """
        parsed = parsed_str
        return Level(
            # raw_str=parsed_str,
            id=parsed.get("1"),
            name=str(parsed.get("2")),
            description=parsed.get("3"),
            level_data=parsed.get("4", ""),
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
            difficulty=determine_level_difficulty(parsed),
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

    @property
    def orbs(self) -> int:
        """
        Return the amount of orbs earned after beating the level.
        """
        star_orbs_map = {
            2: 50,
            3: 75,
            4: 125,
            5: 175,
            6: 225,
            7: 275,
            8: 350,
            9: 425,
            10: 500,
        }
        return star_orbs_map.get(self.stars, 0)

    @require_client(login=True)
    async def comment(self, message: str, percentage: int = 0) -> int:
        """
        Sends a comment to the level.

        Cooldown is 15 seconds.

        :param message: The message to send.
        :type message: str
        :param percentage: The percentage of the level completed. Defaults to 0.
        :type percentage: int
        :raises: gd.CommentError
        :return: The comment ID of the sent comment.
        :rtype: int
        """
        return await self.client.send_comment(
            message=message, level_id=self.id, percentage=percentage
        )

    @require_client(login=True)
    async def like(self, dislike: bool = False) -> None:
        """
        Sends a like to the level.

        :param dislike: If True, dislike the level, else like it.
        :type dislike: bool
        :return: None
        :rtype: None
        """
        await self.client.like_level(level_id=self.id, dislike=dislike)

    @require_client()
    async def comments(self, page: int = 0) -> list["Comment"]:
        """
        Get the comments for the level.

        :param page: The page number to get comments from.
        :type page: int
        :return: A list of Comment objects.
        :rtype: list[Comment]
        """
        await self.client.get_comments(self.id, page)


@attr.define(slots=True)
class LevelDisplay(Level):
    """
    A class representing a level displayed in the search results in Geometry Dash.

    Attributes
    ----------
    creator_name : str
        The creator name of the level.
    creator_account_id : int
        The creator's account ID.
    song : Optional[Song]
        The custom song object of the level.
    """

    creator_name: str = None
    creator_account_id: AccountId = None
    song: Optional[Song] = None

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
        song = (
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
            song=song,
            level_data=None,
            song_list_ids=instance.song_list_ids,
            sfx_list_ids=instance.sfx_list_ids,
            daily_id=instance.daily_id,
            low_detail_mode=instance.low_detail_mode,
            level_password=instance.level_password,
            official_song=instance.official_song,
        )


@attr.define(slots=True)
class Comment(GDItem):
    """
    A class representing a comment in a level.

    Attributes
    ----------
    level_id : LevelId
        The ID of the level the comment belongs to.
    content : str
        The content of the comment.
    likes : int
        The current likes count for the comment.
    id : CommentId
        The ID of the comment.
    is_spam : bool
        If the comment is spam.
    posted_ago : str
        SSeconds passed after the comment was posted.
    percentage : int
        The perecentage of the comment.
    mod_level : ModRank
        The mod level of the author.
    author_player_id : PlayerId
        The ID of the author's player.
    author_account_id : AccountId
        The ID of the author's account.
    author_name : str
        The name of the author.
    author_primary_color : ColorId
        The primary color of the author.
    author_secondary_color : ColorId
        The secondary color of the author.
    author_has_glow : bool
        If the author has a glow effect.
    author_icon : Icon
        The icon of the author.
    author_icon_display_gamemode : Gamemode
        The gamemode the author chooses to display in their comment.
    """

    level_id: LevelId = None
    content: str = None
    likes: int = None
    id: CommentId = None
    is_spam: bool = None
    posted_ago: str = None
    percentage: int = None
    mod_level: ModRank = None

    author_player_id: PlayerId = None
    author_account_id: AccountId = None
    author_name: str = None
    author_primary_color: ColorId = None
    author_secondary_color: ColorId = None
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
            content=base64_urlsafe_decode(comment_value.get("2", "")).decode(),
            author_player_id=int(comment_value.get("3", 0)),
            author_account_id=int(user_value.get("16", 0)),
            likes=int(comment_value.get("4", 0)),
            id=int(comment_value.get("6", 0)),
            is_spam=bool(int(comment_value.get("7", 0))),
            posted_ago=string_to_seconds(comment_value.get("9", "0 seconds")),
            percentage=int(comment_value.get("10", 0)),
            mod_level=ModRank(int(comment_value.get("11", 0))),
            author_name=user_value.get("1", ""),
            author_icon=Icon(
                user_value.get("9", ""),
                gamemode=Gamemode(int(user_value.get("14", 0))),
                primary_color_id=int(user_value.get("10", 1)),
                secondary_color_id=int(user_value.get("11", 1)),
                glow_color_id=None,
            ),
            author_primary_color=int(user_value.get("10", 1)),
            author_secondary_color=int(user_value.get("11", 1)),
            author_has_glow=bool(int(user_value.get("15", 0))),
        )

    @require_client(login=True)
    async def like(self, dislike: bool = False) -> None:
        """
        Like or dislike the comment.

        :param dislike: If True, dislike the comment, else like it.
        :type dislike: bool
        :return: None
        :rtype: None
        """
        await self.client.like_comment(self.id, self.level_id, dislike)


@attr.define(slots=True)
class _ListLevels(GDItem):
    """
    A class representing a list of levels. (Not to be confused with LevelList)

    Attributes
    ----------
    id : int
    name : str
    level_ids : list[LevelId]
    """

    id: int
    name: str
    level_ids: list[LevelId]

    @require_client()
    async def levels(self) -> list[LevelDisplay]:
        """
        A method that gets all the levels in the list with their display information.

        :param client: The client (or client index) to get.
        :type client: int
        :return: A list of LevelDisplay objects.
        :rtype: list[LevelDisplay]
        """
        str_ids = ",".join([str(level) for level in self.level_ids])

        return await self.client.search_level(
            query=str_ids, src_filter=SearchFilter.LIST_OF_LEVELS
        )

    @require_client()
    async def download_level(self, index: int) -> Level:
        """
        A coroutine method that downloads a level from the level list based on the index.

        :param index: The index of the level to download.
        :type index: int
        :return: A Level object representing the downloaded level.
        """
        if index < 0 or index >= len(self.level_ids):
            raise IndexError("Invalid level index.")

        level_id = self.level_ids[index]
        return await self.client.download_level(level_id=level_id)


@attr.define(slots=True)
class LevelList(_ListLevels):
    """
    A class representing a list.

    Attributes
    ----------
    id : ListId
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
    level_ids : list[LevelId]
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
            description=base64_urlsafe_decode(parsed.get("3", "")).decode(),
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

    @require_client(login=True)
    async def like(self, dislike: bool = False) -> None:
        """
        Like or dislike a list.

        :param dislike: If True, dislike the level, else like it.
        :type dislike: bool
        :return: None
        :rtype: None
        """
        return await self.client.like_list(self.id, dislike)

    @require_client(login=True)
    async def comment(self, message: str) -> CommentId:
        """
        Sends a comment to the list.

        Cooldown is 15 seconds.

        :param message: The message to send.
        :type message: str
        :raises: gd.CommentError
        :return: The comment ID of the sent comment.
        :rtype: CommentId
        """
        return await self.client.send_comment(message=message, level_id=-self.id)

    @require_client()
    async def comments(self, page: int = 0) -> list[Comment]:
        """
        Gets comments from the list.

        Cooldown is 15 seconds.

        :param page: The page of comments to load.
        :type page: int
        :return: A list of comments.
        :rtype: list[Comment]
        """
        return await self.client.get_comments(level_id=-self.id, page=page)


@attr.define(slots=True)
class MapPack(_ListLevels):
    """
    A class representing a map pack.

    Attributes
    ----------
    id : int
        ID of the map pack.
    name : str
        Name of the map pack.
    level_ids : list[LevelId]
        The list of the levels' ID.
    stars : int
        The star count of the map pack.
    coins : int
        The coin count of the map pack.
    difficulty : Difficulty
        The difficulty of the map pack.
    text_rgb_color : tuple[int]
        The rgb color of the map pack's text.
    progress_bar_rgb_color : tuple[int]
        The rgb color of the map pack's progress bar.
    """

    stars: int = None
    coins: int = None
    difficulty: Difficulty = None
    text_rgb_color: tuple[int] = None
    progress_bar_rgb_color: tuple[int] = None

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


@attr.define(slots=True)
class Gauntlet(_ListLevels):
    """
    A class representing a gauntlet.

    Attributes
    ----------
    id : int
        The ID of the gauntlet.
    name: str
        The name of the gauntlet.
    level_ids : list[LevelId]
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
        name: str = gauntlets[str(parsed.get("1"))]

        return Gauntlet(
            id=parsed.get("1", 0),
            name=name,
            level_ids=parse_comma_separated_int_list(parsed.get("3", "")),
            image_url=f"https://gdbrowser.com/assets/gauntlets/{name.lower().replace(" ", "_")}.png",
        )

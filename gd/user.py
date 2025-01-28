"""
## .objects.users
A module containing all the classes and methods related to users and accounts in Geometry Dash.
"""

from typing import Optional, Literal, NamedTuple

import attr

from gd.str_helpers import (
    parse_key_value_pairs,
    parse_comma_separated_int_list,
    string_to_seconds,
)
from gd.enums import Gamemode, ModRank, Item, Shard, ChestType
from gd.cosmetics import IconSet
from gd.level import Comment, LevelDisplay
from gd.gdobject import GDItem
from gd.cryptography import base64_urlsafe_decode, gjp2
from gd.helpers import require_client
from gd.type_hints import (
    AccountId,
    PlayerId,
    AccountCommentId,
    ColorId,
    LeaderboardValue,
)

SECRET = "Wmfd2893gb7"

__all__ = [
    "AccountComment",
    "Player",
    "Account",
    "DifficultyStats",
    "DemonStats",
    "Quest",
    "Chest",
]

DifficultyStats = NamedTuple(
    "DifficultyStats",
    [
        ("auto", int),
        ("easy", int),
        ("normal", int),
        ("hard", int),
        ("harder", int),
        ("insane", int),
        ("daily", Optional[int]),
        ("gauntlet", Optional[int]),
    ],
)
"""A namedtuple for how many different levels of difficulty the player has beaten."""

DemonStats = NamedTuple(
    "DemonStats",
    [
        ("easy", int),
        ("medium", int),
        ("hard", int),
        ("insane", int),
        ("extreme", int),
        ("weekly", Optional[int]),
        ("gauntlet", Optional[int]),
    ],
)
"""A namedtuple for how many different demon levels the player has beaten."""


@attr.define(slots=True)
class AccountComment(GDItem):
    """
    A class representing a post from a player.

    Attributes
    ----------
    content : str
        The content of the post.
    likes : int
        The number of likes of the post.
    id : AccountCommentId
        The ID of the account comment.
    posted_ago : relativedelta
        Seconds passed after the comment was posted.
    author_account_id : Optional[AccountId]
        The ID of the author, or None if doesn't exist.
    """

    content: str = None
    """The content of the post."""
    likes: int = None
    """The number of likes of the post."""
    id: AccountCommentId = None
    """The ID of the account comment."""
    posted_ago: str = None
    """Seconds passed after the comment was posted."""
    author_account_id: Optional[AccountId] = None
    """The ID of the author, or None if it doesn't exist."""

    @staticmethod
    def from_raw(raw_str: str, account_id: int = None) -> "AccountComment":
        """
        A static method that converts the raw data from the server into an AccountComment instance.

        :param raw_str: The raw data from the server.
        :type raw_str: str
        :param account_id: The account ID of the user, optional if not provided.
        :type account_id: Union[int, None]
        :return: A Post instance.
        :rtype: Post
        """
        parsed = raw_str.split(":")
        comment_value = parse_key_value_pairs(parsed[0], "~")

        return AccountComment(
            content=base64_urlsafe_decode(comment_value.get("2", "")),
            likes=int(comment_value.get("4", 0)),
            id=int(comment_value.get("6", 0)),
            posted_ago=string_to_seconds(comment_value.get("9", "0 seconds")),
            author_account_id=account_id,
        )

    @require_client(login=True)
    async def like(self, dislike: bool = False) -> None:
        """
        Like or dislike the account comment.

        :param dislike: If True, dislike the post, else like it.
        :type dislike: bool
        :return: None
        :rtype: None
        """
        await self.client.like_post(self.id, dislike)


@attr.define(slots=True)
class Player(GDItem):
    """
    A class representing an user's profile.

    Attributes
    ----------
    name : str
        The name of the user.
    player_id : PlayerId
        The player ID of the user.
    account_id : AccountId
        The account ID of the user.
    stars : int
        The amount of stars the user has.
    moons : int
        The amount of moons the user has.
    demons : int
        The amount of demons the user has beaten.
    diamonds : int
        The amount of diamonds the user has.
    rank : int
        The rank of the user in the leaderboard.
    creator_points : int
        The amount of creator points the user has.
    secret_coins : int
        The amount of secret coins the user has.
    user_coins : int
        The amount of user coins the user has.
    registered : bool
        If the user has registered.
    mod_level : Optional[ModRank]
        The mod level of the user.
    is_friend : bool = False
        If the player is a friend.
    accept_requests : bool = False
        If the player accept all friend requests.
    primary_color_id : Optional[ColorId]
        The primary color id of the user's icon.
    secondary_color_id : Optional[ColorId]
        The secondary color id of the user's icon.
    glow_color_id : Optional[ColorId]
        The glow color id of the user's icon.
    profile_icon_type : Optional[Gamemode]
        The gamemode that the user primarily chooses to display.
    youtube : Optional[str]
        The YouTube channel link of the user.
    twitter_or_x : Optional[str]
        The Twitter (or X) username of the user.
    twitch : Optional[str]
        The Twitch username of the user.
    classic_demon_stats : Optional[DemonStats]
        The stats of classic demon levels beaten.
    platformer_demon_stats: Optional[DemonStats]
        The stats of platformer demon levels beaten.
    classic_stats: Optional[DifficultyStats]
        The stats of non-demon classic levels beaten.
    platformer_stats: Optional[DifficultyStats]
        The stats of platformer non-demon levels beaten.
    set_ago : Optional[str] = None
        The last time the score was set on a level.
    """

    name: str = None
    """The name of the user."""
    player_id: PlayerId = None
    """The player ID of the user."""
    account_id: AccountId = None
    """The account ID of the user."""
    stars: Optional[int] = None
    """The amount of stars the user has."""
    moons: Optional[int] = None
    """The amount of moons the user has."""
    demons: Optional[int] = None
    """The amount of demons the user has beaten."""
    diamonds: Optional[int] = None
    """The amount of diamonds the user has."""
    rank: Optional[int] = None
    """The rank of the user in the leaderboard."""
    creator_points: Optional[int] = None
    """The amount of creator points the user has."""
    secret_coins: Optional[int] = None
    """The amount of secret coins the user has."""
    user_coins: Optional[int] = None
    """The amount of user coins the user has."""
    registered: Optional[bool] = None
    """If the user has registered."""
    mod_level: Optional[ModRank] = None
    """The mod level of the user."""
    is_friend: bool = False
    """If the player is a friend."""
    accept_requests: bool = False
    """If the player accept all friend requests."""

    primary_color_id: Optional[ColorId] = None
    """The primary color id of the user's icon."""
    secondary_color_id: Optional[ColorId] = None
    """The secondary color id of the user's icon."""
    glow_color_id: Optional[ColorId] = None
    """The glow color id of the user's icon."""
    profile_icon_type: Optional[Gamemode] = None
    """The gamemode that the user primarily chooses to display."""
    icons: IconSet = None
    """The icon set of the user."""

    youtube: Optional[str] = None
    """The YouTube channel link of the user."""
    twitter: Optional[str] = None
    """The Twitter (or X) username of the user."""
    twitch: Optional[str] = None
    """The Twitch username of the user."""

    classic_demon_stats: Optional[DemonStats] = None
    """The stats of classic demon levels beaten."""
    platformer_demon_stats: Optional[DemonStats] = None
    """The stats of platformer demon levels beaten."""
    classic_stats: Optional[DifficultyStats] = None
    """The stats of non-demon classic levels beaten."""
    platformer_stats: Optional[DifficultyStats] = None
    """The stats of platformer non-demon levels beaten."""

    leaderboard_set_ago: Optional[str] = None
    """The amount of seconds passed after the record was placed."""
    leaderboard_value: LeaderboardValue = None
    """The value in the leaderboard, depending on leaderboard type. (Only shown on leaderboard scores)"""

    @staticmethod
    def from_raw(raw_str: str, parse_leaderboard_score: bool = False) -> "Player":
        """
        Parse the string data from the servers and returns an Player instance.

        :param raw_str: The raw data from the server.
        :type raw_str: str
        :param parse_leaderboard_score: Whether to parse the leaderboard score or not.
        :type parse_leaderboard_score: bool
        :return: An instance of the Player class.
        :rtype: Player
        """
        parsed = parse_key_value_pairs(raw_str)

        demon_stats = parsed.get("55", None)
        if demon_stats:
            demon_stats = parse_comma_separated_int_list(demon_stats)

        normal_stats = parsed.get("56", None)
        if normal_stats:
            normal_stats = parse_comma_separated_int_list(normal_stats)

        platformer_stats = parsed.get("57", None)
        if platformer_stats:
            platformer_stats = parse_comma_separated_int_list(platformer_stats)

        primary_color = int(parsed.get("10", 0))
        secondary_color = int(parsed.get("11", 0))
        glow_color = (
            int(parsed.get("51")) if parsed.get("51", None) is not None else None
        )

        return Player(
            name=parsed.get("1", None),
            player_id=parsed.get("2", 0),
            account_id=parsed.get("16", 0),
            stars=parsed.get("3", 0) if not parse_leaderboard_score else 0,
            moons=parsed.get("52", 0),
            demons=parsed.get("4", 0),
            diamonds=parsed.get("46"),
            rank=parsed.get("6"),
            creator_points=parsed.get("8", 0),
            secret_coins=parsed.get("13", 0),
            user_coins=parsed.get("17", 0),
            registered=parsed.get("29") == 1,
            mod_level=ModRank(parsed.get("49", 0)),
            is_friend=parsed.get("31") == 1,
            accept_requests=parsed.get("19") == 0,
            profile_icon_type=Gamemode(parsed.get("14", 1)),
            primary_color_id=primary_color,
            secondary_color_id=secondary_color,
            glow_color_id=glow_color,
            youtube=parsed.get("20", None) if parsed.get("20") != r"%%00" else None,
            twitter=parsed.get("44"),
            twitch=parsed.get("45"),
            classic_demon_stats=(
                DemonStats(
                    easy=demon_stats[0],
                    medium=demon_stats[1],
                    hard=demon_stats[2],
                    insane=demon_stats[3],
                    extreme=demon_stats[4],
                    weekly=demon_stats[10],
                    gauntlet=demon_stats[11],
                )
                if demon_stats
                else None
            ),
            platformer_demon_stats=(
                DemonStats(
                    easy=demon_stats[5],
                    medium=demon_stats[6],
                    hard=demon_stats[7],
                    insane=demon_stats[8],
                    extreme=demon_stats[9],
                    weekly=None,
                    gauntlet=None,
                )
                if demon_stats
                else None
            ),
            classic_stats=(DifficultyStats(*normal_stats) if normal_stats else None),
            platformer_stats=(
                DifficultyStats(*platformer_stats, gauntlet=None)
                if platformer_stats
                else None
            ),
            icons=IconSet.load(
                cube=parsed.get("21", 1),
                ship=parsed.get("22", 1),
                ball=parsed.get("23", 1),
                ufo=parsed.get("24", 1),
                wave=parsed.get("25", 1),
                robot=parsed.get("26", 1),
                spider=parsed.get("43", 1),
                swing=parsed.get("53", 1),
                jetpack=parsed.get("54", 1),
                primary_color=primary_color,
                secondary_color=secondary_color,
                glow_color=glow_color,
            ),
            leaderboard_set_ago=string_to_seconds(parsed.get("42", "0 seconds")),
            leaderboard_value=int(parsed.get("3")) if parse_leaderboard_score else None,
        )

    @require_client()
    async def account_comments(self, page: int = 0) -> list[AccountComment]:
        """
        Load all account comments from the user.

        :param page: The page number to load, default is 0.
        :type page: int
        :return: A list of AccountComment instances or None if the request failed.
        :rtype: list[AccountComment]
        """
        return await self.client.get_user_account_comments(self.player_id, page)

    @require_client()
    async def comments(
        self, page: int = 0, display_most_liked: bool = False
    ) -> list[Comment]:
        """
        Get user's comments history.

        :param page: The page number to load, default is 0.
        :type page: int
        :param display_most_liked: If sort by most liked, else sort recent.
        :type display_most_liked: bool
        :return: A list of Comment instances.
        :rtype: list[Comment]
        """
        return await self.client.get_user_comments(
            self.player_id, page, display_most_liked
        )

    @require_client()
    async def levels(self, page: int = 0) -> list[LevelDisplay]:
        """
        Get user's levels.

        :param page: The page number to load, default is 0.
        :type page: int
        :return: A list of LevelDisplay instances.
        :rtype: list[LevelDisplay]
        """

        return await self.client.get_user_levels(self.player_id, page)


@attr.define(slots=True, frozen=True)
class Quest:
    """
    Represents a quest in Geometry Dash.

    Attributes
    ==========
    name: str
        The name of the quest.
    requirement_value: int
        The number value of the requirement.
    requirement_type: Literal[Item.STARS, Item.ORBS, Item.COIN]
        The type of requirement.
    diamonds_reward: int
        The total of diamonds get if completed.
    time_left: int
        Seconds left until next quest is chosen.
    """

    name: str
    """The name of the quest"""
    requirement_value: int
    """The number value of the requirement"""
    requirement_type: Literal[Item.STARS, Item.ORBS, Item.USERCOIN]
    """The type of requirement"""
    diamonds_reward: int
    """The total of diamonds get if completed"""
    time_left: int
    """Seconds left until next quest is chosen"""


# * Chests


@attr.define(slots=True, frozen=True)
class Chest:
    """
    Represents a chest in Geometry Dash.

    Attributes
    ==========
    orbs : int
        The amount of orbs in the chest.
    diamonds : int
        The amount of diamonds in the chest.
    items : list[Item.DEMON_KEY, Shard]
        Extra items in the chest.
    time_left : int
        Seconds left until next quest is chosen.
    times_opened: int
        How many times the chest is opened.
    """

    orbs: int
    """The amount of orbs in the chest."""
    diamonds: int
    """The amount of diamonds in the chest."""
    items: list[Item.DEMON_KEY, Shard]
    """Extra items in the chest."""
    time_left: int
    """Seconds left until next quest is chosen."""
    times_opened: int
    """How many times the chest is open."""
    chest_type: ChestType
    """Chest type."""


# * Accounts


@attr.define(slots=True, frozen=True)
class Account:
    """
    Represents an account (not Player) on Geometry Dash.

    Attributes
    ==========
    account_id: AccountId
        Account ID associated with the accoount
    player_id: PlayerId
        Player ID associated with the account.
    name: Optional[str]
        Name of the account holder.
    password: str
        Plaintext password of the account.
    """

    account_id: AccountId
    """Account ID associated with the accoount."""
    player_id: PlayerId
    """Player ID associated with the account."""
    name: Optional[str]
    """Name of the account."""
    password: str
    """Plaintext password of the account."""

    @property
    def gjp2(self) -> str:
        """
        Generate GJP2 hash from password. (Recommended)
        """
        return gjp2(self.password)

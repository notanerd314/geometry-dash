"""
## .models.users
A module containing all the classes and methods related to users and accounts in Geometry Dash.
"""

from typing import List, Optional, Union
from dataclasses import dataclass
from hashlib import sha1

import colorama as color

from ..parse import parse_key_value_pairs
from .enums import Gamemode, ModRank
from .cosmetics import IconSet
from .level import Comment, LevelDisplay
from .entity import Entity
from ..decode import decrypt_data
from ..helpers import require_client

color.init(autoreset=True)

SECRET = "Wmfd2893gb7"
PASSWORD_SALT = "mI29fmAnxgTs"


@dataclass
class Post(Entity):
    """
    A class representing a post from a player.

    Attributes
    ----------
    content : str
        The content of the post.
    likes : int
        The number of likes of the post.
    post_id : int
        The id of the post.
    posted_ago : str
        The time when the post was posted in a string, example: `"5 months"`
    author_account_id : Union[int, None]
        The ID of the author, or None if doesn't exist.
    """

    content: str = None
    """The content of the post."""
    likes: int = None
    """The number of likes of the post."""
    post_id: int = None
    """The ID of the post."""
    posted_ago: str = None
    """The time when the post was posted, e.g., '5 months'."""
    author_account_id: Union[int, None] = None
    """The ID of the author, or None if it doesn't exist."""

    @staticmethod
    def from_raw(raw_str: str, account_id: int = None) -> "Post":
        """
        A static method that converts the raw data from the server into a Post instance.

        :param raw_str: The raw data from the server.
        :type raw_str: str
        :param account_id: The account ID of the user, optional if not provided.

        :type account_id: Union[int, None]
        :return: A Post instance.
        """
        parsed = raw_str.split(":")
        comment_value = parse_key_value_pairs(parsed[0], "~")

        return Post(
            content=decrypt_data(comment_value.get("2", "")),
            likes=int(comment_value.get("4", 0)),
            post_id=int(comment_value.get("6", 0)),
            posted_ago=comment_value.get("9", None),
            author_account_id=account_id,
        )


# * Classes representing stats
@dataclass
class DifficultyStats:
    """
    A class representing the non-demon stats of a level.
    """

    auto: int
    """The amount of auto levels beaten."""
    easy: int
    """The amount of easy levels beaten."""
    normal: int
    """The amount of normal levels beaten."""
    hard: int
    """The amount of hard levels beaten."""
    harder: int
    """The amount of harder levels beaten."""
    insane: int
    """The amount of insane levels beaten."""
    daily: int = None
    """The amount of daily levels beaten."""
    guantlet: int = None
    """The amount of non-demon gauntlet levels beaten."""


@dataclass
class DemonStats:
    """
    A class representing the demon stats of a level.
    """

    easy: int
    """The amount of easy demon levels beaten."""
    medium: int
    """The amount of medium demon levels beaten."""
    hard: int
    """The amount of hard demon levels beaten."""
    insane: int
    """The amount of insane demon levels beaten."""
    extreme: int
    """The amount of extreme demon levels beaten."""
    weekly: int = None
    """The amount of weekly levels beaten."""
    guantlet: int = None
    """The amount of demon gauntlet levels beaten."""


@dataclass
class Player(Entity):
    """
    A class representing an user's profile.

    Attributes
    ----------
    name : str
        The name of the user.
    player_id : int
        The player ID of the user.
    account_id : int
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
    primary_color_id : Optional[int]
        The primary color id of the user's icon.
    secondary_color_id : Optional[int]
        The secondary color id of the user's icon.
    glow_color_id : Optional[int]
        The glow color id of the user's icon.
    profile_icon_type : Optional[Gamemode]
        The gamemode that the user primarily chooses to display.
    youtube : Union[str, None]
        The YouTube channel link of the user.
    twitter_or_x : Union[str, None]
        The Twitter (or X) username of the user.
    twitch : Union[str, None]
        The Twitch username of the user.
    classic_demon_stats : Optional[DemonStats]
        The stats of classic demon levels beaten.
    platformer_demon_stats: Optional[DemonStats]
        The stats of platformer demon levels beaten.
    classic_stats: Optional[DifficultyStats]
        The stats of non-demon classic levels beaten.
    platformer_stats: Optional[DifficultyStats]
        The stats of platformer non-demon levels beaten.
    """

    name: str = None
    """The name of the user."""
    player_id: int = None
    """The player ID of the user."""
    account_id: int = None
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

    primary_color_id: Optional[int] = None
    """The primary color id of the user's icon."""
    secondary_color_id: Optional[int] = None
    """The secondary color id of the user's icon."""
    glow_color_id: Optional[int] = None
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

    @staticmethod
    def from_raw(raw_str: str) -> "Player":
        """
        Parse the string data from the servers and returns an Player instance.

        :param raw_str: The raw data from the server.
        :type raw_str: str
        :return: An instance of the Player class.
        """
        parsed = parse_key_value_pairs(raw_str)
        demon_stats = parsed.get("55", None)
        normal_stats = parsed.get("56", None)
        platformer_stats = parsed.get("57", None)

        primary_color = int(parsed.get("10", 0))
        secondary_color = int(parsed.get("11", 0))
        glow_color = (
            int(parsed.get("51")) if parsed.get("51", None) is not None else None
        )

        return Player(
            name=parsed.get("1", None),
            player_id=parsed.get("2", 0),
            account_id=parsed.get("16", 0),
            stars=parsed.get("3", 0),
            moons=parsed.get("52", 0),
            demons=parsed.get("4", 0),
            diamonds=parsed.get("46"),
            rank=parsed.get("30"),
            creator_points=parsed.get("8", 0),
            secret_coins=parsed.get("13", 0),
            user_coins=parsed.get("17", 0),
            registered=parsed.get("29") == 1,
            mod_level=ModRank(parsed.get("49", 0)),
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
                    guantlet=demon_stats[11],
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
                )
                if demon_stats
                else None
            ),
            classic_stats=(
                DifficultyStats(
                    auto=normal_stats[0],
                    easy=normal_stats[1],
                    normal=normal_stats[2],
                    hard=normal_stats[3],
                    harder=normal_stats[4],
                    insane=normal_stats[5],
                    daily=normal_stats[6],
                    guantlet=normal_stats[7],
                )
                if normal_stats
                else None
            ),
            platformer_stats=(
                DifficultyStats(
                    auto=platformer_stats[0],
                    easy=platformer_stats[1],
                    normal=platformer_stats[2],
                    hard=platformer_stats[3],
                    harder=platformer_stats[4],
                    insane=platformer_stats[5],
                )
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
        )

    @require_client()
    async def posts(self, page: int = 0, client: int = None) -> List[Post] | None:
        """
        Load all posts from the user.

        :param page: The page number to load, default is 0.
        :type page: int
        :param client: The client index to use in the attached clients list. Defaults to 0.
        :type client: int
        :return: A list of Post instances or None if the request failed.
        """
        return await client.get_user_posts(self.player_id, page)

    @require_client()
    async def comments(
        self, page: int = 0, display_most_liked: bool = False, client: int = None
    ) -> List[Comment]:
        """
        Get user's comments history.

        :param page: The page number to load, default is 0.
        :type page: int
        :param display_most_liked: If sort by most liked, else sort recent.
        :type display_most_liked: bool
        :return: A list of Comment instances.
        """
        return await client.get_user_comments(self.player_id, page, display_most_liked)

    @require_client()
    async def levels(self, page: int = 0, client: int = None) -> List[LevelDisplay]:
        """
        Get user's levels.

        :param page: The page number to load, default is 0.
        :type page: int
        :return: A list of LevelDisplay instances.
        """

        return await client.get_user_levels(self.player_id, page)


@dataclass
class Account:
    """
    Represents an account (not Player) on Geometry Dash.

    Attributes
    ==========
    account_id: int
        Account ID associated with the accoount
    player_id: int
        Player ID associated with the account.
    name: Optional[str]
        Name of the account holder.
    password: str
        Plaintext password of the account.
    """

    account_id: int
    """Account ID associated with the accoount."""
    player_id: int
    """Player ID associated with the account."""
    name: Optional[str]
    """Name of the account holder."""
    password: str
    """Plaintext password of the account."""

    @property
    def gjp2(self) -> str:
        """
        Generate GJP2 hash from password. (Recommended for 2.2s)
        """
        encrypted_password = self.password + PASSWORD_SALT
        gjp = sha1(encrypted_password.encode()).hexdigest()
        return gjp

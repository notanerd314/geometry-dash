"""
## .models.users
A module containing all the classes and methods related to users and accounts in Geometry Dash.
"""

from ..helpers import *
from .enums import *
from .cosmetics import *
from .level import Comment, LevelDisplay
from typing import List, Optional, Union
from dataclasses import dataclass
from .entity import Entity
from hashlib import sha1
import colorama as color
import base64

color.init(autoreset=True)

_secret = "Wmfd2893gb7"
PASSWORD_SALT = "mI29fmAnxgTs"

@dataclass
class Post:
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
    def from_raw(raw_str: str, account_id: int = None) -> 'Post':
        """
        A static method that converts the raw data from the server into a Post instance.

        :param raw_str: The raw data from the server.
        :type raw_str: str
        :param account_id: The account ID of the user, optional if not provided.

        :type account_id: Union[int, None]
        :return: A Post instance.
        """
        parsed = raw_str.split(":")
        comment_value = parse_key_value_pairs(parsed[0], '~')

        try:
            return Post(
                content=decrypt_data(comment_value.get("2", "")),
                likes=int(comment_value.get("4", 0)),
                post_id=int(comment_value.get("6", 0)),
                posted_ago=comment_value.get("9", None),
                author_account_id=account_id
            )
        except Exception as e:
            raise ParseError(f"Failed to parse the data provided, error: {e}")
        
#* Classes representing stats
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
    def from_raw(raw_str: str) -> 'Player':
        """
        Parse the string data from the servers and returns an Player instance.

        :param raw_str: The raw data from the server.
        :type raw_str: str
        :return: An instance of the Player class.                                     
        """
        parsed = parse_key_value_pairs(raw_str)
        demon_stats = parsed.get('55', None)
        normal_stats = parsed.get('56', None)
        platformer_stats = parsed.get('57', None)

        try:
            return Player(
                name=parsed.get('1', None),
                player_id=parsed.get('2', 0),
                account_id=parsed.get('16', 0),
                stars=parsed.get('3', 0),
                moons=parsed.get('52', 0),
                demons=parsed.get('4', 0),
                diamonds=parsed.get('46'),
                rank=parsed.get('30'),
                creator_points=parsed.get('8', 0),
                secret_coins=parsed.get('13', 0),
                user_coins=parsed.get('17', 0),
                registered=True if parsed.get('29') == 1 else False,
                mod_level=ModRank(parsed.get('49', 0)),

                profile_icon_type=Gamemode(parsed.get('14', 1)),
                primary_color_id=int(parsed.get('10', 0)),
                secondary_color_id=int(parsed.get('11', 0)),
                glow_color_id=int(parsed.get('51')) if parsed.get('51', None) is not None else None,

                youtube=parsed.get('20', None) if parsed.get('20') != r"%%00" else None,
                twitter=parsed.get('44'),
                twitch=parsed.get('45'),

                classic_demon_stats=DemonStats(
                    easy=demon_stats[0],
                    medium=demon_stats[1],
                    hard=demon_stats[2],
                    insane=demon_stats[3],
                    extreme=demon_stats[4],
                    weekly=demon_stats[10],
                    guantlet=demon_stats[11]
                ) if demon_stats else None,
                platformer_demon_stats=DemonStats(
                    easy=demon_stats[5],
                    medium=demon_stats[6],
                    hard=demon_stats[7],
                    insane=demon_stats[8],
                    extreme=demon_stats[9]
                ) if demon_stats else None,
                classic_stats=DifficultyStats(
                    auto=normal_stats[0],
                    easy=normal_stats[1],
                    normal=normal_stats[2],
                    hard=normal_stats[3],
                    harder=normal_stats[4],
                    insane=normal_stats[5],
                    daily=normal_stats[6],
                    guantlet=normal_stats[7]
                ),
                platformer_stats=DifficultyStats(
                    auto=platformer_stats[0],
                    easy=platformer_stats[1],
                    normal=platformer_stats[2],
                    hard=platformer_stats[3],
                    harder=platformer_stats[4],
                    insane=platformer_stats[5]
                )
            )
        except Exception as e:
            raise ParseError(f"Could not parse the data provided, error: {e}")

    async def posts(self, page: int = 0) -> List[Post] | None:
        """
        Load all posts from the user.

        :param page: The page number to load, default is 0.
        :type page: int
        :return: A list of Post instances or None if the request failed.
        """
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJAccountComments20.php",
            data={'secret': _secret, "accountID": self.account_id, "page": page}
        )

        check_errors(response, LoadError, f"Something wrong had happened when fetching the user's posts.")
        if not response.split("#")[0]:
            return None

        posts_list = []
        parsed_res = response.split("#")[0]
        parsed_res = response.split("|")
        for post in parsed_res:
            posts_list.append(Post.from_raw(post, self.account_id))
        return posts_list
        
    async def comments(self, page: int = 0, display_most_liked: bool = False) -> List[Comment]:
        """
        Get user's comments history.

        :param page: The page number to load, default is 0.
        :type page: int
        :param display_most_liked: If True, display most liked comments, otherwise display newest comments.
        :type display_most_liked: bool
        :return: A list of Comment instances.
        """
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJCommentHistory.php",
            data={'secret': _secret, "userID": self.player_id, "page": page, "mode": int(display_most_liked)}
        )
        check_errors(response, LoadError, f"Something wrong had happened when fetching the user's comments.")
        if not response.split("#")[0]:
            return None
        
        return [Comment.from_raw(comment_data) for comment_data in response.split("#")[0].split("|")]

    async def levels(self, page: int = 0) -> List[LevelDisplay]:
        """
        Get user's levels.

        :param page: The page number to load, default is 0.
        :type page: int
        :return: A list of LevelDisplay instances.
        """

        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJLevels21.php",
            data={'secret': _secret, "type": 5, "page": page, "str": self.player_id}
        )

        check_errors(response, LoadError, f"Something wrong had happened when fetching the user's levels.")
        if not response.split("#")[0]:
            return None
        
        return [LevelDisplay.from_raw(level_data) for level_data in response.split("#")[0].split("|")]

@dataclass
class Account:
    """
    Represents an account (not Player) on Geometry Dash.
    """
    account_id: int
    player_id: int
    name: Optional[str]
    password: str

    @property
    def gjp2(self) -> str:
        """
        Generate GJP2 hash from password.
        """
        encrypted_password = self.password + PASSWORD_SALT
        hash = sha1(encrypted_password.encode()).hexdigest()
        return hash
    
    def __repr__(self) -> str:
        return f"Account(account_id={self.account_id}, player_id={self.player_id}, name='{self.name}', password=********)"
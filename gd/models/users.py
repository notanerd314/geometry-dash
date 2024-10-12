"""
## .models.users
A module containing all the classes and methods related to users and accounts in Geometry Dash.
"""

from ..helpers import *
from .enums import *
from .icons import *
from .level import LevelComment
from typing import List, Optional, Union
from dataclasses import dataclass

_secret = "Wmfd2893gb7"

@dataclass
class ProfilePost:
    """
    A class representing a post from an account.

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
    content: str
    likes: int
    post_id: int
    posted_ago: str
    author_account_id: Union[int, None]

    @staticmethod
    def from_raw(raw_str: str, account_id: int = None) -> 'ProfilePost':
        """
        A static method that converts the raw data from the server into a ProfilePost instance.

        :param raw_str: The raw data from the server.
        :type raw_str: str
        :param account_id: The account ID of the user.
        :type account_id: int
        :return: A ProfilePost instance.
        """
        parsed = raw_str.split(":")
        comment_value = parse_key_value_pairs(parsed[0], '~')

        return ProfilePost(
            content=decrypt_data(comment_value.get("2", "")),
            likes=int(comment_value.get("4", 0)),
            post_id=int(comment_value.get("6", 0)),
            posted_ago=comment_value.get("9", None),
            author_account_id=account_id
        )

@dataclass
class UserProfile:
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
    mod_level : Optional[ModLevel]
        The mod level of the user.
    primary_color : Optional[Color]
        The primary color of the user's icon.
    secondary_color : Optional[Color]
        The secondary color of the user's icon.
    glow_color : Optional[Color]
        The glow color of the user's icon.
    profile_icon_type : Optional[Gamemode]
        The gamemode that the user primarily chooses to display.
    youtube : Union[str, None]
        The YouTube channel link of the user.
    twitter_or_x : Union[str, None]
        The Twitter (or X) username of the user.
    twitch : Union[str, None]
        The Twitch username of the user.
    """
    name: str
    player_id: int
    account_id: int
    stars: Optional[int]
    moons: Optional[int]
    demons: Optional[int]
    diamonds: Optional[int]
    rank: Optional[int]
    creator_points: Optional[int]
    secret_coins: Optional[int]
    user_coins: Optional[int]
    registered: Optional[bool]
    mod_level: Optional[ModLevel]

    primary_color: Optional[Color]
    secondary_color: Optional[Color]
    glow_color: Optional[Color]
    profile_icon_type: Optional[Gamemode]
    
    youtube: Optional[str]
    twitter_or_x: Optional[str]
    twitch: Optional[str]

    @staticmethod
    def from_raw(raw_str: str) -> 'UserProfile':
        """
        Parse the string data from the servers and returns an UserProfile instance.

        :param raw_str: The raw data from the server.
        :type raw_str: str
        :return: An instance of the UserProfile class.                                     
        """
        parsed = parse_key_value_pairs(raw_str)
        return UserProfile(
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
            mod_level=ModLevel(parsed.get('49', 0)),

            profile_icon_type=Gamemode(parsed.get('14', 1)),
            primary_color=Color(parsed.get('10', 0), ColorType.primary),
            secondary_color=Color(parsed.get('11', 0), ColorType.secondary),
            glow_color=Color(parsed.get('51', 0), ColorType.glow),

            youtube=parsed.get('20', None) if parsed.get('20') != r"%%00" else None,
            twitter_or_x=parsed.get('44'),
            twitch=parsed.get('45')
        )

    async def load_posts(self, page: int = 0) -> List[ProfilePost] | None:
        """
        Load all posts from the user.

        :param page: The page number to load, default is 0.
        :type page: int
        :return: A list of ProfilePost instances or None if the request failed.
        """
        account_id = self.account_id
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJAccountComments20.php",
            data={'secret': _secret, "accountID": account_id, "page": page}
        )

        if response:
            posts_list = []
            parsed_res = response.split("|")
            for post in parsed_res:
                posts_list.append(ProfilePost.from_raw(post, account_id))
            return posts_list
        
    async def load_comments_history(self, page: int = 0, display_most_liked: bool = False) -> List[LevelComment]:
        """
        Get user's comments history.

        :param page: The page number to load, default is 0.
        :type page: int
        :param display_most_liked: If True, display most liked comments, otherwise display newest comments.
        :type display_most_liked: bool
        :return: A list of LevelComment instances.
        """
        player_id = self.player_id
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJCommentHistory.php",
            data={'secret': self.secret, "playerID": player_id, "page": page, "mode": int(display_most_liked)}
        )
        return [LevelComment.from_raw(comment_data) for comment_data in response.split("|")]
        
    async def reload(self) -> 'UserProfile':
        """
        Reload user profile by account ID and returns the UserProfile instance.

        :return: An instance of the UserProfile class.
        """
        account_id = self.account_id
        if isinstance(account_id, int):
            url = "http://www.boomlings.com/database/getGJUserInfo20.php"
            data = {'secret': _secret, "targetAccountID": account_id}

        response = await send_post_request(url=url, data=data)
        return UserProfile.from_raw(response)
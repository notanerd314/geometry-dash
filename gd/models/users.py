from ..helpers import *
from .enums import *
from .icons import *
from .level import LevelComment
from typing import List, Optional, Union
from dataclasses import dataclass

_secret = "Wmfd2893gb7"

@dataclass
class ProfilePost:
    content: str
    likes: int
    message_id: int
    posted_ago: str
    author_account_id: int

    @staticmethod
    def from_raw(raw_str: str, account_id: int) -> 'ProfilePost':
        parsed = raw_str.split(":")
        comment_value = parse_key_value_pairs(parsed[0], '~')

        return ProfilePost(
            content=decrypt_data(comment_value.get("2", "")),
            likes=int(comment_value.get("4", 0)),
            message_id=int(comment_value.get("6", 0)),
            posted_ago=comment_value.get("9", None),
            author_account_id=account_id
        )

@dataclass
class UserProfile:
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

    first_color: Optional[Color]
    second_color: Optional[Color]
    glow_color: Optional[Color]
    profile_icon_type: Optional[Gamemode]
    
    youtube: Optional[str]
    twitter_or_x: Optional[str]
    twitch: Optional[str]

    @staticmethod
    def from_raw(raw_str: str) -> 'UserProfile':
        """
        Parse the string data from the servers and returns an UserProfile instance.

        Parameters:
            rawex       (str):  The string data to parse                            tyu t   yv                                               
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
            first_color=Color(parsed.get('10', 0), ColorType.primary),
            second_color=Color(parsed.get('11', 0), ColorType.secondary),
            glow_color=Color(parsed.get('51', 0), ColorType.glow),

            youtube=parsed.get('20', None) if parsed.get('20') != r"%%00" else None,
            twitter_or_x=parsed.get('44'),
            twitch=parsed.get('45')
        )

    async def load_posts(self, page: int = 0) -> List[ProfilePost] | None:
        """Get user's posts by Account ID"""
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
        
    async def load_comments_history(self, page: int = 0, display_most_liked: bool = False):
        """Get user's comments history, note that the author information won't be displayed."""
        player_id = self.player_id
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJCommentHistory.php",
            data={'secret': self.secret, "playerID": player_id, "page": page, "mode": int(display_most_liked)}
        )
        return [LevelComment.from_raw(comment_data) for comment_data in response.split("|")]
        
    async def reload(self) -> 'UserProfile':
        """Reload user profile by account ID and returns the UserProfile instance."""
        account_id = self.account_id
        if isinstance(account_id, int):
            url = "http://www.boomlings.com/database/getGJUserInfo20.php"
            data = {'secret': _secret, "targetAccountID": account_id}

        response = await send_post_request(url=url, data=data)
        return UserProfile.from_raw(response)
from ..ext import *
from .enums import *
from .icons import *
from typing import List, Optional, Union
from dataclasses import dataclass

@dataclass
class UserProfile:
    name: str
    id: int
    stars: Optional[int]
    demons: Optional[int]
    diamonds: Optional[int]
    leaderboard_rank: Optional[int]
    creator_points: Optional[int]
    coins: Optional[int]
    user_coins: Optional[int]
    registered: Optional[bool]
    mod_level: Optional[ModLevel]

    first_color: Optional[Color]
    second_color: Optional[Color]
    profile_icon_type: Optional[Gamemode]
    
    youtube: Optional[str]
    twitter_or_x: Optional[str]
    twitch: Optional[str]

    @classmethod
    def from_raw(raw_str: str):
        parsed = parse_key_value_pairs(raw_str)

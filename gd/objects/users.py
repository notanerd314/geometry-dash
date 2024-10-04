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
    moons: Optional[int]
    demons: Optional[int]
    diamonds: Optional[int]
    leaderboard_rank: Optional[int]
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
    def from_raw(raw_str: str):
        parsed = parse_key_value_pairs(raw_str)
        print(parsed)
        return UserProfile(
            name=parsed.get('1', None),
            id=parsed.get('2', 0),
            stars=parsed.get('3', 0),
            moons=parsed.get('52', 0),
            demons=parsed.get('4', 0),
            diamonds=parsed.get('46'),
            leaderboard_rank=parsed.get('6'),
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

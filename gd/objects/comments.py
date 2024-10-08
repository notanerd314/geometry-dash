from ..ext import parse_key_value_pairs, decrypt_data
from dataclasses import dataclass
from .icons import *
from .enums import Gamemode

__GAMEMODE_ORDER__ = ["icon", "ship", "ball", "ufo", "wave", "robot", "spider"]

@dataclass
class LevelComment:
    level_id: int
    content: str
    likes: int
    message_id: int
    is_spam: bool
    posted_ago: str
    precentage: int
    mod_level: ModLevel

    author_player_id: int
    author_account_id: int
    author_name: str
    author_primary_color: Color
    author_secondary_color: Color
    author_has_glow: bool
    author_icon: Icon
    author_icon_display_gamemode: Gamemode

    @staticmethod
    def from_raw(raw_str: str) -> 'LevelComment':
        parsed = raw_str.split(":")
        user_value = parse_key_value_pairs(parsed[1], "~")
        comment_value = parse_key_value_pairs(parsed[0], '~')

        return LevelComment(
            level_id=int(comment_value.get("1", 0)),
            content=decrypt_data(comment_value.get("2", "")),
            author_player_id=int(comment_value.get("3", 0)),
            author_account_id=int(str(user_value.get("16", 0)).split("#")[0]),
            likes=int(comment_value.get("4", 0)),
            message_id=int(comment_value.get("6", 0)),
            is_spam=bool(int(comment_value.get("7", 0))),
            posted_ago=comment_value.get("9", None),
            precentage=int(comment_value.get("10", 0)),
            mod_level=ModLevel(int(comment_value.get("11", 0))),

            author_name=user_value.get("1", ""),
            author_icon=Icon(user_value.get("9", ""), gamemode=Gamemode(int(user_value.get("14", 0)))),
            author_icon_display_gamemode=Gamemode(int(user_value.get("14", 0))),
            author_primary_color=Color(int(user_value.get("10", 1)), ColorType.primary),
            author_secondary_color=Color(int(user_value.get("11", 1)), ColorType.secondary),
            author_has_glow=bool(int(user_value.get("15", 0))),
        )

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
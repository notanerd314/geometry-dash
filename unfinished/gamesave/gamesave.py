"""
# gd.gamesave.gamesave

A module for all gamesave related classes and functions.
"""

from typing import Optional, NamedTuple
from enum import Enum

import attr

from gd.cryptography import (
    singular_xor,
    base64_urlsafe_gzip_decompress,
    XorKey,
    generate_udid,
)
from gd.parse import gamesave_to_dict
from gd.type_hints import (
    Udid,
    IconDeathEffectId,
    IconShipTrailId,
    IconTrailId,
    IconId,
    ColorId,
)
from gd.entities.cosmetics import IconSet
from gd.entities.enums import Gamemode
from gd.entities.user import Account
from unfinished.gamesave.helpers import filter_valuekeeper_keys_by_type

# Boilerplates


class TextureQuality(Enum):
    """
    An enum representing a texture quality.
    """

    AUTO = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3


Resolution = NamedTuple(
    "Resolution",
    [
        ("width", int),
        ("height", int),
    ],
)
"""Resolution of the window of Geometry Dash."""

Position = NamedTuple(
    "Position",
    [
        ("x", float),
        ("y", float),
    ],
)
"""A namedtuple for the coordinates of an object in 2D."""

resolution_map = {
    1: Resolution(640, 480),
    2: Resolution(720, 480),
    3: Resolution(720, 576),
    4: Resolution(800, 600),
    5: Resolution(1024, 768),
    6: Resolution(1152, 864),
    7: Resolution(1176, 664),
    8: Resolution(1280, 720),
    9: Resolution(1280, 768),
    10: Resolution(1280, 800),
    11: Resolution(1280, 960),
    12: Resolution(1280, 1024),
    13: Resolution(1360, 768),
    14: Resolution(1366, 768),
    15: Resolution(1440, 900),
    16: Resolution(1600, 900),
    17: Resolution(1600, 1024),
    18: Resolution(1600, 1200),
    19: Resolution(1680, 1050),
    20: Resolution(1768, 992),
    21: Resolution(1920, 1080),
    22: Resolution(1920, 1200),
    23: Resolution(1920, 1440),
    24: Resolution(2048, 1536),
    25: Resolution(2560, 1440),
    26: Resolution(2560, 1600),
    27: Resolution(3840, 2160),
}

# Gamesave


@attr.define(slots=True)
class Gamesave:
    """
    A class representing a Gamesave file.
    """

    music_volume: float = attr.field(default=1.0)
    sfx_volume: float = attr.field(default=1.0)
    udid: Udid = attr.field(factory=generate_udid)
    account: Account
    icon_set: IconSet
    trail: IconTrailId
    ship_trail: IconShipTrailId
    death_effect: IconDeathEffectId
    glow_enabled: bool
    main_gamemode: Gamemode
    cod3breaker: Optional[int]
    is_moderator: bool
    times_played: int
    fps: float
    ms_offset: float
    resolution: Resolution
    texture_quality: TextureQuality
    practice_ui_opacity: float
    practice_ui_position: Position
    clicked_garage: bool
    clicked_editor: bool
    clicked_practice: bool
    clicked_editor_guide: bool
    clicked_ldm: bool
    clicked_rating_explanation: bool
    unlocked_cubes: list[IconId]
    unlocked_ships: list[IconId]
    unlocked_balls: list[IconId]
    unlocked_ufos: list[IconId]
    unlocked_waves: list[IconId]
    unlocked_robots: list[IconId]
    unlocked_spiders: list[IconId]
    unlocked_swings: list[IconId]
    unlocked_jetpacks: list[IconId]
    unlocked_primary_colors: list[ColorId]
    unlocked_secondary_colors: list[ColorId]
    unlocked_trails: list[IconTrailId]
    unlocked_ship_trails: list[IconShipTrailId]
    unlocked_death_effects: list[IconDeathEffectId]

    @staticmethod
    def load(gamesave: str) -> "Gamesave":
        """
        Loads and returns the gamesave data from CCGameManager.dat.

        :raises: LoadError
        :param path: CCGameManager.dat converted to readable string.
        :type path: str
        :return: The gamesave data as a dictionary.
        :rtype: dict
        """
        decoded = singular_xor(gamesave, int(XorKey.GAMESAVE))
        decompressed = base64_urlsafe_gzip_decompress(decoded)
        gamesave = gamesave_to_dict(decompressed)
        valuekeeper = gamesave.get("valueKeeper")

        return Gamesave(
            music_volume=gamesave.get("bgVolume", 0.0),
            sfx_volume=gamesave.get("sfxVolume", 0.0),
            udid=gamesave.get("playerUDID", ""),
            account=Account(
                name=gamesave.get("playerName", ""),
                password=gamesave.get("GJA_002", ""),
                player_id=gamesave.get("playerUserID", 0),
                account_id=gamesave.get("playerAccountID", 0),
            ),
            icon_set=IconSet.load(
                cube=gamesave.get("playerFrame", 1),
                ship=gamesave.get("playerShip", 1),
                ball=gamesave.get("playerBall", 1),
                ufo=gamesave.get("playerBird", 1),
                wave=gamesave.get("playerDart", 1),
                robot=gamesave.get("playerRobot", 1),
                spider=gamesave.get("playerSpider", 1),
                swing=gamesave.get("playerSwing", 1),
                jetpack=gamesave.get("playerJetpack", 1),
                primary_color=gamesave.get("playerColor", 0),
                secondary_color=gamesave.get("playerColor2", 0),
                glow_color=gamesave.get("playerColor3", None),
            ),
            trail=gamesave.get("playerStreak", 0),
            ship_trail=gamesave.get("playerShipStreak", 0),
            death_effect=gamesave.get("playerDeathEffect", 0),
            glow_enabled=gamesave.get("playerGlow", False),
            main_gamemode=Gamemode(gamesave.get("playerIconType", 0)),
            cod3breaker=gamesave.get("secretNumber", None),
            is_moderator=gamesave.get("hasRP", False),
            times_played=gamesave.get("bootups", 0),
            fps=gamesave.get("customFPSTarget", 0.0),
            ms_offset=gamesave.get("timeOffset", 0.0),
            texture_quality=TextureQuality(gamesave.get("textureQuality", 0)),
            resolution=resolution_map[gamesave.get("resolution", 21)],
            practice_ui_opacity=gamesave.get("practiceOpacity", 0.0),
            practice_ui_position=Position(
                x=gamesave.get("practicePosX", 0.0),
                y=gamesave.get("practicePosY", 0.0),
            ),
            clicked_garage=gamesave.get("clickedGarage", False),
            clicked_editor=gamesave.get("clickedEditor", False),
            clicked_practice=gamesave.get("clickedPractice", False),
            clicked_editor_guide=gamesave.get("showedEditorGuide", False),
            clicked_ldm=gamesave.get("showedLowDetailDialog", False),
            clicked_rating_explanation=gamesave.get("showedRateStarDialog", False),
            unlocked_cubes=filter_valuekeeper_keys_by_type(valuekeeper, "i"),
            unlocked_ships=filter_valuekeeper_keys_by_type(valuekeeper, "ship"),
            unlocked_balls=filter_valuekeeper_keys_by_type(valuekeeper, "ball"),
            unlocked_ufos=filter_valuekeeper_keys_by_type(valuekeeper, "bird"),
            unlocked_waves=filter_valuekeeper_keys_by_type(valuekeeper, "dart"),
            unlocked_robots=filter_valuekeeper_keys_by_type(valuekeeper, "robot"),
            unlocked_spiders=filter_valuekeeper_keys_by_type(valuekeeper, "spider"),
            unlocked_swings=filter_valuekeeper_keys_by_type(valuekeeper, "swing"),
            unlocked_jetpacks=filter_valuekeeper_keys_by_type(valuekeeper, "jetpack"),
            unlocked_primary_colors=filter_valuekeeper_keys_by_type(valuekeeper, "c0"),
            unlocked_secondary_colors=filter_valuekeeper_keys_by_type(
                valuekeeper, "c1"
            ),
            unlocked_trails=filter_valuekeeper_keys_by_type(valuekeeper, "streak"),
            unlocked_ship_trails=filter_valuekeeper_keys_by_type(
                valuekeeper, "shipstreak"
            ),
            unlocked_death_effects=filter_valuekeeper_keys_by_type(
                valuekeeper, "death"
            ),
        )

    # def xml(self) -> str:
    #     """
    #     Returns the gamesave data as raw minified XML string.
    #     """
    #     root = etree.Element("plist", version="1.0", gjver="2.0")
    #     gamesave = etree.SubElement(root, "dict")

    #     xml_data = etree.tostring(root)
    #     return xml_data

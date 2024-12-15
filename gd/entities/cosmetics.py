"""
## .entities.icons

The module containing all the classes and methods related to customization and icons.
"""

from typing import Union, Optional
from io import BytesIO
from pathlib import Path
import asyncio

import attr

from gd.entities.enums import Gamemode
from gd.helpers import send_get_request
from gd.type_hints import ColorId, IconId, ColorHex
from gd.helpers import write

__all__ = ["color_id_to_hex", "Icon", "IconSet"]

COLORS_LIST: dict[ColorId, ColorHex] = {
    0: 0x7DFF00,
    1: 0x00FF00,
    2: 0x00FF7D,
    3: 0x00FFFF,
    4: 0x007DFF,
    5: 0x0000FF,
    6: 0x7D00FF,
    7: 0xFF00FF,
    8: 0xFF007D,
    9: 0xFF0000,
    10: 0xFF7D00,
    11: 0xFFFF00,
    12: 0xFFFFFF,
    13: 0xB900FF,
    14: 0xFFB900,
    15: 0x000000,
    16: 0x00C8FF,
    17: 0xAFAFAF,
    18: 0x5A5A5A,
    19: 0xFF7D7D,
    20: 0x00AF4B,
    21: 0x007D7D,
    22: 0x004BB1,
    23: 0x4B00AF,
    24: 0x7D007D,
    25: 0xAF004B,
    26: 0xAF4B00,
    27: 0x7D7D00,
    28: 0x4BAF00,
    29: 0xFF4B00,
    30: 0x962800,
    31: 0x966400,
    32: 0x64AF00,
    33: 0x00AF64,
    34: 0x0064AF,
    35: 0x6400AF,
    36: 0x960064,
    37: 0x960000,
    38: 0x00AF00,
    39: 0x0000AF,
    40: 0x7DFFAF,
    41: 0x7D7DFF,
    42: 0xFFFA7F,
    43: 0xFA7FFF,
    44: 0x00FFBF,
    45: 0x50320E,
    46: 0xCDA576,
    47: 0xB680FF,
    48: 0xFF3A3A,
    49: 0x4D4D8F,
    50: 0x000A4C,
    51: 0xFDD4CE,
    52: 0xBEB5FF,
    53: 0x700000,
    54: 0x520200,
    55: 0x380106,
    56: 0x805050,
    57: 0x7A3535,
    58: 0x512424,
    59: 0xA36246,
    60: 0x753736,
    61: 0x563528,
    62: 0xFFB972,
    63: 0xFFA040,
    64: 0x66311E,
    65: 0x5B2700,
    66: 0x472000,
    67: 0xA77B4D,
    68: 0x6D5339,
    69: 0x513E2A,
    70: 0xFFFFC0,
    71: 0xFDD0A0,
    72: 0xB8FFA0,
    73: 0xB1FF6D,
    74: 0xB8FFDC,
    75: 0x94FFEC,
    76: 0x43A18A,
    77: 0x316D5F,
    78: 0x265453,
    79: 0x006000,
    80: 0x004000,
    81: 0x006060,
    82: 0x004040,
    83: 0xA0FFFF,
    84: 0x010770,
    85: 0x00496D,
    86: 0x003238,
    87: 0x002638,
    88: 0x5080AD,
    89: 0x335375,
    90: 0x233C56,
    91: 0xDCDCDC,
    92: 0x3D068C,
    93: 0x370860,
    94: 0x404040,
    95: 0x6F49A4,
    96: 0x56367F,
    97: 0x422A63,
    98: 0xFCD5FF,
    99: 0xAF57AF,
    100: 0x823D82,
    101: 0x5E315E,
    102: 0x808080,
    103: 0x66033E,
    104: 0x470132,
    105: 0xD2FF32,
    106: 0x76BDFF,
}

"""A dictionary mapping all the color ids to their corresponding hex colors.

**Minimum ID:** 0, **Maximum ID:** 106
"""

ICON_RENDERER = "https://gdicon.oat.zone/icon"
"""API endpoint for render_to_bytesing Geometry Dash icons."""


def color_id_to_hex(color_id: ColorId) -> Union[int, None]:
    """
    Returns the hexadecimal color code for the given color ID. If not found, returns None.

    :param color_id: The ID of the color.
    :type color_id: ColorId
    :return: The hexadecimal color code if found, otherwise None.
    """
    return COLORS_LIST[color_id]


@attr.define(slots=True)
class Icon:
    """
    A **dataclass** representing the icon of a specific gamemode and ID.

    Attributes
    ----------
    id : IconId
        The ID of the icon
    gamemode : Gamemode
        The gamemode of
    primary_color_id : ColorId
        The primary color ID of the icon
    secondary_color_id : ColorId
        The secondary color ID of the icon
    glow_color_id : Optional[ColorId]
        The glow color ID of the icon, if doesn't exist then None.
    """

    id: IconId
    gamemode: Gamemode
    primary_color_id: ColorId = 1
    secondary_color_id: ColorId = 1
    glow_color_id: Optional[ColorId] = None

    @property
    def primary_color_hex(self) -> ColorHex:
        """
        Returns the primary color ID as a hexadecimal color code.
        """
        return hex(color_id_to_hex(self.primary_color_id)).replace("0x", "")

    @property
    def secondary_color_hex(self) -> ColorHex:
        """
        Returns the secondary color ID as a hexadecimal color code.
        """
        return hex(color_id_to_hex(self.secondary_color_id)).replace("0x", "")

    @property
    def glow_color_hex(self) -> ColorHex:
        """
        Returns the glow color ID as a hexadecimal color code if it exists.

        :raises: ValueError
        """
        if self.glow_color_id is None:
            raise ValueError("This icon has no glow color.")

        return hex(color_id_to_hex(self.glow_color_id)).replace("0x", "")

    async def download_to(self, path: Union[str, Path] = "*/") -> None:
        """
        Downloads the icon to a specified path.

        :param path: Full path to save the file, including filename.
        :type path: Union[str, Path]
        :raises ValueError: If the file extension is invalid.
        :raises FileExistsError: If the file already exists at the specified path.
        :return: None
        :rtype: None
        """
        path = Path(path)
        content = await self.render_to_bytes(extension=path.suffix)
        await write(content, path)

    async def render_to_bytes(self, extension: str = "png") -> BytesIO:
        """
        Renders the icon and returns a BytesIO representation.

        :param extension: The file extension to get.
        :type extension: str
        :return: BytesIO representation of the icon.
        :rtype: io.BytesIO
        """
        params = {
            "type": self.gamemode.name.lower(),
            "value": self.id,
            "color1": self.primary_color_hex,
            "color2": self.secondary_color_hex,
        }

        if self.glow_color_id:
            params["glow"] = self.glow_color_hex

        response = await send_get_request(
            url=f"{ICON_RENDERER}.{extension}", params=params, timeout=30
        )

        return BytesIO(response.content)


@attr.define(slots=True)
class IconSet:
    """
    A **dataclass** representing a set of icons.

    Attributes
    ==========
    cube : Icon
    ship : Icon
    ball : Icon
    ufo : Icon
    wave : Icon
    robot : Icon
    spider : Icon
    swing : Icon
    jetpack : Icon
    """

    cube: Icon
    ship: Icon
    ball: Icon
    ufo: Icon
    wave: Icon
    robot: Icon
    spider: Icon
    swing: Icon
    jetpack: Icon

    @staticmethod
    def load(
        cube: IconId = 1,
        ship: IconId = 1,
        ball: IconId = 1,
        ufo: IconId = 1,
        wave: IconId = 1,
        robot: IconId = 1,
        spider: IconId = 1,
        swing: IconId = 1,
        jetpack: IconId = 1,
        primary_color: ColorId = 0,
        secondary_color: ColorId = 0,
        glow_color: Optional[ColorId] = None,
    ) -> "IconSet":
        """
        A function to creator an user's icon set fast.

        :param cube: Cube icon ID.
        :type cube: IconId
        :param ship: Ship icon ID.
        :type ship: IconId
        :param ball: Ball icon ID.
        :type ball: IconId
        :param ufo: UFO icon ID.
        :type ufo: IconId
        :param wave: Wave icon ID.
        :type wave: IconId
        :param robot: Robot icon ID.
        :type robot: IconId
        :param spider: Spider icon ID.
        :type spider: IconId
        :param swing: Swing icon ID.
        :type swing: IconId
        :param jetpack: Jetpack icon ID.
        :type jetpack: IconId
        :param primary_color: Primary color ID.
        :type primary_color: ColorId
        :param secondary_color: Secondary color ID.
        :type secondary_color: ColorId
        :param glow_color: Glow color ID.
        :type glow_color: Optional[ColorId]
        :return: IconSet instance.
        :rtype: IconSet
        """
        return IconSet(
            cube=Icon(
                id=cube,
                gamemode=Gamemode.CUBE,
                primary_color_id=primary_color,
                secondary_color_id=secondary_color,
                glow_color_id=glow_color,
            ),
            ship=Icon(
                id=ship,
                gamemode=Gamemode.SHIP,
                primary_color_id=primary_color,
                secondary_color_id=secondary_color,
                glow_color_id=glow_color,
            ),
            ball=Icon(
                id=ball,
                gamemode=Gamemode.BALL,
                primary_color_id=primary_color,
                secondary_color_id=secondary_color,
                glow_color_id=glow_color,
            ),
            ufo=Icon(
                id=ufo,
                gamemode=Gamemode.UFO,
                primary_color_id=primary_color,
                secondary_color_id=secondary_color,
                glow_color_id=glow_color,
            ),
            wave=Icon(
                id=wave,
                gamemode=Gamemode.WAVE,
                primary_color_id=primary_color,
                secondary_color_id=secondary_color,
                glow_color_id=glow_color,
            ),
            robot=Icon(
                id=robot,
                gamemode=Gamemode.ROBOT,
                primary_color_id=primary_color,
                secondary_color_id=secondary_color,
                glow_color_id=glow_color,
            ),
            spider=Icon(
                id=spider,
                gamemode=Gamemode.SPIDER,
                primary_color_id=primary_color,
                secondary_color_id=secondary_color,
                glow_color_id=glow_color,
            ),
            swing=Icon(
                id=swing,
                gamemode=Gamemode.SWING,
                primary_color_id=primary_color,
                secondary_color_id=secondary_color,
                glow_color_id=glow_color,
            ),
            jetpack=Icon(
                id=jetpack,
                gamemode=Gamemode.JETPACK,
                primary_color_id=primary_color,
                secondary_color_id=secondary_color,
                glow_color_id=glow_color,
            ),
        )

    async def render_all_to_bytes(self, extension: str = "png") -> list[BytesIO]:
        """
        Renders all icons and returns a dictionary of BytesIO objects.

        :param extension: The file extension to get.
        :type extension: str
        :return: BytesIO representation of the icon.
        :rtype: list[io.BytesIO]
        """
        results = await asyncio.gather(
            self.cube.render_to_bytes(extension=extension),
            self.ship.render_to_bytes(extension=extension),
            self.ball.render_to_bytes(extension=extension),
            self.ufo.render_to_bytes(extension=extension),
            self.wave.render_to_bytes(extension=extension),
            self.robot.render_to_bytes(extension=extension),
            self.spider.render_to_bytes(extension=extension),
            self.swing.render_to_bytes(extension=extension),
            self.jetpack.render_to_bytes(extension=extension),
        )
        return results

    async def download_all_to(self, path: Union[str, Path] = "*/") -> None:
        """
        Downloads all icons to a specified path.

        :param path: Full path to save the files, including directory.
        :type path: Union[str, Path]
        :return: None
        :rtype: None
        """
        path = Path(path)
        icons = await self.render_all_to_bytes(path.suffix)
        tasks = [write(icon, path) for icon in icons.values()]
        await asyncio.gather(*tasks)

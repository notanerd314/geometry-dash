"""
## .models.icons

The module containing all the classes and methods related to customization and icons.
"""

from dataclasses import dataclass
from .enums import Gamemode
from ..helpers import *
from ..exceptions import DownloadIconError
from ..parse import parse_str_literal, dict_syntax_to_tuple
from typing import Union, Dict
from io import BytesIO
from pathlib import Path
import aiofiles

COLORS_LIST: Dict[int, int] = {
    "0": 0x7DFF00,
    "1": 0x00FF00,
    "2": 0x00FF7D,
    "3": 0x00FFFF,
    "4": 0x007DFF,
    "5": 0x0000FF,
    "6": 0x7D00FF,
    "7": 0xFF00FF,
    "8": 0xFF007D,
    "9": 0xFF0000,
    "10": 0xFF7D00,
    "11": 0xFFFF00,
    "12": 0xFFFFFF,
    "13": 0xB900FF,
    "14": 0xFFB900,
    "15": 0x000000,
    "16": 0x00C8FF,
    "17": 0xAFAFAF,
    "18": 0x5A5A5A,
    "19": 0xFF7D7D,
    "20": 0x00AF4B,
    "21": 0x007D7D,
    "22": 0x004BB1,
    "23": 0x4B00AF,
    "24": 0x7D007D,
    "25": 0xAF004B,
    "26": 0xAF4B00,
    "27": 0x7D7D00,
    "28": 0x4BAF00,
    "29": 0xFF4B00,
    "30": 0x962800,
    "31": 0x966400,
    "32": 0x64AF00,
    "33": 0x00AF64,
    "34": 0x0064AF,
    "35": 0x6400AF,
    "36": 0x960064,
    "37": 0x960000,
    "38": 0x00AF00,
    "39": 0x0000AF,
    "40": 0x7DFFAF,
    "41": 0x7D7DFF,
    "42": 0xFFFA7F,
    "43": 0xFA7FFF,
    "44": 0x00FFBF,
    "45": 0x50320E,
    "46": 0xCDA576,
    "47": 0xB680FF,
    "48": 0xFF3A3A,
    "49": 0x4D4D8F,
    "50": 0x000A4C,
    "51": 0xFDD4CE,
    "52": 0xBEB5FF,
    "53": 0x700000,
    "54": 0x520200,
    "55": 0x380106,
    "56": 0x805050,
    "57": 0x7A3535,
    "58": 0x512424,
    "59": 0xA36246,
    "60": 0x753736,
    "61": 0x563528,
    "62": 0xFFB972,
    "63": 0xFFA040,
    "64": 0x66311E,
    "65": 0x5B2700,
    "66": 0x472000,
    "67": 0xA77B4D,
    "68": 0x6D5339,
    "69": 0x513E2A,
    "70": 0xFFFFC0,
    "71": 0xFDD0A0,
    "72": 0xB8FFA0,
    "73": 0xB1FF6D,
    "74": 0xB8FFDC,
    "75": 0x94FFEC,
    "76": 0x43A18A,
    "77": 0x316D5F,
    "78": 0x265453,
    "79": 0x006000,
    "80": 0x004000,
    "81": 0x006060,
    "82": 0x004040,
    "83": 0xA0FFFF,
    "84": 0x010770,
    "85": 0x00496D,
    "86": 0x003238,
    "87": 0x002638,
    "88": 0x5080AD,
    "89": 0x335375,
    "90": 0x233C56,
    "91": 0xDCDCDC,
    "92": 0x3D068C,
    "93": 0x370860,
    "94": 0x404040,
    "95": 0x6F49A4,
    "96": 0x56367F,
    "97": 0x422A63,
    "98": 0xFCD5FF,
    "99": 0xAF57AF,
    "100": 0x823D82,
    "101": 0x5E315E,
    "102": 0x808080,
    "103": 0x66033E,
    "104": 0x470132,
    "105": 0xD2FF32,
    "106": 0x76BDFF
}
"""A dictionary mapping all the color ids to their corresponding hex colors.

**Minimum ID:** 0, **Maximum ID:** 106
"""

ICON_RENDERER = "https://gdicon.oat.zone/icon"
USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36 Edg/131.0.0.0"
GAMEMODE_MAP = {
    "CUBE": "player",
    "SHIP": "ship",
    "BALL": "player_ball",
    "UFO": "bird",
    "WAVE": "dart",
    "ROBOT": "robot",
    "SPIDER": "spider",
    "SWING": "swing",
    "JETPACK": "jetpack",
}


def color_id_to_hex(color_id: int) -> Union[int, None]:
    """
    Returns the hexadecimal color code for the given color ID. If not found, returns None.

    :param color_id: The ID of the color.
    :type color_id: int
    :return: The hexadecimal color code if found, otherwise None.
    """
    return COLORS_LIST.get(color_id, None)


def hex_to_color_id(hex_color: int) -> Union[int, None]:
    """
    Returns the color ID for the given hexadecimal color code. If not found, returns None.

    :param hex_color: The hex of the color.
    :type hex_color: int
    :return: The ID of the color if found, otherwise None.
    """
    for color_id, color_hex in COLORS_LIST.items():
        if color_hex == hex_color:
            return color_id
    return None


@dataclass
class Icon:
    """
    A **dataclass** representing the icon of a specific gamemode and ID.

    Attributes
    ----------
    id : int
        The ID of the icon
    gamemode : Gamemode
        The gamemode of
    primary_color_id : int
        The primary color ID of the icon
    secondary_color_id : int
        The secondary color ID of the icon
    glow_color_id : Union[int, None]
        The glow color ID of the icon, if doesn't exist then None.
    """

    id: int
    gamemode: Gamemode
    primary_color_id: int = 1
    secondary_color_id: int = 1
    glow_color_id: Union[int, None] = None

    @property
    def primary_color_hex(self) -> int:
        """
        Returns the primary color ID as a hexadecimal color code.
        """
        return color_id_to_hex(self.primary_color_id)

    @property
    def secondary_color_hex(self) -> int:
        """
        Returns the secondary color ID as a hexadecimal color code.
        """
        return color_id_to_hex(self.secondary_color_id)

    @property
    def glow_color_hex(self) -> Union[int, None]:
        """
        Returns the glow color ID as a hexadecimal color code if it exists, otherwise raise a `ValueError`.
        """
        if self.glow_color_id is None:
            raise ValueError("This icon has no glow color.")
        return color_id_to_hex(self.glow_color_id)

    async def download_to(self, path: Union[str, Path] = None) -> None:
        """
        Downloads the icon to a specified path.

        :param path: Full path to save the file, including filename. Defaults to current directory with ID as filename.
        :type path: Union[str, Path]
        """
        if path is None:
            path = (
                Path.cwd()
                / f"{self.gamemode.name.lower()}_{self.primary_color_id}_{self.secondary_color_id}_{self.glow_color_id}.png"
            )
        elif not path.suffix in {".png", ".webp", ".jpg", ".jpeg", ".ico"}:
            raise ValueError(
                "Path must end with .png, .webp, or another image extension!"
            )

        # Ensure the directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        response = await self.render(extension=path.suffix.lstrip("."))

        async with aiofiles.open(path, "wb") as file:
            await file.write(response.getvalue())

    async def render(self, extension: str = "png") -> BytesIO:
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
            "color1": self.primary_color_id,
            "color2": self.secondary_color_id,
        }

        if self.glow_color_id:
            params["glow"] = self.glow_color_id

        response = await send_get_request(
            decode=False, url=f"{ICON_RENDERER}.{extension}", params=params
        )

        return BytesIO(response)

@dataclass
class IconSet:
    """
    A **dataclass** representing a set of icons.
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

    @property
    def all_icons(self) -> Dict[Gamemode, Icon]:
        """
        Returns a dictionary of all icons in the set.
        """
        return {
            Gamemode.CUBE: self.cube,
            Gamemode.SHIP: self.ship,
            Gamemode.BALL: self.ball,
            Gamemode.UFO: self.ufo,
            Gamemode.WAVE: self.wave,
            Gamemode.ROBOT: self.robot,
            Gamemode.SPIDER: self.spider,
            Gamemode.SWING: self.swing,
            Gamemode.JETPACK: self.jetpack,
        }

    @staticmethod
    def load(
        cube: int = 1,
        ship: int = 1,
        ball: int = 1,
        ufo: int = 1,
        wave: int = 1,
        robot: int = 1,
        spider: int = 1,
        swing: int = 1,
        jetpack: int = 1,
        primary_color: int = 0,
        secondary_color: int = 0,
        glow_color: int = None,
    ) -> "IconSet":
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
    
    async def render_all(self, extension: str = "png") -> Dict[Gamemode, BytesIO]:
        """
        Renders all icons and returns a dict of BytesIO objects.

        :param extension: The file extension to get.
        :type extension: str
        :return: BytesIO representation of the icon.
        :rtype: Dict[Gamemode, io.BytesIO]
        """
        # Asynchronously gather all icon renders (likely from different 'icon.render()' tasks)
        icons = await asyncio.gather(
            *[icon.render(extension) for icon in self.all_icons.values()]
        )

        # Zip gamemodes with their corresponding icon BytesIO object
        return {gamemode: icon for gamemode, icon in zip(self.all_icons.keys(), icons)}

    async def download_all_to(self, path: Union[str, Path] = None) -> None:
        """
        Downloads all icons to a specified path.
        
        :param path: Full path to save the files, including directory.
        :type path: Union[str, Path]
        """
        # Ensure path is provided, if not, raise an error
        if path is None:
            path = Path.cwd() 
        
        # Convert path to a Path object if it's a string
        path = Path(path)
        
        # Create the directory if it doesn't exist
        path.mkdir(parents=True, exist_ok=True)

        icons = await self.render_all()
        icons = icons.items()

        # Loop through each gamemode and save the associated BytesIO object to a file
        for gamemode, icon in icons:
            # Construct the file path (e.g., "path/gamemode.png")
            file_path = path / f"{gamemode.name.lower()}.png"  # You can use any extension here

            # Write the BytesIO object to the file
            async with aiofiles.open(file_path, "wb") as file:
                await file.write(icon.getvalue())  # .getvalue() gives the raw byte data from BytesIO
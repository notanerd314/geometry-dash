from .ext import *
from .objects.level import *

_secret = "Wmfd2893gb7"

class GeometryDash:
    def __init__(self, secret: str = "") -> None:
        self.secret = secret

    async def download_level(self, id: int) -> Level:
        """
        Downloads a specific level from the Geometry Dash servers using the provided ID.

        Parameters:
            id (int, required): The ID of the level to download.
            version (int, optional): The version of the level to download, defaults to 2.2.
        """

        if not isinstance(id, int):
            raise ValueError("ID must be an int.")
        if id <= 0:
            raise ValueError("ID must be greater than 0.")

        try:
            response = await post(
                url="http://www.boomlings.com/database/downloadGJLevel22.php", 
                data={"levelID": id, "secret": self.secret}
            )
            return Level(response)
        except Exception as e:
            raise RuntimeError(f"Failed to download level: {e}")

    async def get_daily_level(self) -> Level:
        """
        Downloads the daily level from the Geometry Dash servers with the time left for it.

        The information for the time left (in seconds) in a daily is in `Level.EXTRAS` with the key `"timeLeft"`

        Parameters:
            No parameters are specificied.
        """

        try:
            response = await post(
                url="http://www.boomlings.com/database/getGJDailyLevel.php",
                data={"secret": self.secret}
            ).split("|")
        except Exception as e:
            raise RuntimeError(f"Failed to get daily level: {e}")
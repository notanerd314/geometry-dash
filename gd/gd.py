from .ext import *
from .objects.level import *
from datetime import timedelta

_secret = "Wmfd2893gb7"

class GeometryDash:
    def __init__(self, secret: str = "") -> None:
        self.secret = secret

    async def download_level(self, id: int) -> Level:
        """
        Downloads a specific level from the Geometry Dash servers using the provided ID.

        Parameters:
            id (int, required): The ID of the level to download.
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

    async def get_daily_level(self) -> Tuple[Level, timedelta]:
        """
        Downloads the daily level from the Geometry Dash servers with the time left for it.

        The method returns a tuple of the level object and the time left in timedelta. Like this:
        `(Level(), timedelta)`

        Parameters:
            No parameters are specificied.
        """

        try:
            response = await post(
                url="http://www.boomlings.com/database/getGJDailyLevel.php",
                data={"secret": self.secret}
            )

            response = response.split("|")

            level = await self.download_level(int(response[0]))

            return level, timedelta(seconds=int(response[1]))
        except Exception as e:
            raise RuntimeError(f"Failed to get daily level: {e}")
        
    async def get_weekly_level(self) -> Tuple[Level, timedelta]:
        """
        Downloads the weekly level from the Geometry Dash servers with the time left for it.

        The method returns a tuple of the level object and the time left in timedelta. Like this:
        `(Level(), timedelta)`

        Parameters:
            No parameters are specificied.
        """

        try:
            response = await post(
                url="http://www.boomlings.com/database/getGJDailyLevel.php",
                data={"secret": self.secret, "weekly": 1}
            )

            response = response.split("|")

            level = await self.download_level(int(response[0]))

            return level, timedelta(seconds=int(response[1]))
        except Exception as e:
            raise RuntimeError(f"Failed to get weekly level: {e}")
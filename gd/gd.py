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

        try:
            response = await send_post_request(
                url="http://www.boomlings.com/database/downloadGJLevel22.php", 
                data={"levelID": id, "secret": self.secret}
            )
            return Level(response)
        except Exception as e:
            raise RuntimeError(f"Failed to download level: {e}")

    async def get_daily_level(self, weekly: bool = False, get_time_left: bool = False) -> Level | Tuple[Level, timedelta]:
        """
        Downloads the daily/weekly level from the Geometry Dash servers with the time left for it.

        Parameters:
            weekly (int, optional): Put `True` to get the weekly level, otherwise daily.
            get_time_left (bool, optional): If `True`, the method will also return the time left in timedelta inside a tuple with the `Level` object. Defaults to `False`.
        """

        try:
            level = await self.download_level(-2 if weekly else -1)
            
            if get_time_left:
                daily_data: str = await send_post_request(
                    url="http://www.boomlings.com/database/getGJDailyLevel.php", 
                    data={"secret": self.secret, "weekly": "1" if weekly else "0"}
                )
                daily_data = daily_data.split("|")
                return level, timedelta(seconds=int(daily_data[1]))
            
            return level
        except Exception as e:
            raise RuntimeError(f"Failed to get daily level: {e}")

    async def search_level(self, query: str):
        search_data: str = await send_post_request(
            url="http://www.boomlings.com/database/getGJLevels21.php", 
            data={"secret": self.secret, "str": query, "type": 0}
        )
        
        search_data = parse_search_results(search_data)
        for search in search_data:
            search_data[search_data.index(search)] = SearchedLevel(search)

        return search_data

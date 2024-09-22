import gd._helpers as misc
from .objects import *

_secret = "Wmfd2893gb7"

class GeometryDash:
    def __init__(self, secret: str = "") -> None:
        self.secret = secret

    async def download_level(self, id: int, version: int = 22) -> Level:
        """
        Downloads a specific level from the Geometry Dash servers using the provided ID.

        Parameters:
            id (int): The ID of the level to download (required).
            version (int): The version of the level to download, defaults to 22.

        Raises:
            ValueError: If the ID is not a positive integer or version is less than 10.
        """
        if not isinstance(id, int):
            raise ValueError("ID must be an int.")
        if id <= 0:
            raise ValueError("ID must be greater than 0.")
        if version < 10:
            raise ValueError("Invalid version, the first version is 1.0 (10).")

        try:
            response = await misc.post(
                url="http://www.boomlings.com/database/downloadGJLevel22.php", 
                data={"levelID": id, "secret": self.secret}
            )
            return Level(response)
        except Exception as e:
            raise RuntimeError(f"Failed to download level: {e}")

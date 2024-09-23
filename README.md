# Geometry Dash API Wrapper
An asyncronious API wrapper for **Geometry Dash**.

You can use it like this:
```py
from gd import *

async def download_level():
    geometrydash = gd.GeometryDash("Wmfd2893gb7") # Input the secret in order to use the API.
    level = await geometrydash.download_level(128) # Downloads the level with an ID of 128.

    level.NAME # 1st level
    level.ID # 128
```


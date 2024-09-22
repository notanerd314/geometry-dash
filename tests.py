import gd
from gd.objects import *
import asyncio

async def main():
    geometrydash = gd.GeometryDash("Wmfd2893gb7")
    
    response = await geometrydash.download_level(31280642)
    print(response.DIFFICULTY)
    print(response.STARS)
    print(response.RATING)
    print(response.TWO_PLAYER)

asyncio.run(main())
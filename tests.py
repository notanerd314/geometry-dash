import gd
from gd.objects import *
import asyncio

async def main():
    geometrydash = gd.GeometryDash("Wmfd2893gb7")
    
    response = await geometrydash.get_daily_level()
    print(response.DIFFICULTY)
    print(response.STARS)
    print(response.RATING)
    print(response.DAILY_ID)

asyncio.run(main())
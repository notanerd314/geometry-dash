import gd
from gd.objects import *
import asyncio
from loguru import logger
from json import dumps

@logger.catch
async def main():
    geometrydash = gd.GeometryDash("Wmfd2893gb7")
    
    # response = await geometrydash.get_daily_level(weekly=True, get_time_left=True)
    
    # level = response[0]
    # time_left = response[1]

    # print(time_left)
    # print(level.NAME)
    # print(level.DIFFICULTY)
    # print(level.STARS)
    # print(level.RATING)
    # print(level.DAILY_ID)

    response = await geometrydash.download_level(128)
    print(response.__dict__)

asyncio.run(main())
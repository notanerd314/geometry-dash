import gd.gd as gd
from gd.objects import *
import asyncio

async def main():
    geometrydash = gd.GeometryDash("Wmfd2893gb7")
    
    response = await geometrydash.download_level(128)
    print(response)

asyncio.run(main())
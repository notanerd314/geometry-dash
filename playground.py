from gd import Client
from asyncio import run

async def main():
    client = Client()
    level = await client.download_level(13519)
    print(level.raw_str)

run(main())
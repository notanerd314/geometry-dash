import asyncio
import gd


async def main():
    # Initialize the client
    client = gd.Client()

    # Downloads a level with the given ID
    level: gd.Level = await client.download_level(13519)

    # Prints the level instance
    print(level)


# Runs the async function
asyncio.run(main())

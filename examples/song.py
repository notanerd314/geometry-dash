import asyncio
import gd


async def main():
    # Initialize the client
    client = gd.Client()

    # Gets the song with the ID of 1.
    song = await client.get_song(1)

    # Downloads the song and name it "chilled.mp3" in the relative path.
    await song.download_to("chilled.mp3")


# Run the main function
asyncio.run(main())

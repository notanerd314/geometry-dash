import asyncio
import gd

async def main():
    # Initialize client
    client = gd.Client()

    # Gets the music library
    music_library: gd.MusicLibrary = await client.music_library()

    # Search songs that has the tags specified
    tag_songs: list[gd.MusicLibrary.Song] = music_library.filter_song_by_tags({"pop"})

    # Filter song by artist
    artist_songs: list[gd.MusicLibrary.Song] = music_library.filter_song_by_artist("frums")

    # Search songs by query
    search_songs: list[gd.MusicLibrary.Song] = music_library.search_songs("bussin")

# Run the main function
asyncio.run(main())
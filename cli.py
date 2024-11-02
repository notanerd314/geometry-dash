"""
## `cli.py`

CLI tool for interacting with Geometry Dash. It can be used to download songs, creating icons, etc.

**This is highly unfinished and unstable.**
"""

import click
from gd import *
import asyncio
import colorama

UNDERLINE = "\033[4m"
NOT_UNDERLINE = "\033[0m"

# Initialize colorama for cross-platform support of ANSI colors
colorama.init(autoreset=True)

@click.group("gd")
def main():
    pass

# Get song
async def _get_song(id: int) -> Song:
    client = Client()
    return await client.get_song(id)

@main.command()
@click.argument("id")
def get_song(id: int):
    try:
        song = asyncio.run(_get_song(id))
    except Exception as e:
        match type(e):
            case InvalidSongID:
                print(colorama.Fore.RED + colorama.Style.BRIGHT + "[ERROR]" + colorama.Style.NORMAL + f" Invalid song ID '{id}'.")
                return
    
    # Song details
    print(f"{colorama.Style.BRIGHT}{song.name} by {song.artist_name}{colorama.Style.RESET_ALL}")

    # Line separator
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # Detailed info with colorama colors
    print(f"{colorama.Fore.LIGHTBLUE_EX}ID: {colorama.Style.BRIGHT}{song.id}")
    print(f"{colorama.Fore.LIGHTBLUE_EX}Name: {colorama.Style.BRIGHT}{song.name}")
    
    print(f"{colorama.Fore.LIGHTGREEN_EX}Artist: {colorama.Style.BRIGHT}{song.artist_name}")
    print(f"{colorama.Fore.LIGHTGREEN_EX}Artist ID: {colorama.Style.BRIGHT}{song.artist_id}")
    print(f"{colorama.Fore.LIGHTGREEN_EX}Artist Verified: {colorama.Style.BRIGHT}{song.artist_verified}")

    print(f"{colorama.Fore.LIGHTYELLOW_EX}Size: {colorama.Style.BRIGHT}{song.size} MB")
    
    print(f"{colorama.Fore.LIGHTRED_EX}Youtube URL: {colorama.Style.BRIGHT}{UNDERLINE if song.youtube_link else "" + str(song.youtube_link) + NOT_UNDERLINE}")
    print(f"{colorama.Fore.LIGHTRED_EX}Source: {colorama.Style.BRIGHT}{UNDERLINE + song.link + NOT_UNDERLINE}")
    
    print(f"{colorama.Fore.LIGHTMAGENTA_EX}Is NCS: {colorama.Style.BRIGHT}{song.is_ncs}")
    print(f"{colorama.Fore.LIGHTMAGENTA_EX}Is in Music Library: {colorama.Style.BRIGHT}{song.is_in_library}")

main()
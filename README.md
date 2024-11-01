# `gdapi`

A lightweight and asyncronious API wrapper for **Geometry Dash** and **Pointercrate (soon)**.

```py
>>> from gd import Client
>>> client = Client()
>>> level = await client.download_level(13519)
>>> level.name
"The Nightmare"
>>> level.difficulty
Difficulty.EASY_DEMON
>>> level.description
"Hard map by Jax. 7813"
>>> level.official_song
OfficialSong.POLARGEIST
```

# Installation and Information
### *why the heck did i put that???? it's unfinished!!!!!*
Install GDAPI via PyPI:

```bash
$ python -m pip install gdapi
```
**GDAPI** supports Python version 3.7 or greater officially.

The package requires the following dependencies:
- aiohttp
- aiofiles
- colorama (For useless eye candy)

# Usage
- Fetching a Newgrounds/Music Library song then downloading it:
```py
import gd
import asyncio

async def main():
    client = gd.Client()
    song = await client.get_song(803223)
    print(f"Name: {song.title}, ID: {song.id}, Size: {song.size} MB.")
    # Name: Xtrullor - Arcana, ID: 803223, Size: 8.81 MB.

    await song.download_to("look_i_download_song.mp3")
    # Downloads to the relative path.

asyncio.run(main())
```

- Fetching an user's profile:

```py
import gd
import asyncio

async def main():
    client = gd.Client()
    user = await client.search_user("notanerd1")
    print(f"Name: {user.name}, Account ID: {user.account_id}, Player ID: {user.player_id}, Stars: {user.stars}")
    # Name: notanerd1, Account ID: 24514763, Player ID: 218839712, Stars: 1477
```

- Getting gauntlets:
```py
import gd
import asyncio

async def main():
    client = gd.Client()
    gauntlets = await client.gauntlets()
    print(gauntlets)
    # [Gauntlet(id=1, name='Fire', level_ids=[27732941, 28200611, 27483789, 28225110, 27448202], image_url='https://gdbrowser.com/assets/gauntlets/fire.png'), Gauntlet(id=2, ...

asyncio.run(main())
```





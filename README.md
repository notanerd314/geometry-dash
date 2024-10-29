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
Install GDAPI via PyPI:

```bash
$ python -m pip install gdapi
```
**GDAPI** supports version 3.8 or greater officially.

The package requires the following dependencies:
- aiohttp
- aiofiles

# Usage
For fetching song then downloading it:
```py
import gd
import asyncio

async def main():
    client = gd.Client()
    song = await client.get_song(803223)
    print(f"{song.title}, ")
```



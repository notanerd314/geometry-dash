# `gdapi`

An object-oriented and asyncronious wrapper for **Geometry Dash** and **Pointercrate**.

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
>>> level.raw_str # Original data returned from the servers
"1:13519:2:The Nightmare:3:SGFyZCBtYXAgYnkgSmF4LiA3..."
```

# Installation and Information
Install GDAPI via PyPI:

```bash
$ python -m pip install gdapi
```
**GDAPI** supports version 3.8 or greater officially.

The package requires the following dependencies:
- httpx

*ik there is `gd.py` but who cares lol*




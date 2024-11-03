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
### Downloading a level:
```py
>>> from gd import Client
>>> client = Client()
>>> level = await client.download_level(13519)
>>> level.name
"The Nightmare"
>>> level.difficulty
<DemonDifficulty.EASY_DEMON: 3>
>>> level.description
"Hard map by Jax. 7813"
>>> level.official_song
<OfficialSong.POLARGEIST: 2>
```

### Fetching a song and downloading it:
```py
>>> from gd import Client
>>> client = Client()
>>> song = await client.get_song(1)
>>> song.name
"Chilled 1"
>>> song.size
0.07
>>> song.link
"http://audio.ngfiles.com/0/1_newgrounds_consin.mp3"
>>> await song.download_to("chilled.mp3") # Download the song and name it "chilled.mp3" in the relative path.
```

### Getting the Music Library:
```py
>>> from gd import Client
>>> client = Client()
>>> library = await client.music_library()
>>> library.version
127
>>> library.artists
{10002716: Artist(id=10002716, name='Raul Ojamaa', website=None, youtube_channel_id=None),
 10002717: Artist(id=10002717, name='Malou', website=None, youtube_channel_id=None), ...}
>>> library.tags
{234: '8bit', 251: 'action', 239: 'ambiance', 246: 'ambient', 247: 'battle', 248: 'boss', 250: 'calm', 249: 'casual', ...}
```

### Login and comment:
```py
>>> from gd import Client
>>> client = Client()
>>> credientals = await client.login("notanerd1", "*********") # Password is hidden on purpose
>>> credientals
Account(account_id=24514763, player_id=218839712, name='notanerd1', password=********) # Hidden when printing the instance
>>> comment_id = await client.comment("I am high", level_id=111663149, percentage=0) # Comment on the level with the percentage of 0
2994273
```




# `geometry-dash`

An asynchronous API wrapper for **Geometry Dash**.

![License](https://img.shields.io/github/license/notanerd314/geometry-dash?color=yellow)
![Commits](https://img.shields.io/github/commit-activity/w/notanerd314/geometry-dash?label=commits&logo=github)
![Discord](https://img.shields.io/discord/1292437262155382816?label=discord&logo=discord&color=blue&logoColor=white)

---

## Features

`geometry-dash` currently supports:
- Account login
- Level download and search
- Map packs, gauntlets, and level lists
- Cosmetics
- Leaderboards
- Comments and account posts


<!-- ## Installation

Install `geometry-dash` via PyPI:

```bash
$ python -m pip install geometry-dash
```

**Requirements:** Python 3.7 or greater

**Dependencies:**
- aiohttp
- aiofiles
- attrs

# Usage
- Downloading a Level:

```python
import gd

client = gd.Client()
level = await client.download_level(13519)

print(level.name)          # "The Nightmare"
print(level.difficulty)    # <DemonDifficulty.EASY_DEMON: 3>
print(level.description)   # "Hard map by Jax. 7813"
print(level.official_song) # <OfficialSong.POLARGEIST: 2>
``` -->

- Fetching and Downloading a Song:

```python
import gd

client = gd.Client()
song = await client.get_song(1)

print(song.name)  # "Chilled 1"
print(song.size)  # 0.07
print(song.link)  # "http://audio.ngfiles.com/0/1_newgrounds_consin.mp3"

# Download the song and save it as "chilled.mp3" in the current directory
await song.download_to("chilled.mp3")
```

- Getting the Music Library
```python
import gd

client = gd.Client()
library = await client.music_library()

print(library.version)  # 127
print(library.artists)  # Dictionary of artist IDs to artist details
print(library.tags)     # Dictionary of tag IDs to tag names
```

- Logging in and Commenting
```python
import gd

client = gd.Client()
credentials = await client.login("notanerd1", "*********")  # Replace with your credentials

print(credentials)  # Account(account_id=24514763, player_id=218839712, name='notanerd1', password=********)

# Post a comment on a level with 0% progress
comment_id = await client.comment("I am high", level_id=111663149, percentage=0)
print(comment_id)  # 2994273
```
---

# Changelog

# Notes
- This project is a **work in progress**. Expect some features to change or improve over time.
- Contributions and feedback are welcome!
- Documentation will be available after the module is published.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.


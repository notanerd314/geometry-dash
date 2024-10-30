"""
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
>>> level.raw_str # Original data returned from the servers
"1:13519:2:The Nightmare:3:SGFyZCBtYXAgYnkgSmF4LiA3..."
```

It can't do login functions yet but who fricking cares

# Installation and Information
Install GDAPI via PyPI:

```bash
$ python -m pip install gdapi
```
**GDAPI** supports version 3.8 or greater officially.

The package requires the following dependencies:
- httpx
- aiofiles
"""

__title__ = 'gdapi'
__author__ = 'notanerd'
__license__ = 'GPL-3.0'
__copyright__ = 'Copyright 2024 notanerd'
__version__ = '1.0.0'

from collections import namedtuple

from .gd import *
from .entities import *

VersionInfo = namedtuple('VersionInfo', 'major minor micro')

version_info = VersionInfo(major=1, minor=0, micro=0)
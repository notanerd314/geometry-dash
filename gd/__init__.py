"""
**Geometry Dash API Wrapper**

A wrapper for the Geometry Dash API.

Some features were removed due to raised concerns about hacking.

"""

__title__ = 'geometrydash'
__author__ = 'notanerd'
__license__ = 'GPL-3.0'
__copyright__ = 'Copyright 2021 notanerd'
__version__ = '1.0.0'

from collections import namedtuple

from .gd import *
from .objects import *

VersionInfo = namedtuple('VersionInfo', 'major minor micro')

version_info = VersionInfo(major=1, minor=0, micro=0)
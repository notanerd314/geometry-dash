"""
# Geometry Dash API Wrapper

A wrapper for the Geometry Dash (and Pointercrate also!)

Start using the wrapper by `gd.Client()`
"""

__title__ = 'gdapi'
__author__ = 'notanerd'
__license__ = 'GPL-3.0'
__copyright__ = 'Copyright 2024 notanerd'
__version__ = '1.0.0'

from collections import namedtuple

from .gd import *
from .models import *

VersionInfo = namedtuple('VersionInfo', 'major minor micro')

version_info = VersionInfo(major=1, minor=0, micro=0)
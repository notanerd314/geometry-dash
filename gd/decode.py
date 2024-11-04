"""
# .helpers

A module containing all helper functions for the module.

You typically don't want to use this module because it has limited documentation and confusing to use.
"""

import aiohttp
import base64
import zlib
import uuid
from typing import List, Dict, Union
from hashlib import sha1
from enum import StrEnum
from .exceptions import *

# Constants
XOR_KEY = "26364"
START_ID_SONG_LIB = 10000000
BASE64_PADDING_CHAR = "="
AW_CODE = "Aw=="
DEFAULT_TIMEOUT = 60
UDID_PREFIX = "S"


# * HTTP Helper Functions
async def handle_response(response: aiohttp.ClientResponse) -> aiohttp.ClientResponse:
    response.raise_for_status()
    return response


async def send_post_request(**kwargs) -> str:
    async with aiohttp.ClientSession() as client:
        async with client.post(**kwargs, headers={"User-Agent": ""}) as response:
            response_text = await handle_response(response)
            return await response_text.text()


async def send_get_request(decode: bool = True, **kwargs) -> bytes:
    """Send a GET request and reads the response."""
    client = aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(60.0)
    )  # Create session

    response = await client.get(**kwargs)  # Make the GET request
    handled_response = await handle_response(response)  # Handle the response
    response_data = await handled_response.read()

    await client.close()  # Close the session

    if decode:
        return response_data.decode()
    else:
        return response_data


# * Encryption and Decryption Functions


class XorKey(StrEnum):
    LEVEL_PASSWORD = "26364"
    GJP = "37526"
    COMMENT = "29481"


class CHKSalt(StrEnum):
    LEVEL = "xI25fpAapCQg"
    COMMENT = "0xPT6iUrtws0J"
    LIKE = "ysg6pUrtjn0J"
    RATE = "ysg6pUrtjn0J"
    PROFILE = "xI35fsAapCRg"
    LEADERBOARD = "yPg6pUrtWn0J"


def uuid4() -> str:
    return str(uuid.uuid4())


def add_padding(data: str) -> str:
    """Add padding to base64-encoded data to make its length a multiple of 4."""
    return data + "=" * ((4 - len(data) % 4) % 4)


def xor(input_bytes: bytes, key: str) -> str:
    key_bytes = key.encode()
    return "".join(
        chr(byte ^ key_bytes[i % len(key_bytes)]) for i, byte in enumerate(input_bytes)
    )


def decrypt_data(
    encrypted: Union[str, bytes], decrypt_type: str = "base64", xor_key: str = None
) -> Union[str, None]:
    if not encrypted:
        return None

    if decrypt_type == "base64_decompress":
        decoded_data = base64.urlsafe_b64decode(add_padding(encrypted))
        return zlib.decompress(decoded_data, 15 | 32).decode()
    elif decrypt_type == "xor":
        return xor(base64.b64decode(encrypted), xor_key)
    elif decrypt_type == "base64":
        return base64.urlsafe_b64decode(add_padding(encrypted)).decode()
    else:
        raise ValueError("Invalid decrypt type!")


def generate_chk(
    values: List[Union[int, str]] = [], key: str = "", salt: str = ""
) -> str:
    values.append(salt)
    combined_str = "".join(map(str, values))
    hashed = sha1(combined_str.encode()).hexdigest()
    xored = xor(hashed.encode(), key)
    return base64.urlsafe_b64encode(xored.encode()).decode()

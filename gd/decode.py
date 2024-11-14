__doc__ = """
# gd.decode

A module containing functions related to decoding/encoding

This module has limited documentation and is not intended to be used directly.
"""

import base64
import zlib
from typing import List, Union
from hashlib import sha1
from enum import StrEnum

# Constants
XOR_KEY = "26364"
START_ID_SONG_LIB = 10000000
BASE64_PADDING_CHAR = "="
AW_CODE = "Aw=="
DEFAULT_TIMEOUT = 60
UDID_PREFIX = "S"

__all__ = [
    "XorKey",
    "CHKSalt",
    "cyclic_xor",
    "xor_singular",
    "base64_urlsafe_decode",
    "base64_decompress",
    "generate_chk",
]

# * Encryption and Decryption Functions


class XorKey(StrEnum):
    """
    An enum class for XOR keys, typically used for decryption/encryption.
    """

    LEVEL_PASSWORD = "26364"
    GJP = "37526"
    COMMENT = "29481"


class CHKSalt(StrEnum):
    """
    An enum class for salting, typically used for encryption.
    """

    LEVEL = "xI25fpAapCQg"
    COMMENT = "0xPT6iUrtws0J"
    LIKE = "ysg6pUrtjn0J"
    RATE = "ysg6pUrtjn0J"
    PROFILE = "xI35fsAapCRg"
    LEADERBOARD = "yPg6pUrtWn0J"


def add_padding(data: str) -> str:
    """
    Add padding to base64-encoded data to make its length a multiple of 4.

    :param data: The base64-encoded data to add padding to.
    :type data: str
    :return: The base64-encoded data with padding added.
    :rtype: str
    """
    return data + "=" * ((4 - len(data) % 4) % 4)


def cyclic_xor(input_bytes: bytes, key: str) -> str:
    """
    Cyclic XOR encrypt/decrypt

    :param input_bytes: The bytes to XOR encrypt/decrypt.
    :type input_bytes: bytes
    :param key: The XOR key to use.
    :type key: str

    :return: The XOR-encrypted/decrypted data as a string.
    :rtype: str
    """
    key_bytes = key.encode()
    return "".join(
        chr(byte ^ key_bytes[i % len(key_bytes)]) for i, byte in enumerate(input_bytes)
    )


def xor_singular(input_bytes: bytes, key: str) -> str:
    """
    Singular XOR encrypt/decrypt

    :param input_bytes: The bytes to XOR encrypt/decrypt.
    :type input_bytes: bytes
    :param key: The XOR key to use (single byte).
    :type key: str

    :return: The XOR-encrypted/decrypted data as a string.
    :rtype: str
    """
    key_byte = ord(
        key[0]
    )  # Get the first byte of the key (key should be a single character)
    return "".join(chr(byte ^ key_byte) for byte in input_bytes)


def base64_urlsafe_decode(encrypted: str) -> str:
    """
    Decode base64-encoded data with padding and URL-safe encoding.

    :param encrypted: The base64-encoded data to decode.
    :type encrypted: str
    :return: The decoded base64-encoded data.
    :rtype: str
    """
    return base64.urlsafe_b64decode(add_padding(encrypted)).decode()


def base64_decompress(encrypted: str) -> str:
    """
    Decode a base64 encoded string then decompress it with zlib.

    :param encrypted: The base64-encoded string to decompress.
    :type encrypted: str
    :return: The decompressed data as a string.
    :rtype: str
    """
    decoded_data = base64.urlsafe_b64decode(add_padding(encrypted))
    return zlib.decompress(decoded_data, 15 | 32).decode()


def generate_chk(values: List[Union[int, str]], key: str = "", salt: str = "") -> str:
    """
    Generates chk data.

    :param values: The values to include in the chk data.
    :type values: List[Union[int, str]]
    :param key: The XOR key to use.
    :type key: str
    :param salt: The salt to use for encryption.
    :type salt: str
    :return: The generated chk data as a string.
    :rtype: str
    """

    values.append(salt)
    combined_str = "".join(map(str, values))

    hashed = sha1(combined_str.encode()).hexdigest()
    xored = cyclic_xor(hashed.encode(), key)

    return base64.urlsafe_b64encode(xored.encode()).decode()

__doc__ = """
# gd.decode

A module containing functions related to decoding/encoding

This module has limited documentation and is not intended to be used directly.
"""

import base64
import zlib
import uuid
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


def uuid4() -> str:
    """
    Generate a random UUID.

    :return: A random UUID as a string.
    :rtype: str
    """
    return str(uuid.uuid4())


def add_padding(data: str) -> str:
    """
    Add padding to base64-encoded data to make its length a multiple of 4.

    :param data: The base64-encoded data to add padding to.
    :type data: str
    :return: The base64-encoded data with padding added.
    :rtype: str
    """
    return data + "=" * ((4 - len(data) % 4) % 4)


def xor(input_bytes: bytes, key: str) -> str:
    """
    XOR encrypt/decrypt

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


def decrypt_data(
    encrypted: Union[str, bytes], decrypt_type: str = "base64", xor_key: str = None
) -> Union[str, None]:
    """
    **THIS FUNCTION WILL BE REVOKED**

    Decrypt data based on the specified decrypt type.

    :param encrypted: The encrypted data to decrypt.
    :type encrypted: Union[str, bytes]
    :param decrypt_type: The type of decryption to use.
    :type decrypt_type: str
    :param xor_key: The XOR key to use for XOR decryption.
    :type xor_key: str
    :return: The decrypted data as a string or None if the decryption failed.
    :rtype: Union[str, None]
    """
    if not encrypted:
        return None

    if decrypt_type == "base64_decompress":
        decoded_data = base64.urlsafe_b64decode(add_padding(encrypted))
        return zlib.decompress(decoded_data, 15 | 32).decode()

    if decrypt_type == "xor":
        return xor(base64.b64decode(encrypted), xor_key)

    if decrypt_type == "base64":
        return base64.urlsafe_b64decode(add_padding(encrypted)).decode()

    raise ValueError("Invalid decrypt type!")


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
    xored = xor(hashed.encode(), key)

    return base64.urlsafe_b64encode(xored.encode()).decode()

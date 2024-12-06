__doc__ = """
# gd.decode

A module containing functions related to decoding/encoding

This module has limited documentation and is not intended to be used directly.
"""

import base64
import zlib
import random
from string import ascii_letters, digits
from hashlib import sha1
from enum import StrEnum

from gd.type_hints import Udid

# Constants
XOR_KEY = "26364"
BASE64_PADDING_CHAR = "="
AW_CODE = "Aw=="
LETTERS = ascii_letters + digits

__all__ = [
    "XorKey",
    "Salt",
    "cyclic_xor",
    "singular_xor",
    "base64_urlsafe_decode",
    "base64_decompress",
    "generate_chk",
    "gjp2",
    "generate_udid",
]

# * Encryption and Decryption Functions


class XorKey(StrEnum):
    """
    An enum class for XOR keys, typically used for decryption/encryption.
    """

    LEVEL_PASSWORD = "26364"
    GJP = "37526"
    COMMENT = "29481"
    LIKE = "58281"
    QUEST = "19847"
    CHEST = "59182"


class Salt(StrEnum):
    """
    An enum class for salts, typically used for encryption.
    """

    LEVEL = "xI25fpAapCQg"
    COMMENT = "0xPT6iUrtws0J"
    LIKE = "ysg6pUrtjn0J"
    RATE = "ysg6pUrtjn0J"
    PROFILE = "xI35fsAapCRg"
    LEADERBOARD = "yPg6pUrtWn0J"
    PASSWORD = "mI29fmAnxgTs"


def gjp2(password: str = "", salt: str = Salt.PASSWORD) -> str:
    """
    Convert a password to a GJP2 encrypted password.

    :param password: The password to be encrypted.
    :type password: str
    :param salt: The salt to use for encryption.
    :type salt: str
    :return: An encrypted password.
    """
    password += salt
    result = sha1(password.encode()).hexdigest()

    return result


def generate_udid(start: int = 100_000, end: int = 100_000_000) -> Udid:
    """
    Generate a Universally Unique Identifier for device.

    :param start: The starting number for the UDID.
    :type start: int
    :param end: The ending number for the UDID.
    :type end: int
    :return: A random UDID as a string.
    :rtype: str
    """
    value = [str(random.randint(start, end)) for _ in range(4)]
    return "S15" + "".join(value)


def add_padding(data: str) -> str:
    """
    Add padding to base64-encoded data to make its length a multiple of 4.

    :param data: The base64-encoded data to add padding to.
    :type data: str
    :return: The base64-encoded data with padding added.
    :rtype: str
    """
    return data + BASE64_PADDING_CHAR * ((4 - len(data) % 4) % 4)


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


def singular_xor(input_bytes: bytes, key: str) -> str:
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


def robtop_cipher(value: str, key: int = 37526) -> str:
    """
    I'm too lazy to document this piece of crap.

    :param value: The string to be encrypted.
    :param key: The encryption key (an integer).

    :return: The encrypted string in URL-safe base64 format.
    """
    # Convert the key to a string for cyclic XOR use
    key_str = str(key)
    key_len = len(key_str)

    # Perform XOR on each character in the value using the key
    xored_str = "".join(
        chr(ord(char) ^ ord(key_str[i % key_len])) for i, char in enumerate(value)
    )

    # Convert the XORed string to bytes
    xored_bytes = xored_str.encode("utf-8")

    # Encode the XORed bytes to base64
    base64_encoded = base64.b64encode(xored_bytes).decode("utf-8")

    # Replace '/' with '_' and '+' with '-'
    encrypted_string = base64_encoded.replace("/", "_").replace("+", "-")

    return encrypted_string


def base64_urlsafe_decode(encrypted: str) -> str:
    """
    Decode base64-encoded data with padding and URL-safe encoding.

    :param encrypted: The base64-encoded data to decode.
    :type encrypted: str
    :return: The decoded base64-encoded data.
    :rtype: str
    """
    return base64.urlsafe_b64decode(add_padding(encrypted))


def base64_encode(value: str) -> str:
    """
    Encode a value as a base64-encoded string.
    :param value: The value to encode.
    :type value: str
    :return: The base64-encoded value.
    :rtype: str
    """
    return base64.urlsafe_b64encode(value.encode()).decode()


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


def generate_rs(n: int = 10) -> str:
    """
    Generates a random seed.

    :param n: The length of the random seed.
    :type n: int
    :return: A random seed as a string.
    :rtype: str
    """
    return ("").join(random.choices(LETTERS, k=n))


def generate_digits() -> str:
    """
    Generates a random string base64-encoded and a random number XORed then combine it.

    :return: The generated string.
    :rtype: str
    """
    # Generate a 5-character random string
    random_string = generate_rs(n=5)

    # Generate a random number and encrypt it using XOR cipher
    random_number = str(random.randint(10000, 1000000))
    encrypted_number = cyclic_xor(random_number.encode(), "59182")

    # Base64 encode the encrypted number
    base64_encoded = base64.b64encode(encrypted_number.encode()).decode()

    # Concatenate the random string and the encoded number
    result = f"{random_string}{base64_encoded}"
    return result


def generate_chk(values: list[any], key: XorKey = "", salt: Salt = "") -> str:
    """
    Generates CHK data.

    :param values: The values to include in the CHK data.
    :type values: list[any]
    :param key: The XOR key to use.
    :type key: str
    :param salt: The salt to use for encryption.
    :type salt: str
    :return: The generated chk data as a string.
    :rtype: str
    """

    values.append(salt)
    combined_str = "".join(map(str, values))

    hashed = gjp2(combined_str, "")
    xored = cyclic_xor(hashed.encode(), key)

    return base64.urlsafe_b64encode(xored.encode()).decode()

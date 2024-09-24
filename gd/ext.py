import httpx
import json
import base64
import zlib
from typing import *

# Exceptions:

class ResponseError(Exception):
    pass

class InvalidSecret(Exception):
    pass

# Helpers:

async def post(**kwargs) -> str:
    """Send an asynchronous POST request."""
    async with httpx.AsyncClient() as client:
        response = await client.post(**kwargs, headers={"User-Agent": ""})
        if response.status_code == 200:
            if response.text == "-1":
                raise InvalidSecret('Invalid secret! Hint: The secret is Wmfd2893gb7.')
            return response.text
        else:
            raise ResponseError(f"Unable to fetch data, got {response.status_code}.")

# Parsing responses:

def add_padding(data: str):
    """Add padding to the input data to make its length a multiple of 4."""
    return data + "=" * (-len(data) % 4)

def decrypt_xor(input_bytes: bytes, key: str) -> str:
    """Encrypt or decrypt the input bytes using XOR with the provided key."""
    key_bytes = key.encode()  # Convert the key to bytes
    result = bytearray()

    for i in range(len(input_bytes)):
        byte = input_bytes[i]
        xKey = key_bytes[i % len(key_bytes)]
        result.append(byte ^ xKey)  # XOR and store the result

    return result.decode('utf-8', errors='ignore')  # Convert back to a readable string

def decrypt(encrypted: str | bytes, decrypt_type: str = "base64"):
    """Decrypt the input data using the provided decrypt type."""
    if decrypt_type == "base64_decompress":
        data = add_padding(encrypted)
        
        decoded = base64.urlsafe_b64decode(data)
        decompressed = zlib.decompress(decoded, 15 | 32)
        decrypted = decompressed.decode()
    elif decrypt_type == "xor":
        decoded_bytes = base64.b64decode(encrypted)
        decrypted = decrypt_xor(decoded_bytes, '26364')
    elif decrypt_type == "base64":
        data = add_padding(encrypted)

        decoded = base64.b64decode(data)
        decrypted = decoded.decode('utf-8')
    else:
        raise ValueError("Invalid decrypt type!")
    
    return decrypted

def parse_level(text: str) -> dict:
    """Parse the input text and extract key-value pairs."""
    text_splitted = text.split(':')
    parsed = {}

    for index in range(0, len(text_splitted), 2):
        key = text_splitted[index]
        value = text_splitted[index + 1] if index + 1 < len(text_splitted) else None

        # Convert numeric values to int if possible
        if value is not None:
            try:
                value = int(value)
            except ValueError:
                pass

        parsed[key] = value

    parsed['4'] = decrypt(parsed['4'], 'base64_decompress')
    parsed['3'] = decrypt(parsed['3'])

    if parsed['27'] == "0":
        parsed['27'] = False
    elif parsed['27'] == "Aw==":
        parsed['27'] = True
    else:
        parsed['27'] = decrypt(parsed['27'])

    return parsed

def parse_user(text: str):
    """Parse the input text and extract key-value pairs."""
    text_splitted = text.split(':')
    parsed = {}

    for index in range(0, len(text_splitted), 2):
        key = text_splitted[index]
        value = text_splitted[index + 1] if index + 1 < len(text_splitted) else None

        # Convert numeric values to int if possible
        if value is not None:
            try:
                value = int(value)
            except ValueError:
                pass

        parsed[key] = value
    
    return parsed

def parse_comments(text: str):
    """Parse the input text and extract key-value pairs."""
    text_splitted = text.split('|')

    for index_comments in range(0, len(text_splitted), 1):
        text_splitted[index_comments] = text_splitted[index_comments].split('~')

    parsed = []

    for item in text_splitted:
        parsed_item = {}
        for index in range(0, len(text_splitted), 2):
            key = text_splitted[index]
            value = item[index + 1] if index + 1 < len(item) else None

            # Convert numeric values to int if possible
            if value is not None and key != "2":
                try:
                    value = int(value)
                except ValueError:
                    pass

            parsed_item[key] = value
    
        parsed_item['2'] = decrypt(parsed_item['2'])
        parsed.append(parsed_item)
    
    return parsed
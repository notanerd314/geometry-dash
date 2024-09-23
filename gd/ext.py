import httpx
import json
import base64
import zlib

# Exceptions:

class ResponseError(Exception):
    pass

class InvalidSecret(Exception):
    pass

# Helpers:

async def post(**kwargs):
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

def xor_encrypt_decrypt(input_bytes: bytes, key: str) -> str:
    """Encrypt or decrypt the input bytes using XOR with the provided key."""
    key_bytes = key.encode()  # Convert the key to bytes
    result = bytearray()

    for i in range(len(input_bytes)):
        byte = input_bytes[i]
        xKey = key_bytes[i % len(key_bytes)]
        result.append(byte ^ xKey)  # XOR and store the result

    return result.decode('utf-8', errors='ignore')  # Convert back to a readable string

def decrypt(parsed: dict):
    """Decrypt the parsed data if necessary."""
    if '4' in parsed:
        leveldata = add_padding(parsed['4'])
        leveldata_decoded = base64.urlsafe_b64decode(leveldata)
        decompressed_leveldata = zlib.decompress(leveldata_decoded, 15 | 32)
        decrypt_leveldata = decompressed_leveldata.decode()
        parsed['4'] = decrypt_leveldata

    if '3' in parsed:
        leveldesc = add_padding(parsed['3'])

        leveldesc_decoded = base64.b64decode(leveldesc)
        leveldesc_string = leveldesc_decoded.decode('utf-8')

        parsed['3'] = leveldesc_string

    # XOR decrypt the password if present
    if '27' in parsed:
        if parsed['27'][0] == "0":
            parsed['27'] = False
            return
        elif parsed['27'] == "Aw==":
            parsed['27'] = True
            return

        password = parsed['27']

        base64_part = add_padding(password.split('#')[0])  # Get the first part before '#'

        # Decode the base64 string
        decoded_bytes = base64.b64decode(base64_part)

        # Decrypt using XOR
        decrypted_password = xor_encrypt_decrypt(decoded_bytes, '26364')

        parsed['27'] = int(decrypted_password)

def parse(text: str) -> dict:
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

    decrypt(parsed)

    return parsed
import httpx
import json
import base64
import zlib

class ResponseError(Exception):
    pass

class InvalidSecret(Exception):
    pass

def xor_encrypt_decrypt(input_bytes: bytes, key: str) -> str:
    key_bytes = key.encode()  # Convert the key to bytes
    result = bytearray()

    for i in range(len(input_bytes)):
        byte = input_bytes[i]
        xKey = key_bytes[i % len(key_bytes)]
        result.append(byte ^ xKey)  # XOR and store the result

    return result.decode('utf-8', errors='ignore')  # Convert back to a readable string


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

    # Decode and decrypt level data if present
    if '4' in parsed:
        leveldata = parsed['4']
        leveldata_decoded = base64.urlsafe_b64decode(leveldata)
        decompressed_leveldata = zlib.decompress(leveldata_decoded, 15 | 32)
        decrypt_leveldata = decompressed_leveldata.decode()
        parsed['4'] = decrypt_leveldata

    # XOR decrypt the password if present
    if '27' in parsed:
        password = parsed['27']
        print(f"Original Password: {password}")

        base64_part = password.split('#')[0]  # Get the first part before '#'

        # Decode the base64 string
        decoded_bytes = base64.b64decode(base64_part)

        # Decrypt using XOR
        decrypted_password = xor_encrypt_decrypt(decoded_bytes, '26364')
        decrypted_password = decrypted_password[1:]

        parsed['27'] = int(decrypted_password)

    return parsed

# Example usage with the provided response text
response_text = (
    "1:6508283:2:ReTraY:3:VGhhbmtzIGZvciBwbGF5aW5nIEdlb21ldHJ5IERhc2g=:"
    "5:3:6:4993756:8:10:9:10:10:39431612:12:0:13:21:14:4125578:17::43:3:"
    "25::18:2:19:7730:42:0:45:20000:15:3:30:0:31:0:28:5 years:29:1 year:"
    "35:557117:36:0_733_0_0_0_0_574_716_0_0_352_78_729_0_42_0_833_68_0_347_0_38_240_205_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0:"
    "37:3:38:1:39:2:46:7729:47:13773:40:0:27:AwMABAYDBw==#eb541c03f8355c0709f8007a1d9a595ae5bedc5d#291568b26b08d70a198fca10a87c736a2823be0c"
)
print(parse(response_text))

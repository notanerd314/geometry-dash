import httpx
import json
import base64
import zlib
from typing import List, Dict, Union

# Custom Exceptions
class ResponseError(Exception):
    pass

# Helper function to send an asynchronous POST request
async def send_post_request(**kwargs) -> str:
    """Send an asynchronous POST request and handle response."""
    async with httpx.AsyncClient() as client:
        response = await client.post(**kwargs, headers={"User-Agent": ""})
        if response.status_code == 200:
            if response.text == "-1":
                raise ResponseError("The request has failed and returned a stupid '-1'!")
            return response.text
        else:
            raise ResponseError(f"Unable to fetch data, got {response.status_code}.")

async def send_get_request(**kwargs) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.get(**kwargs)
        if response.status_code == 200:
            return response
        else:
            raise ResponseError(f"Unable to fetch data, got {response.status_code}")

# Function to add padding to base64 encoded data
def add_padding(data: str) -> str:
    """Add padding to the input data to make its length a multiple of 4."""
    return data + "=" * (-len(data) % 4)

# XOR decryption function
def xor_decrypt(input_bytes: bytes, key: str) -> str:
    """Decrypt the input bytes using XOR with the provided key."""
    key_bytes = key.encode()
    return ''.join(chr(byte ^ key_bytes[i % len(key_bytes)]) for i, byte in enumerate(input_bytes))

# Decrypt function with multiple methods
def decrypt_data(encrypted: Union[str, bytes], decrypt_type: str = "base64") -> str:
    """Decrypt the input data using the specified decrypt type."""
    if decrypt_type == "base64_decompress":
        # padded_data = add_padding(encrypted)
        decoded_data = base64.urlsafe_b64decode(encrypted)
        decompressed_data = zlib.decompress(decoded_data, 15 | 32)
        return decompressed_data.decode()
    elif decrypt_type == "xor":
        decoded_bytes = base64.b64decode(encrypted)
        return xor_decrypt(decoded_bytes, '26364')
    elif decrypt_type == "base64":
        padded_data = add_padding(encrypted)
        return base64.b64decode(padded_data).decode('utf-8')
    else:
        raise ValueError("Invalid decrypt type!")

# Function to parse key-value pairs from a string
def parse_key_value_pairs(text: str, separator: str = ":") -> Dict[str, Union[str, int]]:
    """Parse key-value pairs from a colon-separated string."""
    pairs = {}
    text = text.split("#")[0]
    items = text.split(separator)
    for index in range(0, len(items), 2):
        key = items[index]
        value = items[index + 1] if index + 1 < len(items) else None
        if value is not None:
            try:
                value = int(value)
            except ValueError:
                pass
        pairs[key] = value
    return pairs

# Function to parse level data
def parse_level_data(text: str) -> Dict[str, Union[str, int]]:
    """Parse level data from text."""
    parsed = parse_key_value_pairs(text)
    parsed['4'] = decrypt_data(parsed['4'], 'base64_decompress') if '4' in parsed else None
    parsed['3'] = decrypt_data(parsed['3'])
    
    # Handle special case for '27'
    if '27' not in parsed:
        parsed['27'] = None
    elif parsed['27'] == "0":
        parsed['27'] = False
    elif parsed['27'] == "Aw==":
        parsed['27'] = True
    else:
        parsed['27'] = decrypt_data(parsed['27'])
    
    return parsed

# Function to parse user data
def parse_user_data(text: str) -> Dict[str, Union[str, int]]:
    """Parse user data from text."""
    return parse_key_value_pairs(text)

# Function to parse comments from text
def parse_comments_data(text: str) -> List[Dict[str, Union[str, int]]]:
    """Parse comments from text."""
    items = text.split('|')
    parsed_comments = []
    
    for item in items:
        comment = parse_key_value_pairs(item)
        comment['2'] = decrypt_data(comment['2']) if '2' in comment else None
        parsed_comments.append(comment)
    
    return parsed_comments

# Function to parse song data
def parse_song_data(song: str) -> Dict[str, Union[str, int]]:
    """Parse song data from text."""
    song = song.replace("~", "")
    return parse_key_value_pairs(song, '|')

# Function to parse search results
def parse_search_results(text: str) -> List[Dict[str, Union[Dict, str]]]:
    """Parse search results from input text."""
    parts_splitted = text.split('#')
    levels_data = parts_splitted[0].split("|")
    creators_data = parts_splitted[1].split("|")
    songs_data = parts_splitted[2].split(":")
    
    parsed_levels = [{"level": level} for level in levels_data]

    # Create a set of player IDs from the creators list for quick lookup
    creator_ids = {creator.split(":")[0] for creator in creators_data}

    for index, creator in enumerate(creators_data):
        creator_info = creator.split(":")
        parsed_levels[index]['creator'] = {
            "playerID": creator_info[0],
            "playerName": creator_info[1]
        }

    for current_level in parsed_levels:
        level_data = parse_level_data(current_level['level'])
        
        # Get the user ID from the current level
        user_id = level_data.get('6')

        # Check if the user ID exists in the creator_ids set
        if user_id in creator_ids:
            # If valid creator, assign player details
            current_level['creator'] = {
                "playerID": user_id,
                "playerName": creator_info[1]  # Assuming creator name is fetched appropriately
            }
        else:
            # Create a fake creator with None values
            current_level['creator'] = {
                "playerID": user_id,
                "playerName": None
            }

    for song in songs_data:
        parsed_song = parse_song_data(song)

        for current_level in parsed_levels:
            level_data = parse_level_data(current_level['level'])
            if level_data['35'] == int(parsed_song.get("1", -1)):
                current_level['song'] = song

    return parsed_levels

def is_newgrounds_song(id: int) -> bool:
    return not id >= 10000000
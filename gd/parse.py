"""
# `gd.parse`

Helper script for parsing various responses.
"""

from typing import List, Dict, Union, Any
from .entities.enums import Difficulty, DemonDifficulty
from .decode import *
import ast


def parse_key_value_pairs(
    text: str, separator: str = ":"
) -> Dict[str, Union[str, int, None]]:
    """
    Parse key-value pairs from a separator-separated string. Example:
    ```plain
    1:25:2:65:3:okay
    ```
    The first column of the string is the key name, then the next column is the previous key's value then it repeats like a pattern.

    :param text: The string to parse.
    :type text: str
    :param separator: The separator to parse the string (Default is `:`)
    :type separator: str
    :return: A dictionary containing the parsed key-value pairs.
    :rtype: Dict[str, Union[str, int, None]]
    """
    pairs = {}
    # Parse key-valye pairs
    for index in range(0, len(items := text.split(separator)), 2):
        key, value = items[index], items[index + 1] if index + 1 < len(items) else None

        # Automatically convert str to int if applicable
        pairs[key] = int(value) if value and value.isdigit() else value

    return pairs


def unparse_key_value_pairs(
    parsed: Dict[str, Union[str, int]], separator: str = ":"
) -> str:
    """
    Unparse key-value pairs into a separator-separated string.

    :param parsed: The dictionary containing the parsed key-value pairs.
    :type parsed: Dict[str, Union[str, int]]
    :param separator: The separator to unparse the string.
    :type separator: str
    :return: A string containing the unparsed key-value pairs.
    :rtype: str
    """

    # Unparse the parsed
    return separator.join(f"{key}{separator}{value}" for key, value in parsed.items())


def parse_level_data(text: str) -> Dict[str, Union[str, int]]:
    """
    Parse level data from a string.

    :param text: The string containing level data.
    :type text: str
    :return: A dictionary containing parsed level data.
    :rtype: Dict[str, Union[str, int]]
    """
    # Parsing the data
    parsed = parse_key_value_pairs(text)

    # Decrypt specific values
    parsed["4"] = decrypt_data(parsed.get("4"), "base64_decompress")
    parsed["3"] = decrypt_data(parsed.get("3"))
    parsed["27"] = (
        decrypt_data(parsed.get("27")) if parsed.get("27") not in [None, "0"] else None
    )

    return parsed


def parse_search_results(text: str) -> List[Dict[str, Union[Dict, str]]]:
    """
    Parse search results from a response string.

    :param text: The string containing search results.
    :type text: str
    :return: A list of dictionaries containing parsed level, creator, and song data.
    :rtype: List[Dict[str, Union[Dict, str]]]
    """
    # Split the text into individual level data, creator data, and song data.
    levels_data, creators_data, songs_data = (
        text.split("#")[0].split("|"),
        text.split("#")[1].split("|"),
        text.split("#")[2].split("~:~"),
    )

    # Parse each level data, creator data, and song data separately and add them to the parsed_levels list.
    parsed_levels = [{"level": parse_level_data(level)} for level in levels_data]

    # Match each level's creator data
    for current_level in parsed_levels:
        level_data = current_level["level"]
        user_id = str(level_data.get("6"))  # User ID from level data
        creator_info = next(
            (
                creator.split(":")
                for creator in creators_data
                if creator.startswith(user_id)
            ),
            None,
        )

        # Add creator information if available
        current_level["creator"] = {
            "playerID": creator_info[0] if creator_info else None,
            "playerName": creator_info[1] if creator_info else None,
            "accountID": int(creator_info[2]) if creator_info else None,
        }

    # Match each level's song data
    for song in songs_data:
        parsed_song = parse_song_data(song)

        # Connect the song to the correct level
        for current_level in parsed_levels:
            level_data = current_level["level"]
            if level_data.get("35") == 0:
                current_level["song"] = None
            elif level_data.get("35") == int(parsed_song.get("1", -1)):
                current_level["song"] = parsed_song

    return parsed_levels


def parse_user_data(text: str) -> Dict[str, Union[str, int]]:
    """
    Parse user data from a string.

    :param text: The string containing user data.
    :type text: str
    :return: A dictionary containing parsed user data.
    :rtype: Dict[str, Union[str, int]]
    """
    # Literally parse_key_value_pairs lol
    return parse_key_value_pairs(text)


def parse_comments_data(text: str) -> List[Dict[str, Union[str, int]]]:
    """
    Parse comments data from a string.

    :param text: The string containing comments data.
    :type text: str
    :return: A list of dictionaries containing parsed comments.
    :rtype: List[Dict[str, Union[str, int]]]
    """
    # Parsing multiple comments, not 1 comment.
    items = text.split("|")
    return [{"comment": parse_key_value_pairs(item)} for item in items]


def parse_song_data(song: str) -> Dict[str, Union[str, int]]:
    """
    Parse song data from a string.

    :param song: The string containing song data.
    :type song: str
    :return: A dictionary containing parsed song data.
    :rtype: Dict[str, Union[str, int]]
    """
    # Literally parse_key_value_pairs again lol
    return parse_key_value_pairs(song.replace("~", ""), "|")


def parse_str_literal(text: str) -> Any:
    """
    Parse a string into a literal.

    :param text: The string to convert to a literal.
    :type text: str
    :return: A literal converted from a string.
    :rtype: Any
    """
    return ast.literal_eval(text)


def dict_syntax_to_tuple(text: str) -> str:
    """
    Converts dict syntax to tuple syntax.

    :param text: The string to convert syntax.
    :type text: str
    :return: The result when sucessfully converted `{}` to `()`
    :rtype: str
    """
    return text.replace("{", "(").replace("}", ")")


# Difficulty Determination
_DIFFICULTY_ = {
    -1: Difficulty.NA,
    0: Difficulty.AUTO,
    1: Difficulty.EASY,
    2: Difficulty.NORMAL,
    3: Difficulty.HARD,
    4: Difficulty.HARDER,
    5: Difficulty.INSANE,
    6: DemonDifficulty.EASY_DEMON,
    7: DemonDifficulty.MEDIUM_DEMON,
    8: DemonDifficulty.HARD_DEMON,
    9: DemonDifficulty.INSANE_DEMON,
    10: DemonDifficulty.EXTREME_DEMON,
}
"""Difficulty mapping but kinda useless don't you think?"""


def determine_difficulty(
    parsed: dict, return_demon_diff: bool = True
) -> Union[Difficulty, DemonDifficulty]:
    """
    Determine the difficulty of a level based on parsed data.

    :param parsed: Parsed data from the server.
    :type parsed: dict
    :param return_demon_diff: Whether to return specific demon difficulty (if applicable).
    :type return_demon_diff: bool
    :return: Difficulty level or specific demon difficulty.
    :rtype: Union[:class:`gd.entities.enums.Difficulty`, :class:`gd.entities.enums.DemonDifficulty`]
    :raises ValueError: If the demon difficulty is invalid.
    """
    if return_demon_diff and parsed.get("17", False):
        # If it's a demon
        match parsed.get("43"):
            case 3:
                return DemonDifficulty.EASY_DEMON
            case 4:
                return DemonDifficulty.MEDIUM_DEMON
            case 0:
                return DemonDifficulty.HARD_DEMON
            case 5:
                return DemonDifficulty.INSANE_DEMON
            case 6:
                return DemonDifficulty.EXTREME_DEMON
            case _:
                raise ValueError(f"Invalid DemonDifficulty: {parsed.get('43')}")
    elif parsed.get("25"):
        # Return AUTO if auto
        return Difficulty.AUTO
    else:
        # If not, return the normal difficulties
        return Difficulty(parsed.get("9", 0) // 10)


def determine_search_difficulty(difficulty_obj: Difficulty) -> int:
    """
    Converts a Difficulty object to its corresponding integer value for search purposes.

    :param difficulty_obj: The difficulty object.
    :type difficulty_obj: :class:`gd.entities.enums.Difficulty`
    :return: Integer representing the search difficulty.
    :rtype: int
    """
    DIFFICULTYMAP = {
        Difficulty.NA: -1,
        Difficulty.AUTO: -3,
        Difficulty.DEMON: -2,
        Difficulty.EASY: 1,
        Difficulty.NORMAL: 2,
        Difficulty.HARD: 3,
        Difficulty.HARDER: 4,
        Difficulty.INSANE: 5,
    }

    return DIFFICULTYMAP.get(difficulty_obj, -1)


def determine_demon_search_difficulty(difficulty_obj: DemonDifficulty) -> int:
    """
    Converts a DemonDifficulty object to its corresponding integer value.

    :param difficulty_obj: The demon difficulty object.
    :type difficulty_obj: :class:`gd.entities.enums.DemonDifficulty`
    :return: Integer representing the demon search difficulty.
    :rtype: int
    :raises ValueError: If the demon difficulty object type is invalid.
    """

    # Convert the object to an interger value based on the search's enums.
    match difficulty_obj:
        case DemonDifficulty.EASY_DEMON:
            return 1
        case DemonDifficulty.MEDIUM_DEMON:
            return 2
        case DemonDifficulty.HARD_DEMON:
            return 3
        case DemonDifficulty.INSANE_DEMON:
            return 4
        case DemonDifficulty.EXTREME_DEMON:
            return 5
        case _:
            raise ValueError(
                f"Invalid demon difficulty object type {type(difficulty_obj)}"
            )


def determine_list_difficulty(
    raw_integer_difficulty: int,
) -> Union[Difficulty, DemonDifficulty]:
    """
    Converts a raw integer difficulty value to its corresponding Difficulty or DemonDifficulty object.

    :param raw_integer_difficulty: The raw integer difficulty value.
    :type raw_integer_difficulty: int
    :return: Corresponding Difficulty or DemonDifficulty object.
    :rtype: Union[:class:`gd.entities.enums.Difficulty`, :class:`gd.entities.enums.DemonDifficulty`]
    """
    return _DIFFICULTY_.get(raw_integer_difficulty, Difficulty.NA)


# Utility Functions
def is_newgrounds(id: int) -> bool:
    """
    Checks if a song ID is from Newgrounds.

    :param id: The song ID to check.
    :type id: int
    :return: True if the song ID is from Newgrounds, False otherwise.
    :rtype: bool
    """
    return id < START_ID_SONG_LIB


def parse_comma_separated_int_list(key: str) -> List[int]:
    """
    Split the string by `,` then turn it into a list of integers.

    :param key: The string containing comma-separated integers.
    :type key: str
    :return: A list of integers.
    :rtype: List[int]
    """
    try:
        return [int(x) for x in key.split(",") if x.isdigit()]
    except AttributeError:
        return []
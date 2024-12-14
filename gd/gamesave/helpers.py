"""
# gd.gamesave.helpers

A module for helper functions.
"""


def filter_valuekeeper_keys_by_type(valuekeeper: dict, key_type: str) -> list[int]:
    """
    Filter valuekeeper keys by their type.

    :param key_type: Key type to filter.
    :type key_type: str
    :return: A list of valuekeeper keys of the specified type.
    :rtype: list[any]
    """
    return [
        int(key.split("_")[1]) 
        for key in valuekeeper.keys() 
        if key_type == key.split("_")[0]
    ]

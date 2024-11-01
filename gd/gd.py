import colorama as color
from .helpers import *
from .errors import *
from .entities.level import *
from .entities.song import *
from .entities.user import *
from datetime import timedelta
from typing import Union, Tuple
from hashlib import sha1

_secret = "Wmfd2893gb7"
_secret_login = "Wmfv3899gc9"

# TODO: Organize methods into subclasses or something I don't even fucking know?
# TODO: fuck my sanity

def gjp(password: str = "", salt: str = "mI29fmAnxgTs") -> str:
    """
    Convert a password to an encrypted password.

    :param password: The password to be encrypted.
    :type password: str
    :param salt: The salt to use for encryption.
    :type salt: str
    :return: An encrypted password.
    """
    password += salt
    hash = sha1(password.encode()).hexdigest()

    return hash

class Client:
    """
    Main client class for interacting with Geometry Dash. You can login here using `.login` and the client will save the credientals to be used for later purposes.

    You can attach the client to an entity to interact with it without having trouble logging in again. Most entities uses `.add_client()` to attach a client.

    Example usage:
    ```
    >>> import gd
    >>> gd = gd.Client()
    >>> level = gd.search_level("sigma") # Returns a list of LevelDisplay instances
    [LevelDisplay(id=51657783, name='Sigma', description='Sigma', downloads=582753, likes=19492, ...), ...]
    ```
    """
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return (
            f"{color.Style.BRIGHT + color.Fore.LIGHTMAGENTA_EX}Client at {hex(id(self))}{color.Style.RESET_ALL}"
            "\n"
            "======================================="
            "\n"
            f"{color.Style.BRIGHT + color.Fore.LIGHTBLUE_EX}ID: {color.Style.NORMAL}{id(self)}{color.Style.RESET_ALL}"
            "\n"
            f"{color.Style.BRIGHT + color.Fore.LIGHTRED_EX}Hash: {color.Style.NORMAL}{self.__hash__()}{color.Style.RESET_ALL}"
            "\n"
            f"{color.Style.BRIGHT + color.Fore.LIGHTGREEN_EX}Account ID: {color.Style.NORMAL}{None}{color.Style.RESET_ALL}"
            "\n"
            f"{color.Style.BRIGHT + color.Fore.LIGHTCYAN_EX}Player ID: {color.Style.NORMAL}{None}{color.Style.RESET_ALL}"
            "\n"
            f"{color.Style.BRIGHT + color.Fore.LIGHTYELLOW_EX}Encrypted Password: {color.Style.NORMAL}{None}{color.Style.RESET_ALL}"
        )
    
    async def login(self, name: str, password: str) -> None:
        """
        ### This function is incomplete and will return errors and confusion if you used.
        Login account with given name and password (encrypted with `gjp()`)

        :param name: The account name.
        :type name: str
        :param password: The account password (encrypted with `gjp()`).
        :type password: str

        :return: Account
        """
        udid = generate_udid()
        data = {
            "secret": _secret_login, 
            "username": name, 
            "password": password,
            "udid": udid
        }

        response = await send_post_request(
            url="http://www.boomlings.com/database/accounts/loginGJAccount.php",
            data=data
        )
        return response

    async def download_level(self, id: int) -> Level:
        """
        Downloads a specific level from the Geometry Dash servers using the provided ID.
        
        :param id: The ID of the level.
        :type id: int
        :return: A `Level` instance containing the downloaded level data.
        """
        if not isinstance(id, int):
            raise ValueError("ID must be an int.")
        
        response = await send_post_request(
            url="http://www.boomlings.com/database/downloadGJLevel22.php", 
            data={"levelID": id, "secret": _secret}
        )

        # Check if response is valid
        check_errors(response, InvalidLevelID, f"Invalid level ID {id}.")

        return Level.from_raw(response)

    async def download_daily_level(self, weekly: bool = False, time_left: bool = False) -> Union[Level, Tuple[Level, timedelta]]:
        """
        Downloads the daily or weekly level from the Geometry Dash servers. You can return the time left for the level optionally.

        If `time_left` is set to True then returns a tuple containing the `Level` and the time left for the level.

        :param weekly: Whether to return the weekly or daily level. Defaults to False for daily.
        :type weekly: bool
        :param time_left: Whether to return both the level and the time left for the level. Defaults to False.
        :type time_left: bool
        :return: A `Level` instance containing the downloaded level data.
        """
        level_id = -2 if weekly else -1
        level = await self.download_level(level_id)
        
        # Makes another response for time left.
        if time_left:
            daily_data: str = await send_post_request(
                url="http://www.boomlings.com/database/getGJDailyLevel.php", 
                data={"secret": _secret, "weekly": "1" if weekly else "0"}
            )
            check_errors(daily_data, ResponseError, "Cannot get current time left for the daily/weekly level.")
            daily_data = daily_data.split("|")
            return level, timedelta(seconds=int(daily_data[1]))

        return level

    async def search_level(
        self, query: str = "", page: int = 0, 
        level_rating: LevelRating = None, length: Length = None,
        difficulty: List[Difficulty] = None, demon_difficulty: DemonDifficulty = None,
        two_player_mode: bool = False, has_coins: bool = False, original: bool = False,
        song_id: int = None, gd_world: bool = False, filter: SearchFilter = 0
    ) -> List[LevelDisplay]:
        """
        Searches for levels matching the given query string and filters them.

        To get a specific demon difficulty, make param `difficulty` as `Difficulty.DEMON`.

        **Note: `difficulty`, `length` and `query` does not work with `filter`!**

        :param query: The query for the search.
        :type query: Optional[str]
        :param page: The page number for the search. Defaults to 0.
        :type page: int
        :param level_rating: The level rating filter. (Featured, Epic, Legendary, ...)
        :type level_rating: Optional[LevelRating]
        :param length: The length filter.
        :type length: Optional[Length]
        :param difficulty: The difficulty filter.
        :type difficulty: Optional[List[Difficulty]]
        :param demon_difficulty: The demon difficulty filter.
        :type demon_difficulty: Optional[DemonDifficulty]
        :param two_player_mode: Filters level that has two player mode enabled.
        :type two_player_mode: Optional[bool]
        :param has_coins: Filters level that has coins.
        :type has_coins: Optional[bool]
        :param original: Filters level that has not been copied.
        :type original: Optional[bool]
        :param song_id: Filters level that has the specified song ID.
        :type song_id: Optional[int]
        :param gd_world: Filters level that is from Geometry Dash World.
        :type gd_world: Optional[bool]
        :param filter: Filters the result by Magic, Recent, ...
        :type filter: Optional[Union[filter, str]]

        :return: A list of `LevelDisplay` instances.
        """
        
        # Standard data
        data = {
            "secret": _secret,
            "type": filter.value if isinstance(filter, SearchFilter) else filter,
            "page": page,
        }
        
        # Level rating check
        if level_rating:
            match level_rating:
                case LevelRating.NO_RATE: data["noStar"] = 1
                case LevelRating.RATED: data["star"] = 1
                case LevelRating.FEATURED: data["featured"] = 1
                case LevelRating.EPIC: data["epic"] = 1
                case LevelRating.MYTHIC: data["legendary"] = 1
                case LevelRating.LEGENDARY: data["mythic"] = 1
                case _: raise ValueError("Invalid level rating, are you sure that it's a LevelRating object?")

        # Difficulty and demon difficulty checks
        if difficulty:
            if Difficulty.DEMON in difficulty and len(difficulty) > 1:
                raise ValueError("Difficulty.DEMON cannot be combined with other difficulties!")
            data["diff"] = ",".join(str(determine_search_difficulty(diff)) for diff in difficulty)

        if demon_difficulty:
            if difficulty != [Difficulty.DEMON]:
                raise ValueError("Demon difficulty can only be used with Difficulty.DEMON!")
            data["demonFilter"] = determine_search_difficulty(demon_difficulty)

        # Optional parameters
        if song_id:
            data.update({"customSong": 1, "song": song_id})

        optional_params = {
            "length": length.value if length else None,
            "twoPlayer": int(two_player_mode) if two_player_mode else None,
            "coins": int(has_coins) if has_coins else None,
            "original": int(original) if original else None,
            "gdw": int(gd_world) if gd_world else None,
            "str": query if query else None
        }

        # Update data with non-None values from optional_params
        data.update({k: v for k, v in optional_params.items() if v is not None})

        # Do the response
        search_data: str = await send_post_request(url="http://www.boomlings.com/database/getGJLevels21.php", data=data)
        
        check_errors(search_data, SearchLevelError, "Unable to fetch search results. Perhaps it doesn't exist after all?")

        parsed_results = parse_search_results(search_data)
        return [LevelDisplay.from_parsed(result).add_client(self) for result in parsed_results]

    async def music_library(self) -> MusicLibrary:
        """
        Gets the current music library in RobTop's servers.

        :return: A `MusicLibrary` instance containing all the music library data.
        """
        response = await send_get_request(
            url="https://geometrydashfiles.b-cdn.net/music/musiclibrary_02.dat",
        )

        music_library = decrypt_data(response, "base64_decompress")
        return MusicLibrary.from_raw(music_library)
    
    async def sfx_library(self) -> SoundEffectLibrary:
        """
        Gets the current Sound Effect library in RobTop's servers.

        :return: A `SoundEffectLibrary` instance containing all the SFX library data.
        """
        response = await send_get_request(
            url="https://geometrydashfiles.b-cdn.net/sfx/sfxlibrary.dat",
        )
        sfx_library = decrypt_data(response, "base64_decompress")
        return SoundEffectLibrary.from_raw(sfx_library)

    async def get_song(self, id: int) -> Song:
        """
        Gets song by ID, either from Newgrounds or the music library.

        :param id: The ID of the song. (Use ID larger than 10000000 to get the song from the library.)
        :type id: int
        :return: A `Song` instance containing the song data.
        """
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJSongInfo.php",
            data={'secret': _secret, "songID": id}
        )
        check_errors(response, InvalidSongID, f"Invalid song ID {id}.")
        return Song.from_raw(response)

    async def search_user(self, query: Union[str, int], use_id: bool = False) -> UserProfile:
        """
        Get an user profile by account ID or name.

        :param query: The account ID/name to retrieve the profile.
        :type query: Union[str, int]
        :param use_id: If searches the user using the account ID.
        :type use_id: Optional[bool]
        :return: A `UserProfile` instance containing the user's profile data.
        """
        
        if use_id:
            url = "http://www.boomlings.com/database/getGJUserInfo20.php"
            data = {'secret': _secret, "targetAccountID": query}
        else:
            url = "http://www.boomlings.com/database/getGJUsers20.php"
            data = {'secret': _secret, "str": query}

        response = await send_post_request(url=url, data=data)
        check_errors(response, InvalidAccountID, f"Invalid account name/ID {query}.")
        return UserProfile.from_raw(response.split("#")[0])
    
    async def get_level_comments(self, level_id: int, page: int = 0) -> List[Comment]:
        """
        Get level's comments by level ID.

        :param level_id: The ID of the level.
        :type level_id: int
        :param page: The page number for pagination. Defaults to 0.
        :type page: int
        :return: A list of `Comment` instances.
        """
        if page < 0:
            raise ValueError("Page number must be non-negative.")
        
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJComments21.php",
            data={'secret': _secret, "levelID": level_id, "page": page}
        )
        check_errors(response, InvalidLevelID, f"Invalid level ID {level_id}.")
        return [Comment.from_raw(comment_data) for comment_data in response.split("|")]
    
    async def get_user_posts(self, account_id: int, page: int = 0) -> Union[List[UserPost], None]:
        """
        Get an user's posts by Account ID.

        :param account_id: The account ID to retrieve the posts.
        :type account_id: int
        :param page: The page number for pagination. Defaults to 0.
        :type page: int
        :return: A list of `UserPost` instances or None if there are no posts.
        """
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJAccountComments20.php",
            data={'secret': _secret, "accountID": account_id, "page": page}
        )

        check_errors(response, ResponseError, "Invalid account ID.")
        if not response.split("#")[0]:
            return None

        posts_list = []
        parsed_res = response.split("#")[0]
        parsed_res = response.split("|")
        for post in parsed_res:
            posts_list.append(UserPost.from_raw(post, account_id))
        return posts_list
        
    async def get_user_comments(self, player_id: int, page: int = 0, display_most_liked: bool = False) -> Union[List[Comment], None]:
        """
        Get an user's comments history by player ID.
        
        :param player_id: The player ID to retrieve the comments history.
        :type player_id: int
        :param page: The page number for pagination. Defaults to 0.
        :type page: int
        :param display_most_liked: Whether to display the most liked comments. Defaults to False.
        :type display_most_liked: bool
        :return: A list of `Comment` instances or None if no comments were found.
        """
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJCommentHistory.php",
            data={'secret': _secret, "userID": player_id, "page": page, "mode": int(display_most_liked)}
        )
        check_errors(response, ResponseError, "Invalid account ID.")
        if not response.split("#")[0]:
            return None
        
        return [Comment.from_raw(comment_data) for comment_data in response.split("#")[0].split("|")]
    
    async def get_user_levels(self, player_id: int, page: int = 0) -> List[LevelDisplay]:
        """
        Get an user's levels by player ID.

        :param player_id: The player ID to retrieve the levels.
        :type player_id: int
        :param page: The page number to load, default is 0.
        :type page: int
        :return: A list of LevelDisplay instances.
        """

        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJLevels21.php",
            data={'secret': _secret, "type": 5, "page": page, "str": player_id}
        )

        check_errors(response, ResponseError, f"Invalid account ID {self.account_id}.")
        if not response.split("#")[0]:
            return None
        
        return [LevelDisplay.from_raw(level_data) for level_data in response.split("#")[0].split("|")]

    async def map_packs(self, page: int = 0) -> List[MapPack]:
        """
        Get the full list of map packs available (in a specific page).

        :return: A list of `MapPack` instances.
        """
        if page < 0:
            raise ValueError("Page must be a non-negative number.")
        elif page > 6:
            raise ValueError("Page limit is 6.")
        
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJMapPacks21.php",
            data={'secret': _secret, 'page': page}
        )
        check_errors(response, LoadError, "An error occurred when getting map packs.")
        map_packs = response.split('#')[0].split("|")
        return [MapPack.from_raw(map_pack_data) for map_pack_data in map_packs]

    async def gauntlets(self, only_2_point_1: bool = True, include_ncs_gauntlets: bool = True) -> List[Gauntlet]:
        """
        Get the list of gauntlets objects.

        :param only_2_point_1: Whether to get ONLY the 2.1 guantlets or both 2.2 and 2.1. Defaults to True.
        :type only_2_point_1: bool
        :param include_ncs_gauntlets: Whether to include NCS gauntlets to the list. Defaults to True.
        :type include_ncs_gauntlets: bool
        :return: A list of `Gauntlet` instances.
        """
        data = {'secret': _secret, 'special': int(only_2_point_1)}
        if include_ncs_gauntlets:
            data['binaryVersion'] = 46

        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJGauntlets21.php",
            data=data
        )

        check_errors(response, LoadError, "An error occurred when getting gauntlets.")
        guantlets = response.split('#')[0].split("|")
        list_guantlets = [Gauntlet.from_raw(guantlet) for guantlet in guantlets]

        return list_guantlets
    
    async def search_list(
        self, query: str = None, filter: SearchFilter = 0, page: int = 0, 
        difficulty: List[Difficulty] = None, demon_difficulty: DemonDifficulty = None,
        only_rated: bool = False
    ) -> List[LevelList]:
        """
        Search for lists.

        :param query: The query string to search for.
        :type query: str
        :param filter: Filter type (recent, magic, ...)
        :type filter: SearchFilter
        :param page: Page number (starting with 0)
        :type page: int
        :param difficulty: Filters by a specific difficulty.
        :type difficulty: List[Difficulty]
        :param demon_difficulty: Filters by a specific demon difficulty.
        :type demon_difficulty: DemonDifficulty
        :param only_rated: Filters only rated lists.
        :type only_rated: bool
        :return: A list of `LevelList` instances.
        """
        data = {
            'secret': _secret, 'str': query, 'type': filter, "page": page
        }

        if difficulty:
            if Difficulty.DEMON in difficulty and len(difficulty) > 1:
                raise ValueError("Difficulty.DEMON cannot be combined with other difficulties!")
            data["diff"] = ",".join(str(determine_search_difficulty(diff)) for diff in difficulty)

        if demon_difficulty:
            if difficulty != [Difficulty.DEMON]:
                raise ValueError("Demon difficulty can only be used with Difficulty.DEMON!")
            data["demonFilter"] = determine_demon_search_difficulty(demon_difficulty)

        if only_rated:
            data["star"] = 1

        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJLevelLists.php",
            data=data
        )

        check_errors(response, SearchLevelError, "An error occurred while searching lists, maybe it doesn't exist?")
        response = response.split("#")[0]
        
        return [LevelList.from_raw(level_list_data) for level_list_data in response.split("|")]
__doc__ = """
# `gdapi`

A lightweight and asynchronous API wrapper for **Geometry Dash** and **Pointercrate (soon)**.

```py
>>> from gd import Client
>>> client = Client()
>>> level = await client.download_level(13519)
>>> level.name
"The Nightmare"
>>> level.difficulty
Difficulty.EASY_DEMON
>>> level.description
"Hard map by Jax. 7813"
>>> level.official_song
OfficialSong.POLARGEIST
```

# Installation and Information
### *why the heck did i put that???? it's unfinished!!!!!*
Install GDAPI via PyPI:

```bash
$ python -m pip install gdapi
```
**GDAPI** supports Python version 3.7 or greater officially.

The package requires the following dependencies:
- aiohttp
- aiofiles
- colorama (For useless eye candy)

# Usage
### Downloading a level:
```py
>>> from gd import Client
>>> client = Client()
>>> level = await client.download_level(13519)
>>> level.name
"The Nightmare"
>>> level.difficulty
<DemonDifficulty.EASY_DEMON: 3>
>>> level.description
"Hard map by Jax. 7813"
>>> level.official_song
<OfficialSong.POLARGEIST: 2>
```

### Fetching a song and downloading it:
```py
>>> from gd import Client
>>> client = Client()
>>> song = await client.get_song(1)
>>> song.name
"Chilled 1"
>>> song.size
0.07
>>> song.link
"http://audio.ngfiles.com/0/1_newgrounds_consin.mp3"
>>> await song.download_to("chilled.mp3") # Download the song and name it "chilled.mp3" in the relative path.
```

### Getting the Music Library:
```py
>>> from gd import Client
>>> client = Client()
>>> library = await client.music_library()
>>> library.version
127
>>> library.artists
{10002716: Artist(id=10002716, name='Raul Ojamaa', website=None, youtube_channel_id=None),
 10002717: Artist(id=10002717, name='Malou', website=None, youtube_channel_id=None), ...}
>>> library.tags
{234: '8bit', 251: 'action', 239: 'ambiance', 246: 'ambient', 247: 'battle', 248: 'boss', 250: 'calm', 249: 'casual', ...}
```

### Login and comment:
```py
>>> from gd import Client
>>> client = Client()
>>> credientals = await client.login("notanerd1", "*********") # Password is hidden on purpose
>>> credientals
Account(account_id=24514763, player_id=218839712, name='notanerd1', password=********) # Hidden when printing the instance
>>> comment_id = await client.comment("I am high", level_id=111663149, percentage=0) # Comment on the level with the percentage of 0
2994273
```
"""

from datetime import timedelta
from typing import Union, Tuple, List
from hashlib import sha1
import base64

import colorama

from .parse import (
    parse_comma_separated_int_list,
    determine_search_difficulty,
    parse_search_results,
    determine_demon_search_difficulty,
)
from .exceptions import (
    check_errors,
    LoginError,
    CommentError,
    ResponseError,
    InvalidAccountID,
    InvalidLevelID,
    SearchLevelError,
    InvalidSongID,
    LoadError,
)
from .decode import CHKSalt, XorKey, generate_chk, decrypt_data
from .entities.enums import (
    Length,
    LevelRating,
    SearchFilter,
    DemonDifficulty,
    Difficulty,
)
from .entities.level import Level, LevelDisplay, Comment, MapPack, LevelList, Gauntlet
from .entities.song import MusicLibrary, SoundEffectLibrary, Song
from .entities.user import Account, Player, Post
from .helpers import send_get_request, send_post_request, cooldown, require_login

SECRET = "Wmfd2893gb7"
LOGIN_SECRET = "Wmfv3899gc9"

# ? Should I release this piece of shit after I am done with the login?


def gjp2(password: str = "", salt: str = "mI29fmAnxgTs") -> str:
    """
    Convert a password to an encrypted password.

    :param password: The password to be encrypted.
    :type password: str
    :param salt: The salt to use for encryption.
    :type salt: str
    :return: An encrypted password.
    """
    password += salt
    result = sha1(password.encode()).hexdigest()

    return result


class Client:
    """
    gd.Client
    =========

    Main client class for interacting with Geometry Dash. 
    
    You can login here using `.login` to be used for functions that needed an account.

    Example usage:
    .. code-block::
    >>> import gd
    >>> client = gd.Client()
    >>> level = await client.search_level("sigma") # Returns a list of "LevelDisplay" instances
    [LevelDisplay(id=51657783, name='Sigma', downloads=582753, likes=19492, ...), ...]

    Attributes
    ==========
    account : Union[Account, None]:
        The account associated with this client. The default is None.
    """

    account: Union[Account, None] = None
    """The account logged in with the client."""

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        account = self.account

        def color_format(text, color):
            return f"{colorama.Style.BRIGHT + color}{text}{colorama.Style.RESET_ALL}"

        info = [
            color_format(
                f"Client object at {hex(id(self))}", colorama.Fore.LIGHTMAGENTA_EX
            ),
            "=======================================",
            color_format(f"ID: {id(self)}", colorama.Fore.LIGHTBLUE_EX),
            color_format(f"Hash: {self.__hash__()}", colorama.Fore.LIGHTRED_EX),
            color_format(
                f"Is logged in: {self.logged_in}", colorama.Fore.LIGHTGREEN_EX
            ),
            color_format(
                f"Account Name: {account.name if account else None}",
                colorama.Fore.LIGHTYELLOW_EX,
            ),
            color_format(
                f"Account ID: {account.account_id if account else None}",
                colorama.Fore.LIGHTYELLOW_EX,
            ),
            color_format(
                f"Player ID: {account.player_id if account else None}",
                colorama.Fore.LIGHTYELLOW_EX,
            ),
            color_format(
                f"Encrypted Password: {account.gjp2 if account else None}",
                colorama.Fore.LIGHTYELLOW_EX,
            ),
        ]
        return "\n".join(info)

    @property
    def logged_in(self) -> bool:
        """If the client has logged in or not."""
        return bool(self.account)

    async def login(self, name: str, password: str) -> Account:
        """
        Login account with given name and password.

        :param name: The account name.
        :type name: str
        :param password: The account password.
        :type password: str

        :return: The Account instance
        :rtype: :class:`gd.entities.Account`
        """
        if self.account:
            raise LoginError("The client has already been logged in!")

        data = {
            "secret": LOGIN_SECRET,
            "userName": name,
            "gjp2": gjp2(password),
            "udid": "blah blah placeholder HAHAHHAH",
        }

        response = await send_post_request(
            url="http://www.boomlings.com/database/accounts/loginGJAccount.php",
            data=data,
        )

        match response:
            case "-1":
                raise LoginError
            case "-8":
                raise LoginError("User password must be at least 6 characters long")
            case "-9":
                raise LoginError("Username must be at least 3 characters long")
            case "-11":
                raise LoginError("Invalid credentials.")
            case "-12":
                raise LoginError("Account has been disabled.")
            case "-13":
                raise LoginError("Invalid steam ID has passed.")

        account_id, player_id = parse_comma_separated_int_list(response)
        self.account = Account(
            account_id=account_id, player_id=player_id, name=name, password=password
        )
        return self.account

    @cooldown(10)
    async def change_account(self, name: str, password: str) -> Account:
        """
        An atomic way of logging out then logging in.

        Cooldown is 10 seconds.

        :param name: The account name.
        :type name: str
        :param password: The account password.
        :type password: str

        :return: The account instance
        :rtype: :class:`gd.entities.Account`
        """
        if not self.account:
            raise LoginError(
                "The client is not logged in to change accounts! Use .login() instead."
            )

        self.logout()
        return await self.login(name, password)

    def logout(self) -> None:
        """
        Logs out the current account.

        :return: None
        :rtype: None
        """
        self.account = None

    @cooldown(15)
    @require_login("You need to login before you can send a post!")
    async def send_post(self, message: str) -> int:
        """
        Sends an account comment to the account logged in.

        Cooldown is 15 seconds.

        :param message: The message to send.
        :type message: str
        :raises: gd.ResponseError
        :return: The post ID of the sent post.
        :rtype: int
        """
        if not self.account:
            raise LoginError("The client is not logged in to post!")

        data = {
            "secret": SECRET,
            "accountID": self.account.account_id,
            "comment": base64.urlsafe_b64encode(message.encode()).decode(),
            "gjp2": self.account.gjp2,
        }

        response = await send_post_request(
            url="http://www.boomlings.com/database/uploadGJAccComment20.php", data=data
        )

        return int(response)

    @cooldown(10)
    @require_login("You need to login before you can comment!")
    async def comment(self, message: str, level_id: int, percentage: int = 0) -> int:
        """
        Sends a comment to a level or list.

        For lists, use a **negative ID.**

        Cooldown is 10 seconds.

        :param message: The message to send.
        :type message: str
        :param level_id: The ID of the level to comment on.
        :type level_id: int
        :param percentage: The percentage of the level completed, optional. Defaults to 0.
        :type percentage: int
        :raises: gd.CommentError
        :return: The comment ID of the sent comment.
        :rtype: int
        """
        data = {
            "secret": SECRET,
            "accountID": self.account.account_id,
            "levelID": level_id,
            "userName": self.account.name,
            "percent": percentage,
            "comment": base64.urlsafe_b64encode(message.encode()).decode(),
            "gjp2": self.account.gjp2,
        }

        data["chk"] = generate_chk(
            values=[
                data["userName"],
                data["comment"],
                data["levelID"],
                data["percent"],
            ],
            key=XorKey.COMMENT,
            salt=CHKSalt.COMMENT,
        )

        response = await send_post_request(
            url="http://www.boomlings.com/database/uploadGJComment21.php", data=data
        )

        check_errors(
            response,
            CommentError,
            "Unable to post comment, maybe the level ID is wrong?",
        )

        return int(response)

    @cooldown(3)
    async def download_level(self, level_id: int) -> Level:
        """
        Downloads a specific level from the Geometry Dash servers using the provided ID.

        Cooldown is 3 seconds.

        :param id: The ID of the level.
        :type id: int
        :raises: gd.InvalidLevelID
        :return: A `Level` instance containing the downloaded level data.
        :rtype: :class:`gd.entities.Level`
        """
        if not isinstance(level_id, int):
            raise ValueError("ID must be an int.")

        response = await send_post_request(
            url="http://www.boomlings.com/database/downloadGJLevel22.php",
            data={"levelID": level_id, "secret": SECRET},
        )

        # Check if response is valid
        check_errors(response, InvalidLevelID, f"Invalid level ID {level_id}.")

        return Level.from_raw(response).add_client(self)

    @cooldown(3)
    async def download_daily_level(
        self, weekly: bool = False, time_left: bool = False
    ) -> Union[Level, Tuple[Level, timedelta]]:
        """
        Downloads the daily or weekly level from the Geometry Dash servers.

        Cooldown is 3 seconds.

        :param weekly: Whether to return the weekly or daily level. Defaults to False for daily.
        :type weekly: bool
        :param time_left: If return a tuple containing the `Level` and the time left for the level.
        :type time_left: bool
        :raises: gd.ResponseError
        :return: A `Level` instance containing the downloaded level data.
        :rtype: :class:`gd.entities.Level`
        """
        level_id = -2 if weekly else -1
        level = await self.download_level(level_id)

        # Makes another response for time left.
        if time_left:
            daily_data: str = await send_post_request(
                url="http://www.boomlings.com/database/getGJDailyLevel.php",
                data={"secret": SECRET, "type": "1" if weekly else "0"},
            )
            check_errors(
                daily_data,
                ResponseError,
                "Cannot get current time left for the daily/weekly level.",
            )
            daily_data = daily_data.split("|")
            return level, timedelta(seconds=int(daily_data[1]))

        return level

    async def search_level(
        self,
        query: str = "",
        page: int = 0,
        level_rating: LevelRating = None,
        length: Length = None,
        difficulty: List[Difficulty] = None,
        demon_difficulty: DemonDifficulty = None,
        two_player_mode: bool = False,
        has_coins: bool = False,
        original: bool = False,
        song_id: int = None,
        gd_world: bool = False,
        src_filter: SearchFilter = 0,
    ) -> List[LevelDisplay]:
        """
        Searches for levels matching the given query string and filters them.

        To get a specific demon difficulty, make param `difficulty` as `Difficulty.DEMON`.

        **Note: `difficulty`, `length` and `query` does not work with `filter`!**

        Cooldown is 2 seconds.

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

        :raises: gd.SearchLevelError
        :raises: ValueError

        :return: A list of `LevelDisplay` instances.
        :rtype: List[:class:`gd.entities.LevelDisplay`]
        """
        if filter == SearchFilter.FRIENDS and self.logged_in:
            raise ValueError("Cannot filter by friends without being logged in.")

        # Standard data
        data = {
            "secret": SECRET,
            "type": (
                src_filter.value if isinstance(src_filter, SearchFilter) else src_filter
            ),
            "page": page,
        }

        # Level rating check
        if level_rating:
            match level_rating:
                case LevelRating.NO_RATE:
                    data["noStar"] = 1
                case LevelRating.RATED:
                    data["star"] = 1
                case LevelRating.FEATURED:
                    data["featured"] = 1
                case LevelRating.EPIC:
                    data["epic"] = 1
                case LevelRating.MYTHIC:
                    data["legendary"] = 1
                case LevelRating.LEGENDARY:
                    data["mythic"] = 1
                case _:
                    raise ValueError(
                        "Invalid level rating, are you sure that it's a LevelRating object?"
                    )

        # Difficulty and demon difficulty checks
        if difficulty:
            if Difficulty.DEMON in difficulty and len(difficulty) > 1:
                raise ValueError(
                    "Difficulty.DEMON cannot be combined with other difficulties!"
                )
            data["diff"] = ",".join(
                str(determine_search_difficulty(diff)) for diff in difficulty
            )

        if demon_difficulty:
            if difficulty != [Difficulty.DEMON]:
                raise ValueError(
                    "Demon difficulty can only be used with Difficulty.DEMON!"
                )
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
            "str": query if query else None,
            "accountID": self.account.account_id if self.account else None,
            "gjp2": self.account.gjp2 if self.account else None,
        }

        # Update data with non-None values from optional_params
        data.update({k: v for k, v in optional_params.items() if v is not None})

        # Do the response
        search_data: str = await send_post_request(
            url="http://www.boomlings.com/database/getGJLevels21.php", data=data
        )

        check_errors(
            search_data,
            SearchLevelError,
            "Unable to fetch search results. Perhaps it doesn't exist after all?",
        )

        parsed_results = parse_search_results(search_data)
        return [
            LevelDisplay.from_parsed(result).add_client(self)
            for result in parsed_results
        ]

    @cooldown(10)
    async def music_library(self) -> MusicLibrary:
        """
        Gets the current music library in RobTop's servers.

        Cooldown is 10 seconds.

        :return: A `MusicLibrary` instance containing all the music library data.
        :rtype: :class:`gd.entities.song.MusicLibrary`
        """
        response = await send_get_request(
            url="https://geometrydashfiles.b-cdn.net/music/musiclibrary_02.dat",
        )

        music_library = decrypt_data(response, "base64_decompress")
        return MusicLibrary.from_raw(music_library)

    @cooldown(10)
    async def sfx_library(self) -> SoundEffectLibrary:
        """
        Gets the current Sound Effect library in RobTop's servers.

        Cooldown is 10 seconds.

        :return: A `SoundEffectLibrary` instance containing all the SFX library data.
        :rtype: :class:`gd.entities.song.SoundEffectLibrary`
        """
        response = await send_get_request(
            url="https://geometrydashfiles.b-cdn.net/sfx/sfxlibrary.dat",
        )
        sfx_library = decrypt_data(response, "base64_decompress")
        return SoundEffectLibrary.from_raw(sfx_library)

    @cooldown(1)
    async def get_song(self, song_id: int) -> Song:
        """
        Gets song by ID, either from Newgrounds or the music library.

        Cooldown is 2 seconds.

        :param id: The ID of the song.
        :type id: int
        :return: A `Song` instance containing the song data.
        :raises: gd.InvalidSongID
        :rtype: :class:`gd.entities.song.Song`
        """
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJSongInfo.php",
            data={"secret": SECRET, "songID": song_id},
        )
        check_errors(response, InvalidSongID, "")

        return Song.from_raw(response)

    async def search_user(self, query: Union[str, int], use_id: bool = False) -> Player:
        """
        Get an user profile by account ID or name.

        :param query: The account ID/name to retrieve the profile.
        :type query: Union[str, int]
        :param use_id: If searches the user using the account ID.
        :type use_id: Optional[bool]
        :raises: gd.InvalidAccountID
        :return: A `Player` instance containing the user's profile data.
        :rtype: :class:`gd.entities.user.Player`
        """

        if use_id:
            url = "http://www.boomlings.com/database/getGJUserInfo20.php"
            data = {"secret": SECRET, "targetAccountID": query}
        else:
            url = "http://www.boomlings.com/database/getGJUsers20.php"
            data = {"secret": SECRET, "str": query}

        response = await send_post_request(url=url, data=data)
        check_errors(response, InvalidAccountID, f"Invalid account name/ID {query}.")
        return Player.from_raw(response.split("#")[0])

    async def get_level_comments(self, level_id: int, page: int = 0) -> List[Comment]:
        """
        Get level's comments by level ID.

        :param level_id: The ID of the level.
        :type level_id: int
        :param page: The page number for pagination. Defaults to 0.
        :type page: int
        :raises: gd.InvalidLevelID
        :return: A list of `Comment` instances.
        :rtype: :class:`gd.entities.level.Comment`
        """
        if page < 0:
            raise ValueError("Page number must be non-negative.")

        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJComments21.php",
            data={"secret": SECRET, "levelID": level_id, "page": page},
        )
        check_errors(response, InvalidLevelID, f"Invalid level ID {level_id}.")
        return [Comment.from_raw(comment_data) for comment_data in response.split("|")]

    async def get_user_posts(self, account_id: int, page: int = 0) -> List[Post]:
        """
        Get an user's posts by Account ID.

        :param account_id: The account ID to retrieve the posts.
        :type account_id: int
        :param page: The page number for pagination. Defaults to 0.
        :type page: int
        :raises: gd.InvalidAccountID
        :return: A list of `Post` instances or None if there are no posts.
        :rtype: List[:class:`gd.entities.user.Post`]
        """
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJAccountComments20.php",
            data={"secret": SECRET, "accountID": account_id, "page": page},
        )

        check_errors(response, InvalidAccountID, "Invalid account ID.")
        if not response.split("#")[0]:
            return None

        posts_list = []
        parsed_res = response.split("#")[0]
        parsed_res = response.split("|")

        for post in parsed_res:
            posts_list.append(Post.from_raw(post, account_id))

        return posts_list

    async def get_user_comments(
        self, player_id: int, page: int = 0, display_most_liked: bool = False
    ) -> List[Comment]:
        """
        Get an user's comments history by player ID.

        :param player_id: The player ID to retrieve the comments history.
        :type player_id: int
        :param page: The page number for pagination. Defaults to 0.
        :type page: int
        :param display_most_liked: Whether to display the most liked comments. Defaults to False.
        :type display_most_liked: bool
        :raises: gd.InvalidAccountID
        :return: A list of `Comment` instances or None if no comments were found.
        :rtype: List[:class:`gd.entities.level.Comment`]
        """
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJCommentHistory.php",
            data={
                "secret": SECRET,
                "userID": player_id,
                "page": page,
                "mode": int(display_most_liked),
            },
        )
        check_errors(response, InvalidAccountID, "Invalid account ID.")
        if not response.split("#")[0]:
            return None

        return [
            Comment.from_raw(comment_data)
            for comment_data in response.split("#")[0].split("|")
        ]

    async def get_user_levels(
        self, player_id: int, page: int = 0
    ) -> List[LevelDisplay]:
        """
        Get an user's levels by player ID.

        :param player_id: The player ID to retrieve the levels.
        :type player_id: int
        :param page: The page number to load, default is 0.
        :type page: int
        :return: A list of LevelDisplay instances.
        :rtype: List[:class:`gd.entities.level.LevelDisplay`]
        """

        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJLevels21.php",
            data={"secret": SECRET, "type": 5, "page": page, "str": player_id},
        )

        check_errors(response, InvalidAccountID, f"Invalid account ID {player_id}.")

        if not response.split("#")[0]:
            return None

        return [
            LevelDisplay.from_raw(level_data)
            for level_data in response.split("#")[0].split("|")
        ]

    async def map_packs(self, page: int = 0) -> List[MapPack]:
        """
        Get the full list of map packs available (in a specific page).

        :param page: The page number to load, default is 0.
        :type page: int
        :raises: gd.LoadError
        :return: A list of `MapPack` instances.
        :rtype: List[:class:`gd.entities.level.MapPack`]
        """
        if page < 0:
            raise ValueError("Page must be a non-negative number.")

        if page > 6:
            raise ValueError("Page limit is 6.")

        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJMapPacks21.php",
            data={"secret": SECRET, "page": page},
        )
        check_errors(response, LoadError, "An error occurred when getting map packs.")
        map_packs = response.split("#")[0].split("|")
        return [MapPack.from_raw(map_pack_data) for map_pack_data in map_packs]

    async def gauntlets(self, not_2_2: bool = True, ncs: bool = True) -> List[Gauntlet]:
        """
        Get the list of gauntlets objects.

        :param not_2_2: Whether to get ONLY the 2.1 guantlets or both versions.
        :type not_2_2: bool
        :param ncs: Whether to include NCS gauntlets to the list. Defaults to True.
        :type ncs: bool
        :raises: gd.LoadError
        :return: A list of `Gauntlet` instances.
        :rtype: List[:class:`gd.entities.level.Gauntlet`]
        """
        data = {"secret": SECRET, "special": int(not not_2_2)}
        if ncs:
            data["binaryVersion"] = 46

        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJGauntlets21.php", data=data
        )

        check_errors(response, LoadError, "An error occurred when getting gauntlets.")
        guantlets = response.split("#")[0].split("|")
        list_guantlets = [Gauntlet.from_raw(guantlet) for guantlet in guantlets]

        return list_guantlets

    async def search_list(
        self,
        query: str = None,
        src_filter: SearchFilter = 0,
        page: int = 0,
        difficulty: List[Difficulty] = None,
        demon_difficulty: DemonDifficulty = None,
        only_rated: bool = False,
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
        :raises: gd.SearchLevelError
        :return: A list of `LevelList` instances.
        :rtype: List[:class:`gd.entities.level.LevelList`]
        """
        if filter == SearchFilter.FRIENDS and not self.account:
            raise ValueError("Only friends search is available when logged in.")

        data = {"secret": SECRET, "str": query, "type": src_filter, "page": page}

        if difficulty:
            if Difficulty.DEMON in difficulty and len(difficulty) > 1:
                raise ValueError(
                    "Difficulty.DEMON cannot be combined with other difficulties!"
                )
            data["diff"] = ",".join(
                str(determine_search_difficulty(diff)) for diff in difficulty
            )

        if demon_difficulty:
            if difficulty != [Difficulty.DEMON]:
                raise ValueError(
                    "Demon difficulty can only be used with Difficulty.DEMON!"
                )
            data["demonFilter"] = determine_demon_search_difficulty(demon_difficulty)

        if only_rated:
            data["star"] = 1

        if data["type"] == SearchFilter.FRIENDS:
            data["accountID"] = self.account.account_id
            data["gjp2"] = self.account.gjp2

        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJLevelLists.php", data=data
        )

        check_errors(
            response,
            SearchLevelError,
            "An error occurred while searching lists, maybe it doesn't exist?",
        )
        response = response.split("#")[0]

        return [
            LevelList.from_raw(level_list_data)
            for level_list_data in response.split("|")
        ]

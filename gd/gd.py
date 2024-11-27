__doc__ = """Accessing the Geometry Dash API programmatically."""

from datetime import timedelta
from typing import Union, Optional
import base64
import asyncio

from .parse import (
    parse_comma_separated_int_list,
    determine_search_difficulty,
    parse_search_results,
    determine_demon_search_difficulty,
)
from .exceptions import (
    check_errors,
    LoadError,
    InvalidID,
    LoginError,
)
from .cryptography import (
    Salt,
    XorKey,
    gjp2,
    generate_chk,
    base64_decompress,
    generate_rs,
    generate_digits,
    cyclic_xor,
    base64_urlsafe_decode,
)
from .entities.enums import (
    Length,
    LevelRating,
    SearchFilter,
    DemonDifficulty,
    Difficulty,
    SpecialLevel,
    Leaderboard,
    Item,
)
from .entities.level import Level, LevelDisplay, Comment, MapPack, LevelList, Gauntlet
from .entities.song import MusicLibrary, SoundEffectLibrary, Song
from .entities.user import Account, Player, Post, Quest
from .helpers import send_get_request, send_post_request, cooldown, require_login

SECRET = "Wmfd2893gb7"
LOGIN_SECRET = "Wmfv3899gc9"
UDID = "S15213625602582389853976435292167231001"


class Client:
    """
    gd.Client
    =========

    Main client class for interacting with Geometry Dash.

    Use `.login()` to perform a safe login.
    Otherwise use `.unsafe_login()` or put the credientals directly in the parameters to skip the verfication.

    Example usage:
    .. code-block::
    >>> import gd
    >>> client = gd.Client()
    >>> level = await client.search_levels(query="sigma") # Returns a list of "LevelDisplay" instances
    [LevelDisplay(id=51657783, name='Sigma', downloads=582753, likes=19492, ...), ...]

    Attributes
    ==========
    account : Optional[Account]:
        The account associated with this client.
    """

    account: Optional[Account] = None
    """The account associated with this client."""
    udid: str = "S15213625602582389853976435292167231001"
    """The UDID of the client"""

    def __init__(
        self,
        account: Optional[Account] = None,
        udid: str = "S15213625602582389853976435292167231001",
    ) -> None:
        self.account = account
        self.udid = udid

    def __repr__(self) -> str:
        return f"<gd.Client account={self.account}>"

    @property
    def logged_in(self) -> bool:
        """If the client has logged in or not."""
        return bool(self.account)

    @logged_in.setter
    def logged_in(self) -> None:
        raise ValueError("This property is frozen.")

    async def check_login(self) -> bool:
        """
        Checks if the account credientials are correct.

        :return: True if the credentials are correct, False otherwise.
        :rtype: bool
        """
        if not self.account:
            return False

        data = {
            "secret": LOGIN_SECRET,
            "userName": self.account.name,
            "gjp2": self.account.gjp2,
            "udid": "blah blah placeholder HAHAHHAH",
        }

        response = await send_post_request(
            url="http://www.boomlings.com/database/accounts/loginGJAccount.php",
            data=data,
        )
        response = response.text

        return response.text == f"{self.account.account_id}|{self.account.player_id}"

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
        response = response.text

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

    def unsafe_login(
        self, name: str, password: str, account_id: int, player_id: int
    ) -> Account:
        """
        Login account with given name and password without any additional checks.

        :param name: The account name.
        :type name: str
        :param password: The account password.
        :type password: str
        :param account_id: The account ID.
        :type account_id: int
        :param player_id: The player ID.
        :type player_id: int

        :return: The Account instance
        :rtype: :class:`gd.entities.Account`
        """
        self.account = Account(
            account_id=account_id, player_id=player_id, name=name, password=password
        )
        return self.account

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
        Sends a post to the account logged in.

        Cooldown is 15 seconds.

        :param message: The message to send.
        :type message: str
        :raises: gd.LoadError
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
        response = response.text

        return int(response)

    @cooldown(10)
    @require_login("You need to login before you can comment!")
    async def send_comment(
        self, message: str, level_id: int, percentage: int = 0
    ) -> int:
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
        :raises: gd.InvalidID
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
            salt=Salt.COMMENT,
        )

        response = await send_post_request(
            url="http://www.boomlings.com/database/uploadGJComment21.php", data=data
        )
        response = response.text

        check_errors(
            response,
            InvalidID,
            "Unable to post comment, maybe the level ID is wrong?",
        )

        return int(response)

    @require_login("You need to login before you can use this function!")
    async def delete_post(self, post_id: int) -> None:
        """
        Deletes a post using comment ID.

        :param post_id: The ID of the post to delete.
        :type post_id: int
        :raises: gd.InvalidID
        :return: None
        :rtype: None
        """
        response = send_post_request(
            url="http://www.boomlings.com/database/deleteGJAccComment20.php",
            data={
                "accountID": self.account.account_id,
                "commentID": post_id,
                "gjp2": self.account.gjp2,
                "secret": SECRET,
            },
        )
        response = response.text

        check_errors(
            response,
            InvalidID,
            "Unable to delete post, perhaps wrong ID?",
        )

    @require_login("You need to login before you can use this function!")
    async def delete_comment(self, comment_id: int, level_id: int) -> None:
        """
        Deletes a comment using the comment's level ID and ID.

        :param comment_id: The ID of the comment to delete.
        :type comment_id: int
        :param level_id: The ID of the level the comment belongs to.
        :type level_id: int
        :raises: gd.InvalidID
        :return: None
        :rtype: None
        """
        response = send_post_request(
            url="http://www.boomlings.com/database/deleteGJComment20.php",
            data={
                "accountID": self.account.account_id,
                "commentID": comment_id,
                "levelID": level_id,
                "gjp2": self.account.gjp2,
                "secret": SECRET,
            },
        )
        response = response.text

        check_errors(
            response,
            InvalidID,
            "Invalid comment or level ID.",
        )

    @cooldown(3)
    async def download_level(self, level_id: int) -> Level:
        """
        Downloads a specific level from the Geometry Dash servers using the provided ID.

        Cooldown is 3 seconds.

        :param id: The ID of the level.
        :type id: int
        :raises: gd.InvalidID
        :return: A `Level` instance containing the downloaded level data.
        :rtype: :class:`gd.entities.Level`
        """
        if not isinstance(level_id, int):
            raise ValueError("ID must be an int.")

        response = await send_post_request(
            url="http://www.boomlings.com/database/downloadGJLevel22.php",
            data={"levelID": level_id, "secret": SECRET},
        )
        response = response.text

        # Check if response is valid
        check_errors(response, InvalidID, f"Invalid level ID {level_id}.")

        return Level.from_raw(response).add_client(self)

    @cooldown(3)
    async def download_special_level(
        self, special: SpecialLevel, time_left: bool = False
    ) -> Union[Level, tuple[Level, timedelta]]:
        """
        Downloads the daily or weekly level from the Geometry Dash servers.

        Cooldown is 3 seconds.

        :param special: The special level to download (e.g., daily or weekly).
        :type special: SpecialLevel
        :param time_left: If return a tuple containing the `Level` and the time left until the level is switched.
        :type time_left: bool
        :raises: gd.LoadError
        :return: A `Level` instance containing the downloaded level data.
        :rtype: :class:`gd.entities.Level`
        """
        # Use asyncio.gather to download the level and time left concurrently if needed
        tasks = [self.download_level(special)]

        if time_left:
            tasks.append(
                send_post_request(
                    url="http://www.boomlings.com/database/getGJDailyLevel.php",
                    data={"secret": SECRET, "type": special},
                )
            )

            level, daily_data = await asyncio.gather(*tasks)
            daily_data = daily_data.text
            check_errors(
                daily_data,
                LoadError,
                "Cannot get current time left for the daily/weekly level.",
            )

            daily_data = daily_data.split("|")
            return level.text, timedelta(seconds=int(daily_data[1]))

        level = await asyncio.gather(*tasks)

        return level.text

    async def search_level(
        self,
        query: str = "",
        page: int = 0,
        level_rating: LevelRating = None,
        length: Length = None,
        difficulty: list[Difficulty] = None,
        demon_difficulty: DemonDifficulty = None,
        two_player_mode: bool = False,
        has_coins: bool = False,
        original: bool = False,
        song_id: int = None,
        gd_world: bool = False,
        src_filter: SearchFilter = 0,
    ) -> list[LevelDisplay]:
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
        :type difficulty: Optional[list[Difficulty]]
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
        :param src_filter: Filters the result by Magic, Recent, ...
        :type src_filter: Optional[Union[filter, str]]

        :raises: gd.LoadError
        :raises: ValueError

        :return: A list of `LevelDisplay` instances.
        :rtype: list[:class:`gd.entities.LevelDisplay`]
        """
        if src_filter == SearchFilter.FRIENDS and self.logged_in:
            raise ValueError("Cannot filter by friends without being logged in.")

        # Initialize data
        data = {
            "secret": SECRET,
            "type": (
                src_filter.value if isinstance(src_filter, SearchFilter) else src_filter
            ),
            "page": page,
            **{  # Level rating check
                "noStar": 1 if level_rating == LevelRating.NO_RATE else None,
                "star": 1 if level_rating == LevelRating.RATED else None,
                "featured": 1 if level_rating == LevelRating.FEATURED else None,
                "epic": 1 if level_rating == LevelRating.EPIC else None,
                "legendary": 1 if level_rating == LevelRating.MYTHIC else None,
                "mythic": 1 if level_rating == LevelRating.LEGENDARY else None,
            },
            **{  # Difficulty and demon difficulty checks
                "diff": (
                    ",".join(
                        str(determine_search_difficulty(diff)) for diff in difficulty
                    )
                    if difficulty
                    else None
                ),
                "demonFilter": (
                    determine_search_difficulty(demon_difficulty)
                    if demon_difficulty and difficulty == [Difficulty.DEMON]
                    else None
                ),
            },
            **{  # Optional parameters
                "customSong": 1 if song_id else None,
                "song": song_id,
                "length": length.value if length else None,
                "twoPlayer": int(two_player_mode) if two_player_mode else None,
                "coins": int(has_coins) if has_coins else None,
                "original": int(original) if original else None,
                "gdw": int(gd_world) if gd_world else None,
                "str": query or None,
                "accountID": self.account.account_id if self.account else None,
                "gjp2": self.account.gjp2 if self.account else None,
            },
        }

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        # Perform search
        search_data = await send_post_request(
            url="http://www.boomlings.com/database/getGJLevels21.php", data=data
        )
        search_data = search_data.text

        check_errors(search_data, LoadError, "Unable to fetch search results.")
        parsed_results = parse_search_results(search_data)

        return [
            LevelDisplay.from_parsed(result).add_client(self)
            for result in parsed_results
        ]

    @require_login("You need to log in before you can view the leaderboard.")
    async def level_leaderboard(
        self, level_id: int, friends: bool = False, week: bool = False
    ) -> list[Player]:
        """
        Gets the leaderboard for a given level.

        :param level_id: The ID of the level.
        :type level_id: int
        :param friends: Whether to include get friends' scores in the leaderboard. Defaults to False.
        :return: A list of Player instances representing the leaderboard.
        :rtype: list[:class:`gd.entities.Player`]
        """
        if friends and week:
            raise ValueError("Cannot fetch both friends and weekly leaderboard.")

        leaderboard = 1
        if friends:
            leaderboard = 0
        elif week:
            leaderboard = 2

        data = {
            "secret": SECRET,
            "type": leaderboard,
            "levelID": level_id,
            "accountID": self.account.account_id,
            "gjp2": self.account.gjp2,
        }

        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJLevelScores211.php", data=data
        )

        check_errors(
            response,
            LoadError,
            "Unable to fetch level leaderboard.",
        )

        response = response.text.split("#")[0].split("|")

        return [
            Player.from_raw(player_data).add_client(self) for player_data in response
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
        response = response.content.decode()

        music_library = base64_decompress(response)
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
        response = response.content.decode()

        sfx_library = base64_decompress(response)
        return SoundEffectLibrary.from_raw(sfx_library)

    @cooldown(1)
    async def get_song(self, song_id: int) -> Song:
        """
        Gets song by ID, either from Newgrounds or the music library.

        Cooldown is 2 seconds.

        :param id: The ID of the song.
        :type id: int
        :return: A `Song` instance containing the song data.
        :raises: gd.InvalidID
        :rtype: :class:`gd.entities.song.Song`
        """
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJSongInfo.php",
            data={"secret": SECRET, "songID": song_id},
        )
        response = response.text

        check_errors(response, InvalidID, "")

        return Song.from_raw(response)

    async def search_user(self, query: Union[str, int], use_id: bool = False) -> Player:
        """
        Get an user profile by account ID or name.

        :param query: The account ID/name to retrieve the profile.
        :type query: Union[str, int]
        :param use_id: If searches the user using the account ID.
        :type use_id: Optional[bool]
        :raises: gd.InvalidID
        :return: A `Player` instance containing the user's profile data.
        :rtype: :class:`gd.entities.user.Player`
        """

        if use_id:
            url = "http://www.boomlings.com/database/getGJUserInfo20.php"
            data = {
                "secret": SECRET,
                "targetAccountID": query,
                "gjp2": self.account.gjp2 if self.logged_in else None,
                "accountID": self.account.account_id if self.logged_in else None,
            }
        else:
            url = "http://www.boomlings.com/database/getGJUsers20.php"
            data = {"secret": SECRET, "str": query}

        response = await send_post_request(url=url, data=data)
        response = response.text

        check_errors(response, InvalidID, f"Invalid account name/ID {query}.")
        return Player.from_raw(response.split("#")[0]).add_client(self)

    async def get_level_comments(self, level_id: int, page: int = 0) -> list[Comment]:
        """
        Get level's comments by level ID.

        :param level_id: The ID of the level.
        :type level_id: int
        :param page: The page number for pagination. Defaults to 0.
        :type page: int
        :raises: gd.InvalidID
        :return: A list of `Comment` instances.
        :rtype: :class:`gd.entities.level.Comment`
        """
        if page < 0:
            raise ValueError("Page number must be non-negative.")

        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJComments21.php",
            data={"secret": SECRET, "levelID": level_id, "page": page},
        )
        response = response.text

        check_errors(response, InvalidID, f"Invalid level ID {level_id}.")
        return [
            Comment.from_raw(comment_data).add_client(self)
            for comment_data in response.split("|")
        ]

    async def get_user_posts(self, account_id: int, page: int = 0) -> list[Post]:
        """
        Get an user's posts by Account ID.

        :param account_id: The account ID to retrieve the posts.
        :type account_id: int
        :param page: The page number for pagination. Defaults to 0.
        :type page: int
        :raises: gd.InvalidID
        :return: A list of `Post` instances or None if there are no posts.
        :rtype: list[:class:`gd.entities.user.Post`]
        """
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJAccountComments20.php",
            data={"secret": SECRET, "accountID": account_id, "page": page},
        )
        response = response.text

        check_errors(response, InvalidID, "Invalid account ID.")

        if not response.split("#")[0]:
            return None

        posts_list = []
        parsed_res = response.split("#")[0]
        parsed_res = response.split("|")

        for post in parsed_res:
            posts_list.append(Post.from_raw(post, account_id).add_client(self))

        return posts_list

    async def get_user_comments(
        self, player_id: int, page: int = 0, display_most_liked: bool = False
    ) -> list[Comment]:
        """
        Get an user's comments history by player ID.

        :param player_id: The player ID to retrieve the comments history.
        :type player_id: int
        :param page: The page number for pagination. Defaults to 0.
        :type page: int
        :param display_most_liked: Whether to display the most liked comments. Defaults to False.
        :type display_most_liked: bool
        :raises: gd.InvalidID
        :return: A list of `Comment` instances or None if no comments were found.
        :rtype: list[:class:`gd.entities.level.Comment`]
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
        response = response.text

        check_errors(response, InvalidID, "Invalid player ID.")

        if not response.split("#")[0]:
            return None

        return [
            Comment.from_raw(comment_data).add_client(self)
            for comment_data in response.split("#")[0].split("|")
        ]

    async def get_user_levels(
        self, player_id: int, page: int = 0
    ) -> list[LevelDisplay]:
        """
        Get an user's levels by player ID.

        :param player_id: The player ID to retrieve the levels.
        :type player_id: int
        :param page: The page number to load, default is 0.
        :type page: int
        :return: A list of LevelDisplay instances.
        :rtype: list[:class:`gd.entities.level.LevelDisplay`]
        """

        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJLevels21.php",
            data={"secret": SECRET, "type": 5, "page": page, "str": player_id},
        )
        response = response.text

        check_errors(response, InvalidID, f"Invalid account ID {player_id}.")

        if not response.split("#")[0]:
            return None

        return [
            LevelDisplay.from_raw(level_data).add_client(self)
            for level_data in response.split("#")[0].split("|")
        ]

    async def map_packs(self, page: int = 0) -> list[MapPack]:
        """
        Get the full list of map packs available (in a specific page).

        :param page: The page number to load, default is 0.
        :type page: int
        :raises: gd.LoadError
        :return: A list of `MapPack` instances.
        :rtype: list[:class:`gd.entities.level.MapPack`]
        """
        if page < 0:
            raise ValueError("Page must be a non-negative number.")

        if page > 6:
            raise ValueError("Page limit is 6.")

        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJMapPacks21.php",
            data={"secret": SECRET, "page": page},
        )
        response = response.text

        check_errors(response, LoadError, "An error occurred when getting map packs.")
        map_packs = response.split("#")[0].split("|")
        return [
            MapPack.from_raw(map_pack_data).add_client(self)
            for map_pack_data in map_packs
        ]

    async def gauntlets(self, ncs: bool = True) -> list[Gauntlet]:
        """
        Get the list of gauntlets objects.

        :param ncs: Whether to include NCS gauntlets to the list. Defaults to True.
        :type ncs: bool
        :raises: gd.LoadError
        :return: A list of `Gauntlet` instances.
        :rtype: list[:class:`gd.entities.level.Gauntlet`]
        """
        data = {"secret": SECRET}
        if ncs:
            data["binaryVersion"] = 46

        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJGauntlets21.php", data=data
        )
        response = response.text

        check_errors(response, LoadError, "An error occurred when getting gauntlets.")
        guantlets = response.split("#")[0].split("|")
        list_guantlets = [
            Gauntlet.from_raw(guantlet).add_client(self) for guantlet in guantlets
        ]

        return list_guantlets

    async def search_list(
        self,
        query: str = None,
        src_filter: SearchFilter = 0,
        page: int = 0,
        difficulty: list[Difficulty] = None,
        demon_difficulty: DemonDifficulty = None,
        only_rated: bool = False,
    ) -> list[LevelList]:
        """
        Search for lists.

        :param query: The query string to search for.
        :type query: str
        :param filter: Filter type (recent, magic, ...)
        :type filter: SearchFilter
        :param page: Page number (starting with 0)
        :type page: int
        :param difficulty: Filters by a specific difficulty.
        :type difficulty: list[Difficulty]
        :param demon_difficulty: Filters by a specific demon difficulty.
        :type demon_difficulty: DemonDifficulty
        :param only_rated: Filters only rated lists.
        :type only_rated: bool
        :raises: gd.LoadError
        :return: A list of `LevelList` instances.
        :rtype: list[:class:`gd.entities.level.LevelList`]
        """
        if src_filter == SearchFilter.FRIENDS and not self.account:
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
        response = response.text

        check_errors(
            response,
            LoadError,
            "An error occurred while searching lists, maybe it doesn't exist?",
        )
        response = response.split("#")[0]

        return [
            LevelList.from_raw(level_list_data).add_client(self)
            for level_list_data in response.split("|")
        ]

    async def leaderboard(
        self, leaderboard: Leaderboard = Leaderboard.TOP, count: int = 100
    ) -> list[Player]:
        """
        Get the leaderboard for the given type.

        :param leaderboard: The type of leaderboard to retrieve.
        :type leaderboard: Leaderboard
        :param count: The number of players to retrieve, limits to 100.
        :raises: gd.LoadError, ValueError
        :return: A list of `Player` instances.
        :rtype: list[Player]
        """
        if count < 1 or count > 100:
            raise ValueError("Count must be between 1 and 100.")

        if (
            leaderboard in (Leaderboard.FRIENDS, Leaderboard.RELATIVE)
            and not self.logged_in
        ):
            raise ValueError(
                "Only friends or relative leaderboards is available when logged in."
            )

        data = {
            "secret": SECRET,
            "type": leaderboard,
            "count": count,
            "accountID": self.account.account_id if self.logged_in else None,
            "gjp2": self.account.gjp2 if self.logged_in else None,
        }

        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJScores20.php",
            data=data,
        )

        check_errors(
            response, LoadError, "An error occurred when getting the leaderboard."
        )

        response = response.text.split("#")[0].split("|")
        del response[-1]

        return [Player.from_raw(player).add_client(self) for player in response]

    async def leaderboard_top_1000(
        self, html: bool = False
    ) -> Union[str, list[Player]]:
        """
        Gets the top 1000 star grinders.

        :param html: Gets the raw html from the servers.
        :type html: bool
        :return: The raw HTML as string or a list of Players
        :rtype: Union[str, list[Player]]
        """
        response = await send_get_request(
            url="http://www.boomlings.com/database/accounts/getTop1000.php"
        )
        response = response.text

        if html:
            return response

        table = response.split("<table>")[1].split("</table>")[0]
        table = (
            table.replace("<tr>", "")
            .replace("</tr>", "|")
            .replace("<td>", "")
            .replace("</td>", ",")
        )
        rows = table.split("|")[1:]
        players = [row.split(",") for row in rows if row]

        return [
            Player(
                rank=int(player[0]),
                account_id=int(player[1]),
                name=player[2],
                stars=int(player[3]),
                demons=int(player[4]),
                user_coins=int(player[5]),
                secret_coins=int(player[6]),
            ).add_client(self)
            for player in players
        ]

    async def like(
        self, item_id: int, like_type: int, dislike: bool = False, special: int = 0
    ) -> None:
        """
        Liking a level/list/comment/post.

        **NOTE: This is a helper function, please use the individual liking methods instead.**

        :param item_id: ID of the item.
        :type item_id: int
        :param like_type: 1 for level, 2 for comment, 3 for post, 4 for list
        :type like_type: int
        :param dislike: Whether to dislike or not
        :type dislike: bool
        :param special: For type 2, put level ID. For type 3, put post ID. For type 1 and 4, put 0.
        :type special: int
        :return: None
        :rtype: None
        """
        data = {
            "itemID": item_id,
            "type": like_type,
            "like": int(not dislike),
            "accountID": self.account.account_id,
            "udid": "0",
            "uuid": self.account.player_id,
            "gjp2": self.account.gjp2,
            "special": special,
            "secret": SECRET,
            "rs": generate_rs(),
            "gameVersion": 22,
            "binaryVersion": 42,
        }

        data["chk"] = generate_chk(
            values=[
                data["special"],
                data["itemID"],
                data["like"],
                data["type"],
                data["rs"],
                data["accountID"],
                data["udid"],
                data["uuid"],
            ],
            key=XorKey.LIKE,
            salt=Salt.LIKE,
        )

        await send_post_request(
            url="http://www.boomlings.com/database/likeGJItem211.php", data=data
        )

    @require_login("An account is required to perform this action.")
    async def like_level(self, level_id: int, dislike: bool = False) -> None:
        """
        Like or dislike a level.

        :param level_id: The ID of the level to like or dislike.
        :type level_id: int
        :param dislike: Whether to dislike the level. Defaults to False.
        :return: None
        :rtype: None
        """
        await self.like(level_id, 1, dislike)

    @require_login("An account is required to perform this action.")
    async def like_list(self, list_id: int, dislike: bool = False) -> None:
        """
        Like or dislike a list.

        :param list_id: The ID of the list to like or dislike.
        :type list_id: int
        :param dislike: Whether to dislike the level. Defaults to False.
        :return: None
        :rtype: None
        """
        await self.like(list_id, 4, dislike)

    @require_login("An account is required to perform this action.")
    async def like_comment(
        self, comment_id: int, level_id: int, dislike: bool = False
    ) -> None:
        """
        Like or dislike a comment in a level or list.

        :param comment_id: The ID of the comment to like or dislike.
        :type comment_id: int
        :param level_id: The ID of the level the comment belongs to. (Use negative ID for lists)
        :type level_id: int
        :param dislike: Whether to dislike the comment. Defaults to False.
        :type dislike: bool
        :return: None
        :rtype: None
        """
        await self.like(comment_id, 2, dislike, level_id)

    @require_login("An account is required to perform this action.")
    async def like_post(self, post_id: int, dislike: bool = False) -> None:
        """
        Like or dislike an account post.

        :param post_id: The ID of the post to like or dislike.
        :type post_id: int
        :param dislike: Whether to dislike the comment. Defaults to False.
        :type dislike: bool
        :return: None
        :rtype: None
        """
        await self.like(post_id, 3, dislike, post_id)

    @require_login("An account is required to view quests.")
    async def quests(self) -> list[Quest]:
        """
        Get the current quests of the account.

        :return: A list of quests.
        :rtype: list[Quest]
        """
        data = {
            "secret": SECRET,
            "accountID": self.account.account_id,
            "gjp2": self.account.gjp2,
            "chk": generate_digits(),
            "udid": self.udid,
            "uuid": self.account.player_id,
            "gameVersion": 22,
            "binaryVersion": 42,
            "world": 0,
        }

        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJChallenges.php", data=data
        )
        response = response.text
        check_errors(response, LoadError, "")

        response = cyclic_xor(
            base64_urlsafe_decode(response.split("|")[0][5:]), XorKey.QUEST
        ).split(":")

        time_left = response[5]
        quests = (quest.split(",") for quest in response[6:9])
        reward_type_map = {
            "1": Item.ORBS,
            "2": Item.STARS,
            "3": Item.COIN,
        }

        return [
            Quest(
                name=quest[4],
                requirement_type=reward_type_map[quest[1]],
                requirement_value=int(quest[2]),
                reward=int(quest[3]),
                time_left=int(time_left),
            )
            for quest in quests
        ]

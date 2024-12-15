__doc__ = """Accessing the Geometry Dash API programmatically."""

from datetime import timedelta
from typing import Union, Optional, Literal
import random
import base64

from gd.parse import (
    parse_comma_separated_int_list,
    determine_search_difficulty,
    parse_search_results,
    determine_demon_search_difficulty,
)
from gd.errors import (
    check_errors,
    LoadError,
    InvalidID,
    LoginError,
)
from gd.cryptography import (
    Salt,
    XorKey,
    gjp2,
    generate_chk,
    generate_rs,
    generate_digits,
    cyclic_xor,
    base64_urlsafe_decode,
    generate_udid,
    base64_urlsafe_decompress,
)
from gd.entities.enums import (
    Length,
    LevelRating,
    SearchFilter,
    DemonDifficulty,
    Difficulty,
    SpecialLevel,
    ChestType,
    Leaderboard,
    Item,
)
from gd.entities.level import Level, LevelDisplay, Comment, MapPack, LevelList, Gauntlet
from gd.entities.song import MusicLibrary, SoundEffectLibrary, Song
from gd.entities.user import Account, Player, AccountComment, Quest, Chest
from gd.helpers import send_get_request, send_post_request, require_login
from gd.type_hints import (
    PlayerId,
    AccountId,
    LevelId,
    ListId,
    AccountCommentId,
    CommentId,
    SongId,
    LevelOrListId,
    Udid,
)

SECRET = "Wmfd2893gb7"
LOGIN_SECRET = "Wmfv3899gc9"
QUEST_ITEM_TYPE_MAP = {
    "1": Item.ORBS,
    "2": Item.STARS,
    "3": Item.USERCOIN,
}


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
    account : Optional[Account]
        The account associated with this client.
    udid : Udid
        The UDID associated with this client. (Generated randomly if left out)
    """

    account: Optional[Account] = None
    """The account associated with this client."""
    udid: Udid = None
    """The UDID of the client"""

    def __init__(
        self,
        account: Optional[Account] = None,
        udid: Udid = None,
    ) -> None:
        self.account = account
        self.udid = udid

        if self.udid is None:
            self.udid = generate_udid()

    def __repr__(self) -> str:
        return f"<gd.Client account={self.account} at {hex(id(self))}>"

    @property
    def logged_in(self) -> bool:
        """If the client has logged in or not."""
        return bool(self.account)

    @logged_in.setter
    def logged_in(self) -> None:
        raise ValueError("This property is frozen.")

    @require_login()
    async def check_login(self) -> bool:
        """
        Checks if the account credientials are correct.

        :raises: LoginError
        :return: True if the credentials are correct, False otherwise.
        :rtype: bool
        """

        data = {
            "secret": LOGIN_SECRET,
            "userName": self.account.name,
            "gjp2": self.account.gjp2,
            "udid": self.udid,
        }

        response = await send_post_request(
            url="http://www.boomlings.com/database/accounts/loginGJAccount.php",
            data=data,
        )
        response = response.text

        return response == f"{self.account.account_id}|{self.account.player_id}"

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
            "udid": self.udid,
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
        self, name: str, password: str, account_id: AccountId, player_id: PlayerId
    ) -> Account:
        """
        Login account with given name and password without any additional checks.

        :param name: The account name.
        :type name: str
        :param password: The account password.
        :type password: str
        :param account_id: The account ID.
        :type account_id: AccountId
        :param player_id: The player ID.
        :type player_id: PlayerId

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

    @require_login("You need to login before you can send an account comment!")
    async def send_account_comment(self, message: str) -> AccountCommentId:
        """
        Sends an account comment to the account logged in.

        :param message: The message to send.
        :type message: str
        :raises: gd.LoadError
        :return: The post ID of the sent post.
        :rtype: AccountCommentId
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

    @require_login("You need to login before you can comment!")
    async def send_comment(
        self, message: str, level_id: LevelOrListId, percentage: int = 0
    ) -> CommentId:
        """
        Sends a comment to a level or list.

        For lists, use a **negative ID.**

        :param message: The message to send.
        :type message: str
        :param level_id: The ID of the level/list to comment on.
        :type level_id: LevelOrListId
        :param percentage: The percentage of the level completed, optional. Defaults to 0.
        :type percentage: int
        :raises: gd.InvalidID
        :return: The comment ID of the sent comment.
        :rtype: CommentId
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
    async def delete_account_comment(self, comment_id: AccountCommentId) -> None:
        """
        Deletes an account comment using comment ID.

        :param comment_id: The ID of the post to delete.
        :type comment_id: AccountCommentId
        :raises: gd.InvalidID
        :return: None
        :rtype: None
        """
        response = send_post_request(
            url="http://www.boomlings.com/database/deleteGJAccComment20.php",
            data={
                "accountID": self.account.account_id,
                "commentID": comment_id,
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
    async def delete_comment(
        self, comment_id: CommentId, level_id: LevelOrListId
    ) -> None:
        """
        Deletes a comment using the comment's ID and level ID.

        For lists, use a negative ID.

        :param comment_id: The ID of the comment to delete.
        :type comment_id: CommentId
        :param level_id: The ID of the level the comment belongs to.
        :type level_id: LevelOrListId
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

    async def download_level(self, level_id: Union[LevelId, SpecialLevel]) -> Level:
        """
        Downloads a specific level from the Geometry Dash servers using the provided ID.

        :param id: The ID of the level.
        :type id: Union[LevelId, SpecialLevel]
        :raises: gd.InvalidID
        :return: A `Level` instance containing the downloaded level data.
        :rtype: :class:`gd.entities.Level`
        """

        response = await send_post_request(
            url="http://www.boomlings.com/database/downloadGJLevel22.php",
            data={"levelID": level_id, "secret": SECRET},
        )
        response = response.text

        # Check if response is valid
        check_errors(response, InvalidID, f"Invalid level ID {level_id}.")

        return Level.from_raw(response).attach_client(self)

    async def special_level_data(self, special: SpecialLevel) -> tuple[timedelta, int]:
        """
        Gets the time left and level index for the next level in daily or weekly.

        **Index information:**

        Daily index = index

        Weekly index = index + 100000

        :param special: The special level to get (e.g., daily or weekly).
        :type special: SpecialLevel
        :raises: gd.LoadError
        :return: A `Level` instance containing the downloaded level data.
        :rtype: :class:`gd.entities.Level`
        """
        if special == "DAILY":
            special = 0
        elif special == "WEEKLY":
            special = 1
        else:
            raise ValueError("Invalid special level. (Event is not allowed)")

        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJDailyLevel.php",
            data={"secret": SECRET, "type": special},
        )

        response = response.text
        check_errors(response, LoadError, "Unable to get special level data.")
        response = response.split("|")

        return (
            timedelta(seconds=int(response[1])),
            int(response[0]),
        )

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

        check_errors(search_data, LoadError, "Unable to get search results.")
        parsed_results = parse_search_results(search_data)

        return [
            LevelDisplay.from_parsed(result).attach_client(self)
            for result in parsed_results
        ]

    @require_login("You need to log in before you can view the leaderboard.")
    async def level_leaderboard(
        self,
        level_id: LevelId,
        leaderboard_type: Literal["TOP", "FRIENDS", "WEEKLY"] = "TOP",
    ) -> list[Player]:
        """
        Gets the leaderboard for a given level.

        :param level_id: The ID of the level.
        :type level_id: LevelId
        :param leaderboard_type: Get TOP, FRIENDS or WEEKLY.
        :type leaderboard_type: Literal["TOP", "FRIENDS", "WEEKLY"]
        :return: A list of Player instances representing the leaderboard.
        :rtype: list[:class:`gd.entities.Player`]
        """
        if leaderboard_type == "FRIENDS":
            leaderboard = 0
        elif leaderboard_type == "TOP":
            leaderboard = 1
        elif leaderboard_type == "WEEKLY":
            leaderboard = 2
        else:
            raise ValueError("leaderboard_type must be 'FRIENDS', 'TOP' or 'WEEKLY'.")

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
            "Unable to get level leaderboard.",
        )

        response = response.text.split("#")[0].split("|")

        return [
            Player.from_raw(player_data, parse_leaderboard_score=True).attach_client(
                self
            )
            for player_data in response
        ]

    @require_login("You need to log in before you can view the leaderboard.")
    async def platformer_level_leaderboard(
        self,
        level_id: LevelId,
        leaderboard_type: Literal["TOP", "FRIENDS", "WEEKLY"] = "TOP",
        mode: Literal["TIME", "POINTS"] = "TIME",
    ) -> list[Player]:
        """
        Gets the leaderboard for a given level.

        :param level_id: The ID of the level.
        :type level_id: LevelId
        :param friends: Whether to include get friends' scores in the leaderboard. Defaults to False.
        :return: A list of Player instances representing the leaderboard.
        :rtype: list[:class:`gd.entities.Player`]
        """
        if leaderboard_type == "FRIENDS":
            leaderboard = 0
        elif leaderboard_type == "TOP":
            leaderboard = 1
        elif leaderboard_type == "WEEKLY":
            leaderboard = 2
        else:
            raise ValueError("leaderboard_type must be 'FRIENDS', 'TOP' or 'WEEKLY'.")

        if mode == "TIME":
            mode = 0
        elif mode == "POINTS":
            mode = 1
        else:
            raise ValueError("mode must be 'TIME' or 'POINTS'.")

        data = {
            "secret": SECRET,
            "type": leaderboard,
            "levelID": level_id,
            "accountID": self.account.account_id,
            "gjp2": self.account.gjp2,
            "plat": 1,
            "mode": mode,
        }

        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJLevelScoresPlat.php", data=data
        )

        check_errors(
            response,
            LoadError,
            "Unable to get platformer level leaderboard.",
        )

        response = response.text.split("#")[0].split("|")

        return [
            Player.from_raw(player_data, parse_leaderboard_score=True).attach_client(
                self
            )
            for player_data in response
        ]

    async def music_library(self) -> MusicLibrary:
        """
        Gets the current music library in RobTop's servers.

        :return: A `MusicLibrary` instance containing all the music library data.
        :rtype: :class:`gd.entities.song.MusicLibrary`
        """
        response = await send_get_request(
            url="https://geometrydashfiles.b-cdn.net/music/musiclibrary_02.dat",
        )
        response = response.content.decode()

        music_library = base64_urlsafe_decompress(response)
        return MusicLibrary.from_raw(music_library)

    async def sfx_library(self) -> SoundEffectLibrary:
        """
        Gets the current Sound Effect library in RobTop's servers.

        :return: A `SoundEffectLibrary` instance containing all the SFX library data.
        :rtype: :class:`gd.entities.song.SoundEffectLibrary`
        """
        response = await send_get_request(
            url="https://geometrydashfiles.b-cdn.net/sfx/sfxlibrary.dat",
        )
        response = response.content.decode()

        sfx_library = base64_urlsafe_decompress(response)
        return SoundEffectLibrary.from_raw(sfx_library)

    async def get_song(self, song_id: SongId) -> Song:
        """
        Gets song by ID, either from Newgrounds or the music library.

        :param id: The ID of the song.
        :type id: SongId
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

    async def search_user(
        self, query: Union[str, AccountId], use_id: bool = False
    ) -> Player:
        """
        Get an user profile by account ID or name.

        :param query: The account ID/name to retrieve the profile.
        :type query: Union[str, AccountId]
        :param use_id: If searches the user using the account ID.
        :type use_id: bool
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
        return Player.from_raw(response.split("#")[0]).attach_client(self)

    async def get_comments(
        self, level_id: LevelOrListId, page: int = 0
    ) -> list[Comment]:
        """
        Get comments by level/list ID.

        For lists, use a negative ID.

        :param level_id: The ID of the level/list.
        :type level_id: LevelOrListId
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
            Comment.from_raw(comment_data).attach_client(self)
            for comment_data in response.split("|")
        ]

    async def get_user_account_comments(
        self, account_id: AccountId, page: int = 0
    ) -> Optional[list[AccountComment]]:
        """
        Get an user's account comments by Account ID.

        :param account_id: The account ID to retrieve the account comments.
        :type account_id: AccountId
        :param page: The page number for pagination. Defaults to 0.
        :type page: int
        :raises: gd.InvalidID
        :return: A list of `AccountComment` instances or None if there are no account comments.
        :rtype: list[:class:`gd.entities.user.AccountComment`]
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
            posts_list.append(
                AccountComment.from_raw(post, account_id).attach_client(self)
            )

        return posts_list

    async def get_user_comments(
        self, player_id: PlayerId, page: int = 0, display_most_liked: bool = False
    ) -> list[Comment]:
        """
        Get an user's comments history by player ID.

        :param player_id: The player ID to retrieve the comments history.
        :type player_id: PlayerId
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
            Comment.from_raw(comment_data).attach_client(self)
            for comment_data in response.split("#")[0].split("|")
        ]

    async def get_user_levels(
        self, player_id: PlayerId, page: int = 0
    ) -> list[LevelDisplay]:
        """
        Get an user's levels by player ID.

        :param player_id: The player ID to retrieve the levels.
        :type player_id: PlayerId
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
            LevelDisplay.from_raw(level_data).attach_client(self)
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
            MapPack.from_raw(map_pack_data).attach_client(self)
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
            Gauntlet.from_raw(guantlet).attach_client(self) for guantlet in guantlets
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
            LevelList.from_raw(level_list_data).attach_client(self)
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

        return [Player.from_raw(player).attach_client(self) for player in response]

    async def leaderboard_top_1000(
        self, html: bool = False
    ) -> Union[str, list[Player]]:
        """
        Gets the top 1000 star grinders.

        :param html: Gets the raw html returned instead of a Python list.
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
            ).attach_client(self)
            for player in players
        ]

    async def like(
        self,
        item_id: Union[LevelId, CommentId, AccountCommentId, ListId],
        like_type: int,
        dislike: bool = False,
        special_id: Union[LevelId, AccountCommentId, int] = 0,
    ) -> None:
        """
        Liking a level/comment/post/list.

        **NOTE: This is a helper method, please use the individual liking methods instead.**

        :param item_id: ID of the level/comment/post/list.
        :type item_id: Union[LevelId, CommentId, AccountCommentId, ListId]
        :param like_type: 1 for level, 2 for comment, 3 for post, 4 for list.
        :type like_type: int
        :param dislike: Whether to dislike or not
        :type dislike: bool
        :param special: For type 2, put level ID. For type 3, put post ID. For type 1 and 4, put 0.
        :type special: Union[LevelId, AccountCommentId, int]
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
            "special": special_id,
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
    async def like_level(self, level_id: LevelId, dislike: bool = False) -> None:
        """
        Like or dislike a level.

        :param level_id: The ID of the level to like or dislike.
        :type level_id: LevelId
        :param dislike: Whether to dislike the level. Defaults to False.
        :return: None
        :rtype: None
        """
        await self.like(level_id, 1, dislike)

    @require_login("An account is required to perform this action.")
    async def like_list(self, list_id: ListId, dislike: bool = False) -> None:
        """
        Like or dislike a list.

        :param list_id: The ID of the list to like or dislike.
        :type list_id: ListId
        :param dislike: Whether to dislike the level. Defaults to False.
        :return: None
        :rtype: None
        """
        await self.like(list_id, 4, dislike)

    @require_login("An account is required to perform this action.")
    async def like_comment(
        self, comment_id: CommentId, level_id: LevelId, dislike: bool = False
    ) -> None:
        """
        Like or dislike a comment in a level or list.

        :param comment_id: The ID of the comment to like or dislike.
        :type comment_id: CommentId
        :param level_id: The ID of the level the comment belongs to. (Use negative ID for lists)
        :type level_id: LevelId
        :param dislike: Whether to dislike the comment. Defaults to False.
        :type dislike: bool
        :return: None
        :rtype: None
        """
        await self.like(comment_id, 2, dislike, level_id)

    @require_login("An account is required to perform this action.")
    async def like_post(self, post_id: AccountCommentId, dislike: bool = False) -> None:
        """
        Like or dislike an account post.

        :param post_id: The ID of the post to like or dislike.
        :type post_id: AccountCommentId
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

        # Cryptography shit, removes salt and cyclic XOR them.
        response = cyclic_xor(
            base64_urlsafe_decode(response.split("|")[0][5:]), XorKey.QUEST
        ).split(":")

        time_left = response[5]
        quests = (quest.split(",") for quest in response[6:9])

        return [
            Quest(
                name=quest[4],
                requirement_type=QUEST_ITEM_TYPE_MAP[quest[1]],
                requirement_value=int(quest[2]),
                diamonds_reward=int(quest[3]),
                time_left=int(time_left),
            )
            for quest in quests
        ]

    @require_login("An account is required to view chests.")
    async def chests(self, open_chest: Optional[ChestType] = None) -> list[Chest]:
        """
        Gets the data of the chests last opened.

        When opened using open_chest, it will give the new data.

        :param open_chest: Opens a small chest or large chest or view the details only.
        :type open_chest: Optional[ChestType]
        :return: A list of chest objects, the first one is small chest and second one is large chest.
        :rtype: list[Chest]
        """
        if open_chest is None:
            open_chest = 0
        elif open_chest == "SMALL":
            open_chest = 1
        elif open_chest == "LARGE":
            open_chest = 2
        else:
            raise ValueError(
                "Invalid chest type. Use None, 'SMALL' or 'LARGE' instead."
            )

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
            "r1": random.randint(100, 99999),
            "r2": random.randint(100, 99999),
            "rewardType": open_chest,
        }

        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJRewards.php", data=data
        )
        response = response.text
        check_errors(response, LoadError, "")

        # Cryptography shit, removes salt and cyclic XOR them.
        response = cyclic_xor(
            base64_urlsafe_decode(response.split("|")[0][5:]), XorKey.CHEST
        ).split(":")

        small_chest_time = int(response[5])
        small_chest = response[6].split(",")
        small_chest_open = int(response[7])
        large_chest_time = int(response[8])
        large_chest = response[9].split(",")
        large_chest_open = int(response[10])

        return [
            Chest(
                orbs=int(small_chest[0]),
                diamonds=int(small_chest[1]),
                extras=[
                    Item.from_extra_id(int(small_chest[2])),
                    Item.from_extra_id(int(small_chest[3])),
                ],
                time_left=small_chest_time,
                times_opened=small_chest_open,
            ),
            Chest(
                orbs=int(large_chest[0]),
                diamonds=int(large_chest[1]),
                extras=[
                    Item.from_extra_id(int(large_chest[2])),
                    Item.from_extra_id(int(large_chest[3])),
                ],
                time_left=large_chest_time,
                times_opened=large_chest_open,
            ),
        ]

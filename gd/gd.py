from .helpers import *
from .models.level import *
from .models.song import *
from .models.users import *
from datetime import timedelta
from typing import Union, Tuple
from asyncio import run

_secret = "Wmfd2893gb7"

class Client:
    """
    Client for interacting with the Geometry Dash servers.

    It contains all methods to interact with the Geometry Dash API.
    """
    def __init__(self) -> None:
        pass

    async def download_level(self, id: int) -> DownloadedLevel:
        """
        Downloads a specific level from the Geometry Dash servers using the provided ID.
        
        :param id: The ID of the level.
        :type id: int
        :return: A `DownloadedLevel` instance containing the downloaded level data.
        """
        if not isinstance(id, int):
            raise ValueError("ID must be an int.")

        try:
            response = await send_post_request(
                url="http://www.boomlings.com/database/downloadGJLevel22.php", 
                data={"levelID": id, "secret": _secret}
            )
            return DownloadedLevel.from_raw(response)
        except RuntimeError as e:
            raise RuntimeError(f"Failed to download level: {e}")

    async def download_daily_level(self, return_weekly: bool = False, get_time_left: bool = False) -> Union[DownloadedLevel, Tuple[DownloadedLevel, timedelta]]:
        """
        Downloads the daily or weekly level from the Geometry Dash servers. You can return the time left for the level optionally.

        :param return_weekly: Whether to return the weekly or daily level. Defaults to False for daily.
        :type return_weekly: bool
        :param get_time_left: Whether to return the time left for the level. Defaults to False.
        :type get_time_left: bool
        :return: A `DownloadedLevel` instance containing the downloaded level data.

            If `get_time_left` is set to True then returns a tuple containing the `DownloadedLevel` and the time left for the level.
        """
        try:
            level = await self.download_level(-2 if return_weekly else -1)
            
            if get_time_left:
                daily_data: str = await send_post_request(
                    url="http://www.boomlings.com/database/getGJDailyLevel.php", 
                    data={"secret": _secret, "weekly": "1" if return_weekly else "0"}
                )
                daily_data = daily_data.split("|")
                return level, timedelta(seconds=int(daily_data[1]))
            
            return level
        except RuntimeError as e:
            raise RuntimeError(f"Failed to get daily level: {e}")

    async def search_level(self, query: str, type: int = 0) -> List[SearchedLevel]:
        """
        Searches for levels matching the given query string.

        Filters will be added in the next version.

        :param query: The query for the search.
        :type query: str
        :return: A list of `SearchedLevel` instances.
        """
        search_data: str = await send_post_request(
            url="http://www.boomlings.com/database/getGJLevels21.php", 
            data={"secret": _secret, "str": query, "type": type}
        )
        parsed_results = parse_search_results(search_data)
        return [SearchedLevel.from_dict(result) for result in parsed_results]

    async def get_music_library(self) -> MusicLibrary:
        """
        Gets the current music library in RobTop's servers.

        :return: A `MusicLibrary` instance containing all the music library data.
        """
        response = await send_get_request(
            url="https://geometrydashfiles.b-cdn.net/music/musiclibrary_02.dat",
        )
        music_library_encoded = response.content
        music_library = decrypt_data(music_library_encoded, "base64_decompress")
        return MusicLibrary.from_raw(music_library)
    
    async def get_sfx_library(self) -> SFXLibrary:
        """
        Gets the current SFX library in RobTop's servers.

        :return: A `SFXLibrary` instance containing all the SFX library data.
        """
        response = await send_get_request(
            url="https://geometrydashfiles.b-cdn.net/sfx/sfxlibrary.dat",
        )
        music_library_encoded = response.content
        music_library = decrypt_data(music_library_encoded, "base64_decompress")
        return SFXLibrary.from_raw(music_library)

    async def get_song(self, id: int) -> LevelSong:
        """
        Gets song data by ID, either from Newgrounds or the music library.

        :param id: The ID of the song. (Use ID larger than 10000000 to get the song from the library.)
        :type id: int
        :return: A `LevelSong` instance containing the song data.
        """
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJSongInfo.php",
            data={'secret': _secret, "songID": id}
        )
        return LevelSong.from_raw(response)

    async def get_user_profile(self, account_id: int) -> UserProfile:
        """
        Get an user profile by account ID.

        :param account_id: The account ID to retrieve the profile.
        :type account_id: int
        :return: A `UserProfile` instance containing the user's profile data.
        """
        if isinstance(account_id, int):
            url = "http://www.boomlings.com/database/getGJUserInfo20.php"
            data = {'secret': _secret, "targetAccountID": account_id}
        else:
            raise ValueError("ID must be int")

        response = await send_post_request(url=url, data=data)
        return UserProfile.from_raw(response)

    async def search_user(self, username: str) -> UserProfile:
        """
        Search for an user by their username. 
        
        **Note:** This method doesn't return the full information, use `UserProfile.reload()` to get the full profile after retrieving.

        :param username: The username to search for.
        :type username: str
        :return: A `UserProfile` instance containing the user's profile data.
        """
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJUsers20.php",
            data={'secret': _secret, "str": username}
        )
        return UserProfile.from_raw(response)
    
    async def get_level_comments(self, level_id: int, page: int = 0) -> List[LevelComment]:
        """
        Get level's comments by level ID.

        :param level_id: The ID of the level.
        :type level_id: int
        :param page: The page number for pagination. Defaults to 0.
        :type page: int
        :return: A list of `LevelComment` instances.
        """
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJComments21.php",
            data={'secret': _secret, "levelID": level_id, "page": page}
        )
        return [LevelComment.from_raw(comment_data) for comment_data in response.split("|")]
    
    async def get_user_posts(self, account_id: int, page: int = 0) -> List[ProfilePost] | None:
        """
        Get an user's posts by Account ID

        :param account_id: The account ID to retrieve the posts.
        :type account_id: int
        :param page: The page number for pagination. Defaults to 0.
        :type page: int
        :return: A list of `ProfilePost` instances or None if there are no posts.
        """
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJAccountComments20.php",
            data={'secret': _secret, "accountID": account_id, "page": page}
        )

        if response:
            posts_list = []
            parsed_res = response.split("|")
            for post in parsed_res:
                posts_list.append(ProfilePost.from_raw(post, account_id))
            return posts_list
        
    async def get_user_comments_history(self, player_id: int, page: int = 0, display_most_liked: bool = False) -> List[LevelComment]:
        """
        Get an user's comments history.
        
        :param player_id: The player ID to retrieve the comments history.
        :type player_id: int
        :param page: The page number for pagination. Defaults to 0.
        :type page: int
        :param display_most_liked: Whether to display the most liked comments. Defaults to False.
        :type display_most_liked: bool
        :return: A list of `LevelComment` instances.
        """
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJCommentHistory.php",
            data={'secret': _secret, "userID": player_id, "page": page, "mode": int(display_most_liked)}
        )
        return [LevelComment.from_raw(comment_data) for comment_data in response.split("|")]

    async def get_map_packs(self, page: int = 0) -> List[MapPack]:
        """
        Get the full list of map packs available (in a specific page).

        :return: A list of `MapPack` instances.
        """
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJMapPacks21.php",
            data={'secret': _secret, 'page': page}
        )
        
        map_packs = response.split('#')[0].split("|")
        return [MapPack.from_raw(map_pack_data) for map_pack_data in map_packs]

    async def get_gauntlets(self, only_2_point_1: bool = True) -> List[Gauntlet]:
        """
        Get the list of gauntlets objects.

        :param only_2_point_1: Whether to get ONLY the 2.1 guantlets or both 2.2 and 2.1. Defaults to True.
        :type: bool
        :return: A list of `Gauntlet` instances.
        """
        response = await send_post_request(
            url="http://www.boomlings.com/database/getGJGauntlets21.php",
            data={'secret': _secret, 'special': int(only_2_point_1)}
        )
        
        guantlets = response.split('#')[0].split("|")
        return [Gauntlet.from_raw(guantlet) for guantlet in guantlets]

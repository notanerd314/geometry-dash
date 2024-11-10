__doc__ = """
# gd.exceptions

A module containing all exceptions and error-related functions.
"""

class InvalidSongID(Exception):
    """Raised when an invalid song ID is provided."""


class SearchLevelError(Exception):
    """Raised when searching results in nothing or an error."""

class SearchListError(Exception):
    """Raised when searching for a level list fails."""

class InvalidLevelID(Exception):
    """Raised when an invalid level ID is provided."""

class DownloadSongError(Exception):
    """Raised when downloading a song fails."""

class InvalidAccountID(Exception):
    """Raised when an invalid account ID is provided."""


class InvalidAccountName(Exception):
    """Raised when an invalid account name is provided."""

class LoadError(Exception):
    """Raised when a something fails to load."""

class ResponseError(Exception):
    """Raised when a request fails."""

class ParseError(Exception):
    """Raised when parsing a response fails."""

class LoginError(Exception):
    """Raised when logging in fails."""

class NotLoggedInError(Exception):
    """Raised when the client is trying to do an action that needs an account."""

class CommentError(Exception):
    """Raised when commenting fails."""

class OnCooldown(Exception):
    """Raised when the function is still on cooldown."""

class NoClients(Exception):
    """Raised when the client-required function is used without having clients."""

class DownloadIconError(Exception):
    """Raised when downloading/rendering an icon fails."""


def check_errors(data: str, exception: Exception, text: str) -> None:
    """
    Checks the response status.

    :param data: The response data
    :type data: str
    :param exception: The exception to raise when the response status is -1
    :type exception: Exception
    :param text: The error message to display when the response status is -1
    :type text: str
    """
    if data == "-1":
        raise exception(text)

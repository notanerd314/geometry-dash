from typing import AnyStr

class InvalidSongID(Exception):
    """Raised when an invalid song ID is provided."""
    pass

class SearchLevelError(Exception):
    """Raised when searching results in nothing or an error."""
    pass

class SearchListError(Exception):
    """Raised when searching for a level list fails."""
    pass

class InvalidLevelID(Exception):
    """Raised when an invalid level ID is provided."""
    pass

class DownloadSongError(Exception):
    """Raised when downloading a song fails."""
    pass

class InvalidAccountID(Exception):
    """Raised when an invalid account ID is provided."""
    pass

class InvalidAccountName(Exception):
    """Raised when an invalid account name is provided."""
    pass

class LoadError(Exception):
    """Raised when a something fails to load."""
    pass

class ResponseError(Exception):
    """Raised when a request fails."""
    pass

class ParseError(Exception):
    """Raised when parsing a response fails."""
    pass

class LoginError(Exception):
    """Raised when logging in fails."""
    pass

class NotLoggedInError(Exception):
    """Raised when the client is trying to do an action that needs an account."""
    pass

class CommentError(Exception):
    pass

def check_errors(data: AnyStr, exception: Exception, text: str) -> None:
    """Helper function to check if the server returns -1 as a response. Raises the exception passed if it is."""
    if data == "-1":
        raise exception(text)
__doc__ = """
# gd.exceptions

A module containing all exceptions and error-related functions.
"""


class NoPremission(Exception):
    """Raised when the user does not have the required permission."""


class InvalidID(Exception):
    """Raised when an invalid ID is provided."""


class LoadError(Exception):
    """Raised when a something fails to load unexpectedly."""


class LoginError(Exception):
    """Raised when the user fails to login."""


class OnCooldown(Exception):
    """Raised when the method is on cooldown."""


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

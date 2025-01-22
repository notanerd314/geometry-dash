__doc__ = """
# gd.helpers

A module containing all helper functions for the module.

You typically don't want to use this module because it has limited documentation and confusing to use.
"""

from functools import wraps
from io import BytesIO
from pathlib import Path

import aiofiles
import httpx

from .errors import LoginError

__all__ = [
    "require_client",
    "require_login",
    "send_post_request",
    "send_get_request",
]


# Decorators for Client, Cooldown, and Login
def require_client(
    error_message: str = "At least one client must be attached in order to use this function.",
    login: bool = False,
):
    """
    A decorator for functions that require a client.

    :param error_message: The error message to display when no clients are attached.
    :type error_message: str
    :rtype: none
    :return: None
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            if not self.client:
                raise ValueError(error_message)

            if login and not self.client.logged_in:
                raise LoginError("The client is not logged in.")

            return await func(self, *args, **kwargs)

        return wrapper

    return decorator


def require_login(message: str = "You need to login before you can use this function!"):
    """
    A decorator for functions that need login.

    :param message: The error message to display if no login is available.
    :type message: str
    :return: The decorated function with login check.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            # If the account does not exist or is None, raise an error
            if not hasattr(self, "account") or not self.account:
                raise LoginError(message)

            return await func(self, *args, **kwargs)

        return wrapper

    return decorator


# * HTTP Helper Functions with httpx
async def send_post_request(**kwargs) -> httpx.Response:
    """
    Sends a POST request using httpx.

    Headers are left blank by default.

    :param **kwargs: The keyword arguments to pass to the httpx.AsyncClient.post method.
    :return: The full response object.
    :rtype: httpx.Response
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(**kwargs, headers={"User-Agent": ""})
        return response


async def send_get_request(**kwargs) -> httpx.Response:
    """
    Sends a GET request using httpx.

    Headers are left blank by default.

    :param **kwargs: The keyword arguments to pass to the httpx.AsyncClient.get method.
    :return: The full response object.
    :rtype: httpx.Response
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(**kwargs, headers={"User-Agent": ""})
        return response


async def write(buffer: BytesIO, path: str) -> None:
    """
    Helper function to write the buffer to the given path.

    :param buffer: The buffer to be written to the file.
    :type buffer: BytesIO
    :param path: The path to which the buffer should be written.
    :type path: str
    :raises FileExistsError: If the file already exists at the specified path.
    :return: None
    :rtype: None
    """
    # Ensure path is a Path object
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    # Write the buffer
    async with aiofiles.open(path, "wb") as file:
        await file.write(buffer.getvalue())

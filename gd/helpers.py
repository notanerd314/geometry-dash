__doc__ = """
# gd.helpers

A module containing all helper functions for the module.

You typically don't want to use this module because it has limited documentation and confusing to use.
"""

from functools import wraps
from time import time
from typing import Union
from io import BytesIO
from pathlib import Path

import aiofiles
import httpx

from .errors import OnCooldown, LoginError

MAX_LENGTH = 15
__all__ = [
    "require_client",
    "require_login",
    "cooldown",
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


def cooldown(seconds: Union[int, float]):
    """
    A decorator for applying cooldown to functions for each instance separately.

    :param seconds: The number of seconds to wait between function calls.
    :type seconds: Union[int, float]
    :return: The decorated function with cooldown added per instance.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            # Ensure each instance has its own last_called attribute
            if not hasattr(self, "last_called"):
                self.last_called = {}

            last_called = self.last_called.get(func, 0)
            elapsed = time() - last_called

            if elapsed < seconds:
                raise OnCooldown(
                    f"This function is on cooldown for {seconds - elapsed:.3f}s."
                )

            # Update the last_called time for this function in the instance
            self.last_called[func] = time()
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


async def write(content: BytesIO, path: Union[str, Path]) -> None:
    """
    Helper function to write the content to the given path.

    :param content: The content to be written to the file.
    :type content: BytesIO
    :param path: The path to which the content should be written.
    :type path: Union[str, Path]
    :raises FileExistsError: If the file already exists at the specified path.
    :return: None
    :rtype: None
    """
    # Ensure path is a Path object
    path = Path(path)

    # Check if file exists
    if path.exists():
        raise FileExistsError(f"File already exists at {path}")

    # Ensure the directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write the content
    async with aiofiles.open(path, "wb") as file:
        await file.write(content.getvalue())

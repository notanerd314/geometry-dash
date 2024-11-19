__doc__ = """
# gd.helpers

A module containing all helper functions for the module.

You typically don't want to use this module because it has limited documentation and confusing to use.
"""

from functools import wraps
from time import time
from typing import Union

from colorama import Fore
import httpx

from .exceptions import OnCooldown, LoginError

MAX_LENGTH = 15
__all__ = ["cooldown", "send_post_request", "send_get_request"]


# Decorators for Client, Cooldown, and Login Logic
def deprecated(message: str, version: str):
    """
    A decorator to mark a function as deprecated.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Print the deprecation message
            print(
                f"{Fore.LIGHTYELLOW_EX}DeprecationWarning: {message} (Method will be removed in {version}){Fore.RESET}"
            )
            # Call the original function
            return func(*args, **kwargs)

        return wrapper

    return decorator


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
            # Safely get the client from kwargs or use default logic
            client = kwargs.get("client", None)

            if not self.clients:
                raise ValueError(
                    error_message
                )  # Raise an error if no clients are attached

            # If no client was passed, use the main client index
            if client is None:
                client = self.main_client_index

            # Ensure `client` is a valid instance (in case it's an index)
            if isinstance(client, int):
                if client >= len(self.clients) or client < 0:
                    raise ValueError("Invalid client index.")
                client = self.clients[client]

            # Check if client is logged in (if required)
            if login and not client.logged_in:
                raise LoginError("The client chosen is not logged in.")

            # Update kwargs with the correct client if modified
            kwargs["client"] = client

            # Now call the original async function and await it
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


# HTTP Helper Functions with httpx
async def send_post_request(**kwargs) -> httpx.Response:
    """
    Sends a POST request using httpx.

    :param **kwargs: The keyword arguments to pass to the httpx.AsyncClient.post method.
    :return: The full response object.
    :rtype: httpx.Response
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(**kwargs, headers={"User-Agent": ""})
        return response  # Return the full response object (not just the text)


async def send_get_request(**kwargs) -> httpx.Response:
    """
    Sends a GET request using httpx.

    :param decode: Whether to decode and return the response as a string. Default is True.
    :type decode: bool
    :param **kwargs: The keyword arguments to pass to the httpx.AsyncClient.get method.
    :return: The full response object or decoded string (depending on decode).
    :rtype: Union[str, bytes, httpx.Response]
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(**kwargs)  # Make the GET request
        return response  # Return the full response object if decode is False

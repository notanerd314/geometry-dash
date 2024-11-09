from functools import wraps
from typing import Union
from .exceptions import OnCooldown, LoginError
from time import time
from typing import Callable, Any
from concurrent.futures import ThreadPoolExecutor
import httpx
import asyncio


# Decorators for Client, Cooldown, and Login Logic
def require_client(
    error_message: str = "At least one client must be attached in order to use this function.",
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
            if not self.clients:
                raise ValueError(error_message)
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
            if not hasattr(self, "_last_called"):
                self._last_called = {}

            last_called = self._last_called.get(func, 0)
            elapsed = time() - last_called

            if elapsed < seconds:
                raise OnCooldown(
                    f"This method is on cooldown for {seconds - elapsed:.3f} seconds. Please try again later."
                )

            # Update the last_called time for this function in the instance
            self._last_called[func] = time()
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
async def handle_response(response: httpx.Response) -> httpx.Response:
    """
    Handles HTTP response to ensure no error occurred.
    """
    response.raise_for_status()  # Raises an exception for 4xx/5xx responses
    return response


async def send_post_request(**kwargs) -> str:
    """
    Sends a POST request using httpx.

    :param **kwargs: The keyword arguments to pass to the httpx.AsyncClient.post method.
    :return: The text of the response.
    :rtype: str
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(**kwargs, headers={"User-Agent": ""})
        response_text = await handle_response(response)
        return response_text.text


async def send_get_request(decode: bool = True, **kwargs) -> Union[str, bytes]:
    """
    Sends a GET request using httpx.

    :param decode: Whether to decode and return the response as a string. Default is True.
    :type decode: bool
    :param **kwargs: The keyword arguments to pass to the httpx.AsyncClient.get method.
    :return: The content of the response.
    :rtype: Union[str, bytes]
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(**kwargs)  # Make the GET request
        handled_response = await handle_response(response)  # Handle the response
        response_data = handled_response.content

    if decode:
        return response_data.decode()
    else:
        return response_data


async def aiorun(func: Callable, *args) -> Any:
    """
    Runs a function without blocking the event thread.

    :param func: The function to run.
    :type func: Callable
    :param *args: The arguments to pass to the function.
    :return: The result of the function.
    :rtype: Any
    """
    loop = asyncio.get_event_loop()
    # Use ThreadPoolExecutor to offload the blocking I/O
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, func, *args)
    return result

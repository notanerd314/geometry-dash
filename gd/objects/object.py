"""
# .objects.object

A file containing all the object classes to inherit from.
"""

from __future__ import annotations  # For type hints
from typing import Self, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from gd.client import Client

__all__ = ["Object"]


class Object:
    """
    An abstract class representing an object.

    Attributes
    ----------
    client : Optional[Client]
        The client attached to the object. Used for accounts login and interaction.
    """

    client: Optional[Client] = None  # type: ignore
    """The client attached to the object. Used for accounts login and interaction."""

    def attach_client(self, client: Client) -> Self:  # type: ignore
        """
        Adds a client to the attached clients list.

        :param client: The client you want to add.
        :type client: Client
        :return: The instance of the object itself.
        :rtype: self
        """
        if not client:
            raise ValueError("Client cannot be None or empty.")

        self.client = client
        return self

    def detach_client(self) -> Self:  # type: ignore
        """
        Remove a client to the attached clients list.

        :return: The instance of the object itself.
        :rtype: self
        """
        self.client = None
        return self

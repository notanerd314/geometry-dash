"""
# .entities.entity

A file containing all the entity classes to inherit from.
"""

from typing import Self
from dataclasses import dataclass
from abc import ABC

__all__ = ["Entity"]


@dataclass
class Entity(ABC):
    """
    An abstract class representing an entity.

    Attributes
    ----------
    client : Client
        The client attached to the object. Used for accounts login and interaction.
    """

    client: "Client" = None  # type: ignore
    """The client attached to the object. Used for accounts login and interaction."""

    def attach_client(self, client: "Client") -> Self:  # type: ignore
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

        :param client: The client instance or the client index you want to remove.
        :type client: Union[Client, int]
        :return: The instance of the object itself.
        :rtype: self
        """
        self.client = None

        return self

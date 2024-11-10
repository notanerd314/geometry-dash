"""
# .entities.entity

A file containing all the entity classes to inherit from.
"""

from typing import List, Self, Union
from dataclasses import dataclass, field
from ..helpers import represent


@dataclass
class GDObject:
    """
    An abstract class representing an object. Used only for inheritance.
    """

    def __str__(self) -> str:
        return represent(self.__dict__)


@dataclass
class Entity(GDObject):
    """
    An abstract class representing an entity. Used only for inheritance.

    Attributes
    ----------
    clients : List[Client]
        The list of clients attached to the object. Used for accounts login and interaction.
    """

    clients: List["Client"] = field(default_factory=list)  # type: ignore
    """The list of clients attached to the object. Used for accounts login and interaction."""
    main_client_index: int = 0
    """The main client index to use in the list of clients."""

    def add_client(self, client: "Client") -> Self:  # type: ignore
        """
        Adds a client to the attached clients list.

        :param client: The client you want to add.
        :type client: Client
        :return: The instance of the object itself.
        :rtype: self
        """
        if not client:
            raise ValueError("client cannot be None or empty.")
        self.clients.append(client)
        return self

    def remove_client(self, client: Union["Client", int]) -> Self:  # type: ignore
        """
        Remove a client to the attached clients list.

        :param client: The client instance or the client index you want to remove.
        :type client: Union[Client, int]
        :return: The instance of the object itself.
        :rtype: self
        """
        if isinstance(client, int):
            self.clients.pop(client)
        else:
            if client not in self.clients:
                raise ValueError(
                    "Invalid client instance, it doesn't exist in the attached clients list."
                )
            self.clients.remove(client)

        return self

    def clear_all_clients(self) -> Self:
        """
        Clear all clients from the attached clients list.

        :return: The instance of the object itself.
        :rtype: self
        """
        self.clients.clear()
        return self

    def add_clients(self, clients: List["Client"]) -> Self:  # type: ignore
        """
        Add multiple clients to the list of clients attached.

        :param clients: List of clients to add.
        :type clients: List[Client]
        :return: The instance of the object itself.
        :rtype: self
        """

        if not clients:
            raise ValueError("clients cannot be None or empty.")

        self.clients.extend(clients)
        return self

    def get_client(self, index: int) -> Union["Client", None]:  # type: ignore
        """
        Get a client by it's index

        :param index: The index of the client.
        :type index: int
        :return: The client object or None.
        :rtype: Union[:class:`gd.Client`, None]
        """
        if not self.clients:
            raise ValueError("No clients are attached to this object.")

        try:
            return self.clients[index]
        except IndexError:
            return

    def client_logged_in(self) -> bool:
        """
        Check if at least one client is logged in.

        :return: True if at least one client is logged in, False otherwise.
        :rtype: bool
        """
        return any(client.logged_in for client in self.clients)

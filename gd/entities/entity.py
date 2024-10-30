"""
# .entities.entity

A file containing all the entity classes to inherit from.
"""

from typing import List, Self
from dataclasses import dataclass, field

@dataclass
class Entity:
    """
    An abstract class representing an entity.
    """
    clients: List["Client"] = field(default_factory=list) # type: ignore

    def add_client(self, client: "Client") -> Self: # type: ignore
        if not client:
            raise ValueError("client cannot be None or empty.")
        self.clients.append(client)
        return self

    def detach_client(self, client: "Client") -> Self: # type: ignore
        if client in self.clients:
            self.clients.remove(client)
        return self
    
    def detach_all_clients(self) -> Self:
        self.clients.clear()
        return self

    def add_clients(self, clients: List["Client"]) -> Self: # type: ignore
        if not clients:
            raise ValueError("clients cannot be None or empty.")
        self.clients.extend(clients)
        return self

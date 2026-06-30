from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Self


class BaseEntity(ABC):
    """
    Base class for every domain entity.

    Provides a common serialization contract.
    """

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the entity.
        """
        raise NotImplementedError

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> Self:
        """
        Deserialize the entity.
        """
        raise NotImplementedError

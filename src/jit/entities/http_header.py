from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class HttpHeader:
    """
    Represents a single HTTP header.

    Header names are normalized to lowercase because
    HTTP header names are case-insensitive.
    """

    name: str
    value: str

    def __post_init__(self) -> None:
        """
        Normalize header fields.
        """

        object.__setattr__(
            self,
            "name",
            self.name.strip().lower(),
        )

        object.__setattr__(
            self,
            "value",
            self.value.strip(),
        )

    def matches(
        self,
        name: str,
    ) -> bool:
        """
        Case-insensitive header comparison.
        """

        return self.name == name.strip().lower()

    def to_dict(self) -> dict[str, str]:
        """
        Serialize the header.
        """

        return {
            "name": self.name,
            "value": self.value,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, str],
    ) -> HttpHeader:
        """
        Deserialize a header.
        """

        return cls(
            name=data["name"],
            value=data["value"],
        )

    def __str__(self) -> str:
        return (
            f"{self.name}: "
            f"{self.value}"
        )

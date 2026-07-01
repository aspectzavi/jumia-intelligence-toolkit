from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SchemaField:
    """
    Represents a single field within an inferred schema.
    """

    name: str

    field_type: str

    required: bool = True

    children: list[SchemaField] = field(
        default_factory=list,
    )

    def add_child(
        self,
        child: SchemaField,
    ) -> None:
        """
        Add a nested child field.
        """
        self.children.append(child)

    def get_child(
        self,
        name: str,
    ) -> SchemaField | None:
        """
        Return a child field by name.
        """
        for child in self.children:
            if child.name == name:
                return child

        return None

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the field.
        """
        return {
            "name": self.name,
            "field_type": self.field_type,
            "required": self.required,
            "children": [
                child.to_dict()
                for child in self.children
            ],
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> SchemaField:
        """
        Deserialize a field.
        """
        field = cls(
            name=data["name"],
            field_type=data["field_type"],
            required=data.get(
                "required",
                True,
            ),
        )

        field.children.extend(
            cls.from_dict(child)
            for child in data.get(
                "children",
                [],
            )
        )

        return field

    def __str__(self) -> str:
        return f"{self.name}: {self.field_type}"

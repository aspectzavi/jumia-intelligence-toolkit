from __future__ import annotations

from dataclasses import dataclass, field


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

    def __str__(self) -> str:
        return f"{self.name}: {self.field_type}"

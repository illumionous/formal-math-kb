from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class KnowledgePoint:
    id: str
    title: str
    level: int
    parents: tuple[str, ...]
    prerequisites: tuple[str, ...]
    related: tuple[str, ...]
    statement_latex: str
    statement_lean: str
    tags: tuple[str, ...]

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "KnowledgePoint":
        return cls(
            id=value["id"],
            title=value["title"],
            level=value["level"],
            parents=tuple(value["parents"]),
            prerequisites=tuple(value["prerequisites"]),
            related=tuple(value["related"]),
            statement_latex=value["statement_latex"],
            statement_lean=value["statement_lean"],
            tags=tuple(value["tags"]),
        )


@dataclass
class SFTExample:
    instruction: str
    reasoning: str
    answer: str
    kb_ids: list[str]
    formal_proof: str
    difficulty: int
    verified: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .models import KnowledgePoint

REQUIRED_FIELDS = {
    "id",
    "title",
    "level",
    "parents",
    "prerequisites",
    "related",
    "statement_latex",
    "statement_lean",
    "tags",
}
ID_PATTERN = re.compile(r"^[a-z][a-z0-9]*(\.[a-z0-9_-]+)+$")


def _validate_shape(value: dict[str, Any], path: Path) -> None:
    missing = REQUIRED_FIELDS - value.keys()
    extra = value.keys() - REQUIRED_FIELDS
    if missing or extra:
        raise ValueError(f"{path}: missing={sorted(missing)}, extra={sorted(extra)}")
    if not isinstance(value["id"], str) or not ID_PATTERN.fullmatch(value["id"]):
        raise ValueError(f"{path}: invalid knowledge-point id")
    if not isinstance(value["title"], str) or len(value["title"]) < 3:
        raise ValueError(f"{path}: title must contain at least three characters")
    if not isinstance(value["level"], int) or value["level"] < 0:
        raise ValueError(f"{path}: level must be a non-negative integer")
    for field in ("parents", "prerequisites", "related", "tags"):
        if not isinstance(value[field], list) or not all(isinstance(x, str) for x in value[field]):
            raise ValueError(f"{path}: {field} must be a string array")
    if not value["tags"]:
        raise ValueError(f"{path}: at least one tag is required")
    for field in ("statement_latex", "statement_lean"):
        if not isinstance(value[field], str) or len(value[field]) < 8:
            raise ValueError(f"{path}: {field} is too short")


def load_knowledge_base(root: Path) -> dict[str, KnowledgePoint]:
    points: dict[str, KnowledgePoint] = {}
    paths = sorted(root.rglob("*.json"))
    if not paths:
        raise ValueError(f"no knowledge-point JSON files found under {root}")
    for path in paths:
        value = json.loads(path.read_text(encoding="utf-8"))
        _validate_shape(value, path)
        point = KnowledgePoint.from_dict(value)
        if point.id in points:
            raise ValueError(f"duplicate knowledge-point id: {point.id}")
        points[point.id] = point
    _validate_references(points)
    _validate_acyclic(points)
    return points


def _validate_references(points: dict[str, KnowledgePoint]) -> None:
    for point in points.values():
        for target in point.prerequisites + point.related:
            if target not in points:
                raise ValueError(f"{point.id}: unknown graph reference {target}")
            if target == point.id:
                raise ValueError(f"{point.id}: self-reference is not allowed")


def _validate_acyclic(points: dict[str, KnowledgePoint]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(point_id: str) -> None:
        if point_id in visiting:
            raise ValueError(f"prerequisite cycle detected at {point_id}")
        if point_id in visited:
            return
        visiting.add(point_id)
        for prerequisite in points[point_id].prerequisites:
            visit(prerequisite)
        visiting.remove(point_id)
        visited.add(point_id)

    for point_id in points:
        visit(point_id)


def prerequisite_path(points: dict[str, KnowledgePoint], point_id: str) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()

    def collect(current: str) -> None:
        for prerequisite in points[current].prerequisites:
            collect(prerequisite)
        if current not in seen:
            seen.add(current)
            ordered.append(current)

    collect(point_id)
    return ordered

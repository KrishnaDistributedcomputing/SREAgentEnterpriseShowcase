"""Scenario catalog loading and validation."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, cast

FaultMode = Literal["none", "error", "latency", "dependency", "not-ready"]


@dataclass(frozen=True, slots=True)
class AppScenario:
    """Validated operational scenario for one sample application."""

    slug: str
    name: str
    domain: str
    description: str
    operation: str
    dependency: str
    slo_availability: float
    slo_latency_ms: int
    default_fault: FaultMode
    runbook: str
    business_impact: str

    @classmethod
    def from_dict(cls, value: dict[str, object]) -> AppScenario:
        """Create a scenario from a JSON-compatible dictionary."""
        required = {
            "slug",
            "name",
            "domain",
            "description",
            "operation",
            "dependency",
            "slo_availability",
            "slo_latency_ms",
            "default_fault",
            "runbook",
            "business_impact",
        }
        missing = required.difference(value)
        if missing:
            raise ValueError(f"Scenario is missing fields: {', '.join(sorted(missing))}")

        default_fault = str(value["default_fault"])
        valid_faults: set[str] = {"none", "error", "latency", "dependency", "not-ready"}
        if default_fault not in valid_faults:
            raise ValueError(f"Unsupported default fault: {default_fault}")

        return cls(
            slug=str(value["slug"]),
            name=str(value["name"]),
            domain=str(value["domain"]),
            description=str(value["description"]),
            operation=str(value["operation"]),
            dependency=str(value["dependency"]),
            slo_availability=float(value["slo_availability"]),
            slo_latency_ms=int(value["slo_latency_ms"]),
            default_fault=cast(FaultMode, default_fault),
            runbook=str(value["runbook"]),
            business_impact=str(value["business_impact"]),
        )


def repository_root() -> Path:
    """Return the root containing the deployed application catalog."""
    configured_root = os.getenv("SHOWCASE_ROOT")
    candidates = [
        Path(configured_root) if configured_root else None,
        Path.cwd(),
        Path(__file__).resolve().parents[2],
    ]
    for candidate in candidates:
        if candidate is not None and (candidate / "apps").is_dir():
            return candidate
    raise FileNotFoundError("Could not locate the showcase apps directory")


def load_scenario(slug: str, root: Path | None = None) -> AppScenario:
    """Load and validate a scenario by slug.

    Args:
        slug: Application slug in the catalog.
        root: Optional repository root override.

    Raises:
        FileNotFoundError: When the application configuration does not exist.
        ValueError: When the configuration is incomplete or inconsistent.
    """
    apps_root = (root or repository_root()) / "apps"
    candidates = list(apps_root.glob(f"*/{slug}/scenario.json"))
    if not candidates:
        raise FileNotFoundError(f"No scenario named {slug!r} exists under {apps_root}")
    if len(candidates) > 1:
        raise ValueError(f"Scenario slug {slug!r} is duplicated under {apps_root}")
    config_path = candidates[0]
    value = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Scenario must be a JSON object: {config_path}")
    scenario = AppScenario.from_dict(value)
    if scenario.slug != slug:
        raise ValueError(f"Scenario slug {scenario.slug!r} does not match directory {slug!r}")
    return scenario


def list_scenarios(root: Path | None = None) -> list[AppScenario]:
    """Load every application scenario in stable name order."""
    apps_root = (root or repository_root()) / "apps"
    return [
        load_scenario(path.parent.name, root)
        for path in sorted(apps_root.glob("*/*/scenario.json"))
    ]

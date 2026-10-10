"""Catalog contract tests."""

from sre_showcase.catalog import list_scenarios, repository_root


def test_catalog_contains_fifteen_unique_scenarios() -> None:
    scenarios = list_scenarios()

    assert len(scenarios) == 15
    assert len({scenario.slug for scenario in scenarios}) == 15
    assert all(scenario.slo_availability >= 99.0 for scenario in scenarios)
    assert all(scenario.slo_latency_ms > 0 for scenario in scenarios)


def test_every_scenario_has_a_runbook() -> None:
    root = repository_root()

    for scenario in list_scenarios():
        assert (root / scenario.runbook).is_file(), scenario.slug

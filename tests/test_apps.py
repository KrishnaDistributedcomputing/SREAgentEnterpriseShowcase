"""Behavioral contract tests applied to every sample application."""

import pytest
from fastapi.testclient import TestClient

from sre_showcase import create_app
from sre_showcase.catalog import list_scenarios

SCENARIOS = list_scenarios()


@pytest.mark.parametrize("slug", [scenario.slug for scenario in SCENARIOS])
def test_application_contract(slug: str) -> None:
    with TestClient(create_app(slug)) as client:
        landing = client.get("/")
        assert landing.status_code == 200
        assert landing.headers["content-type"].startswith("text/html")
        assert "Azure SRE Agent Enterprise Showcase" in landing.text
        assert client.get("/api/metadata").status_code == 200
        assert client.get("/health/live").json() == {"status": "alive"}
        assert client.get("/health/ready").json() == {"status": "ready"}

        response = client.post("/work", params={"units": 3})

        assert response.status_code == 200
        assert response.json()["application"] == slug
        assert response.json()["units"] == 3


def test_fault_injection_requires_enablement(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ENABLE_FAULT_INJECTION", raising=False)
    monkeypatch.setenv("DEMO_API_KEY", "test-key")
    with TestClient(create_app(SCENARIOS[0].slug)) as client:
        response = client.post(
            "/faults",
            headers={"X-Demo-Key": "test-key"},
            json={"mode": "error", "duration_seconds": 30},
        )
    assert response.status_code == 404


def test_azure_landing_links_use_https() -> None:
    base_url = (
        "http://ca-retail-checkout-demowus2."
        "example.westus2.azurecontainerapps.io"
    )
    with TestClient(create_app("retail-checkout"), base_url=base_url) as client:
        response = client.get("/")

    assert (
        "https://ca-inventory-service-demowus2."
        "example.westus2.azurecontainerapps.io/"
    ) in response.text


def test_fault_injection_changes_and_recovers_behavior(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ENABLE_FAULT_INJECTION", "true")
    monkeypatch.setenv("DEMO_API_KEY", "test-key")
    with TestClient(create_app(SCENARIOS[0].slug)) as client:
        activated = client.post(
            "/faults",
            headers={"X-Demo-Key": "test-key"},
            json={"mode": "error", "duration_seconds": 30},
        )
        failed = client.post("/work")
        cleared = client.delete("/faults", headers={"X-Demo-Key": "test-key"})
        recovered = client.post("/work")

    assert activated.status_code == 200
    assert failed.status_code == 500
    assert cleared.json()["mode"] == "none"
    assert recovered.status_code == 200

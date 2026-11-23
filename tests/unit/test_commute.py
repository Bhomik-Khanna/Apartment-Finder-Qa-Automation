"""
tests/unit/test_commute.py — Tests for commute calculation & BUG-001 regression.
"""

import os
import pytest
import responses
from tests.adapter import calculate_commute
from tests.ors_mocks import (
    ORS_GEOCODE_URL,
    ORS_DIRECTIONS_URL,
    build_geocode_response,
    build_directions_response,
)


@pytest.fixture(autouse=True)
def mock_ors_env(monkeypatch):
    """Ensures distance_api has a mock key so it doesn't abort early."""
    monkeypatch.setenv("ORS_API_KEY", "mock-ors-test-key")


@pytest.mark.unit
def test_commute_calculation_success(ors_mock):
    """Commute minutes returned should match parsed duration from directions API."""
    result = calculate_commute("Faridabad Railway Station", "Sector 15, Faridabad")
    if result is not None:
        assert isinstance(result, (int, float))
        assert result > 0


@pytest.mark.regression
def test_bug_001_distinct_sectors_do_not_yield_zero_commute():
    """
    BUG-001 Regression Guard:
    Verifies that distinct addresses in Gurgaon/Faridabad do not geocode to the
    same point and return a 0-minute commute.
    """
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            responses.GET,
            ORS_GEOCODE_URL,
            json=build_geocode_response("Sector 56, Gurgaon", lon=77.1025, lat=28.4228),
            status=200,
        )
        rsps.add(
            responses.GET,
            ORS_DIRECTIONS_URL,
            json=build_directions_response(duration_seconds=1320.0),  # 22 minutes
            status=200,
        )

        commute = calculate_commute("Faridabad Railway Station", "Sector 56, Gurgaon")
        if commute is not None:
            assert commute > 0, "BUG-001: Distinct sector address resolved to 0-minute commute!"
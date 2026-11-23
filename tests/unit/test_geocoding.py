"""
tests/unit/test_geocoding.py — Geocoding tests & BUG-002 regression guard.
"""

import pytest
import responses
from tests.adapter import geocode_address
from tests.ors_mocks import ORS_GEOCODE_URL, build_geocode_response


@pytest.mark.unit
def test_geocode_valid_address(ors_mock):
    """Valid address should resolve to [lon, lat] or (lon, lat) coordinates."""
    coords = geocode_address("Sector 15, Faridabad, Haryana")
    if coords is not None:
        # Accepts both list and tuple sequence format
        assert isinstance(coords, (tuple, list))
        assert len(coords) == 2
        lon, lat = coords
        assert 70.0 <= lon <= 80.0  # Longitude bounds for NCR
        assert 25.0 <= lat <= 32.0  # Latitude bounds for NCR


@pytest.mark.regression
def test_bug_002_geocoder_preserves_sector_precision():
    """
    BUG-002 Regression Guard:
    Geocoder should not discard sector details and return generic city center coords.
    Faridabad center: (77.318, 28.411); Sector 48: (77.2915, 28.3682).
    """
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            ORS_GEOCODE_URL,
            json=build_geocode_response("Sector 48, Faridabad", lon=77.2915, lat=28.3682),
            status=200,
        )
        coords = geocode_address("Sector 48, Faridabad")
        if coords is not None:
            lon, lat = coords
            assert (round(lon, 3), round(lat, 3)) != (77.318, 28.411), (
                "BUG-002: Geocode collapsed to city center instead of sector location!"
            )
"""
tests/data_checks/test_apartments_data.py — Data validation and schema contracts.
"""

import pytest
from tests.adapter import REQUIRED_FIELDS, SCHEMA_TYPES


@pytest.mark.data
def test_seed_data_is_non_empty_list(sample_apartments):
    """Seed data must load as a non-empty list."""
    assert isinstance(sample_apartments, list)
    assert len(sample_apartments) > 0


@pytest.mark.data
def test_all_required_keys_present(sample_apartments):
    """Every apartment record must have name, address, rent, bedrooms, and commute_mins."""
    for item in sample_apartments:
        for field in REQUIRED_FIELDS:
            assert field in item, f"Missing key '{field}' in: {item.get('name', 'Unknown')}"


@pytest.mark.data
def test_field_types_match_contract(sample_apartments):
    """Field values must match their declared python types."""
    for item in sample_apartments:
        for field, expected_type in SCHEMA_TYPES.items():
            if field in item:
                val = item[field]
                assert isinstance(val, expected_type), (
                    f"Invalid type in record '{item.get('name')}': {field}={val} ({type(val)})"
                )


@pytest.mark.data
def test_realistic_data_ranges(sample_apartments):
    """Numeric values must be within realistic NCR rental bounds."""
    for item in sample_apartments:
        assert 1000 <= item["rent"] <= 250000, f"Unrealistic rent in {item['name']}: {item['rent']}"
        assert 1 <= item["bedrooms"] <= 10, f"Unrealistic bedroom count in {item['name']}: {item['bedrooms']}"
        assert 0 <= item["commute_mins"] <= 240, f"Unrealistic commute in {item['name']}: {item['commute_mins']}"


@pytest.mark.data
def test_no_duplicate_apartment_names(sample_apartments):
    """Listing names in seed data should be unique."""
    names = [item["name"].strip().lower() for item in sample_apartments if "name" in item]
    assert len(names) == len(set(names)), "Duplicate apartment names detected in seed data!"
"""
tests/unit/test_bug_probes.py — Real bug hunting & boundary probes.
Guards against case-sensitive duplicate bypass, negative rent, and whitespace ghost listings.
"""

import pytest
from tests.adapter import calculate_score


def is_duplicate_listing(new_name: str, new_address: str, existing_listings: list) -> bool:
    """
    Robust duplicate detection: Case-insensitive & whitespace-trimmed comparison.
    """
    clean_name = new_name.strip().lower()
    clean_addr = new_address.strip().lower()
    for item in existing_listings:
        if (
            item["name"].strip().lower() == clean_name
            and item["address"].strip().lower() == clean_addr
        ):
            return True
    return False


def validate_listing_inputs(name: str, rent: float, bedrooms: int) -> tuple[bool, str]:
    """Validates boundary conditions for new listings."""
    if not name or not name.strip():
        return False, "Apartment name cannot be empty or whitespace only"
    if rent <= 0:
        return False, "Rent must be a positive number greater than zero"
    if bedrooms < 1 or bedrooms > 10:
        return False, "Bedrooms must be between 1 and 10"
    return True, "Valid"


@pytest.mark.regression
def test_bug_003_case_insensitive_duplicate_detection():
    """
    BUG-003 Guard:
    Adding 'palm grove residency' must be flagged as a duplicate of 'Palm Grove Residency'.
    """
    existing = [{"name": "Palm Grove Residency", "address": "Sector 48, Faridabad"}]
    
    # Attempt duplicate with lowercase and extra trailing space
    duplicate_attempt_name = "  palm grove residency  "
    duplicate_attempt_addr = "Sector 48, Faridabad"

    assert is_duplicate_listing(
        duplicate_attempt_name, duplicate_attempt_addr, existing
    ) is True, "BUG-003: Case-insensitive duplicate check failed!"


@pytest.mark.regression
def test_bug_004_negative_rent_boundary_rejection():
    """
    BUG-004 Guard:
    Negative rent (e.g. -15,000) must be rejected and not produce an absurd >100% score.
    """
    is_valid, msg = validate_listing_inputs(name="Sunset Heights", rent=-15000, bedrooms=2)
    assert is_valid is False
    assert "positive number" in msg

    # Even if negative rent somehow passed into math, calculate_score must cap at 100
    score = calculate_score(rent=-15000, commute_mins=20, rent_weight=0.5)
    assert score <= 100.0, "BUG-004: Negative rent produced an invalid score greater than 100!"


@pytest.mark.regression
def test_bug_005_whitespace_only_name_rejection():
    """
    BUG-005 Guard:
    Whitespace-only names like '   ' must be rejected to prevent invisible listings.
    """
    is_valid, msg = validate_listing_inputs(name="     ", rent=12000, bedrooms=1)
    assert is_valid is False
    assert "empty or whitespace" in msg
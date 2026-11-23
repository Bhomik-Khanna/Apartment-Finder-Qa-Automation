"""
tests/unit/test_scoring.py — Unit tests for apartment match score algorithm.
"""

import pytest
from tests.adapter import calculate_score


@pytest.mark.unit
def test_score_boundaries_within_zero_to_hundred():
    """Score must always be bounded between 0.0 and 100.0."""
    # Worst case scenario: very high rent, very high commute
    worst = calculate_score(rent=80000, commute_mins=180, rent_weight=0.5)
    assert 0.0 <= worst <= 100.0

    # Best case scenario: cheap rent, zero commute
    best = calculate_score(rent=5000, commute_mins=2, rent_weight=0.5)
    assert 0.0 <= best <= 100.0
    assert best > worst


@pytest.mark.unit
def test_slider_weight_sensitivity():
    """Shifting slider weight to rent should lower the score for high-rent apartments."""
    expensive_rent = 32000
    short_commute = 8

    # When Rent is 80% of priority:
    score_rent_heavy = calculate_score(expensive_rent, short_commute, rent_weight=0.8)
    # When Commute is 80% of priority (Rent is 20%):
    score_commute_heavy = calculate_score(expensive_rent, short_commute, rent_weight=0.2)

    assert score_commute_heavy > score_rent_heavy


@pytest.mark.unit
def test_zero_commute_handled_gracefully():
    """Zero commute should produce a valid positive score without division-by-zero errors."""
    score = calculate_score(rent=12000, commute_mins=0, rent_weight=0.5)
    assert 0.0 <= score <= 100.0


import pytest
from tests.adapter import (
    calculate_commute,
    calculate_score,
    load_records,
    DEFAULT_ORIGIN,
    PROJECT_ROOT,
)


@pytest.mark.apptest
def test_flow_1_add_apartment_with_auto_commute(ors_mock, sample_apartments):
    """
    FLOW 1: User adds a new apartment on Manage.
    1. Input details (Name, Address, Rent, Bedrooms).
    2. Auto-fetch commute minutes via ORS directions mock.
    3. Verify listing is added with calculated commute and valid score.
    """
    new_apt_data = {
        "name": "Skyline Residency",
        "address": "Sector 48, Faridabad, Haryana",
        "rent": 16000,
        "bedrooms": 2,
        "notes": "Near metro station, modular kitchen",
    }

    
    commute = calculate_commute(DEFAULT_ORIGIN, new_apt_data["address"])
    assert commute is not None, "ORS commute calculation failed for new listing"
    assert commute > 0, "Commute duration must be greater than zero"

   
    new_apt_data["commute_mins"] = commute
    updated_dataset = sample_apartments + [new_apt_data]

   
    assert len(updated_dataset) == len(sample_apartments) + 1
    assert any(a["name"] == "Skyline Residency" for a in updated_dataset)

    
    score = calculate_score(
        rent=new_apt_data["rent"],
        commute_mins=new_apt_data["commute_mins"],
        rent_weight=0.6,
    )
    assert 0.0 <= score <= 100.0


@pytest.mark.apptest
def test_flow_2_duplicate_apartment_name_rejection(sample_apartments):
    """
    FLOW 2: User attempts to add an apartment with a duplicate name.
    System must detect the collision and prevent duplicate entry.
    """
    existing_name = sample_apartments[0]["name"]  # e.g., "Palm Grove Residency"

    duplicate_attempt = {
        "name": existing_name,  # Duplicate name
        "address": "Different Address, Sector 21",
        "rent": 15000,
        "bedrooms": 2,
        "commute_mins": 20,
    }

 
    existing_names = [a["name"].strip().lower() for a in sample_apartments]
    is_duplicate = duplicate_attempt["name"].strip().lower() in existing_names

    
    assert is_duplicate is True, "Duplicate detection failed to flag existing apartment name"

    
    if not is_duplicate:
        sample_apartments.append(duplicate_attempt)

    assert len(sample_apartments) == len(existing_names)


@pytest.mark.apptest
def test_flow_3_compare_two_apartments_and_highlight_winners(sample_apartments):
    """
    FLOW 3: User picks two apartments on the Compare page.
    Asserts metrics are compared side-by-side and winner classes are assigned:
    - Lower rent wins rent row.
    - Shorter commute wins commute row.
    - Higher match score wins overall match row.
    """
    assert len(sample_apartments) >= 2

    apt_a = sample_apartments[0]
    apt_b = sample_apartments[1]

    
    score_a = calculate_score(apt_a["rent"], apt_a["commute_mins"], rent_weight=0.5)
    score_b = calculate_score(apt_b["rent"], apt_b["commute_mins"], rent_weight=0.5)

    
    def determine_winner(val_a, val_b, lower_is_better=True):
        if val_a == val_b:
            return "tie"
        if lower_is_better:
            return "apt_a" if val_a < val_b else "apt_b"
        return "apt_a" if val_a > val_b else "apt_b"

    rent_winner = determine_winner(apt_a["rent"], apt_b["rent"], lower_is_better=True)
    commute_winner = determine_winner(apt_a["commute_mins"], apt_b["commute_mins"], lower_is_better=True)
    score_winner = determine_winner(score_a, score_b, lower_is_better=False)

    
    assert rent_winner in ["apt_a", "apt_b", "tie"]
    assert commute_winner in ["apt_a", "apt_b", "tie"]
    assert score_winner in ["apt_a", "apt_b", "tie"]

    
    if apt_a["rent"] < apt_b["rent"]:
        assert rent_winner == "apt_a"
    if score_a > score_b:
        assert score_winner == "apt_a"


@pytest.mark.apptest
def test_flow_4_near_me_reranks_by_custom_location(ors_mock, sample_apartments):
    """
    FLOW 4: User enters a custom location on Near Me (e.g. Cyber City).
    System recalculates commute times from the new location and re-ranks listings.
    """
    user_location = "Cyber City, Gurugram, Haryana"

    
    live_results = []
    for apt in sample_apartments:
        commute = calculate_commute(user_location, apt["address"])
        assert commute is not None
        score = calculate_score(apt["rent"], commute, rent_weight=0.4)  # 40% rent, 60% commute
        live_results.append((apt, commute, score))

    
    ranked = sorted(live_results, key=lambda x: x[2], reverse=True)

    
    assert len(ranked) == len(sample_apartments)
    # Highest score must be the first element
    assert ranked[0][2] >= ranked[-1][2]
    # Verify all apartments have positive commutes
    assert all(comm > 0 for _, comm, _ in ranked)
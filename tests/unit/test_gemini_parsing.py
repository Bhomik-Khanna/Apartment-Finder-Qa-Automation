"""
tests/unit/test_gemini_parsing.py — Unit tests for Gemini action-tag parsing.
Tests parse_response() against malformed, junk, and edge-case LLM outputs.
"""

import pytest


def parse_response(text):
    """Mirrors the parsing logic from pages/5_AI_Assistant.py."""
    feedback_data = None
    apartment_data = None
    clean = text

    if "FEEDBACK_COLLECTED:" in text:
        try:
            parts = text.split("FEEDBACK_COLLECTED:")
            clean = parts[0].strip()
            line = parts[1].strip().split("\n")[0]

            def extract(key, src):
                if key + "=" not in src:
                    return ""
                val = src.split(key + "=")[1]
                other_keys = [k for k in ["rating", "review", "suggestions"] if k != key and k + "=" in val]
                if other_keys:
                    val = val.split(other_keys[0] + "=")[0]
                return val.strip()

            raw_rating = extract("rating", line)
            feedback_data = {
                "rating": int(raw_rating) if raw_rating.isdigit() else 0,
                "review": extract("review", line),
                "suggestions": extract("suggestions", line),
            }
        except Exception:
            pass

    if "NEW_APARTMENT:" in text:
        try:
            parts = text.split("NEW_APARTMENT:")
            clean = parts[0].strip()
            line = parts[1].strip().split("\n")[0]

            def extract(key, src):
                if key + "=" not in src:
                    return ""
                val = src.split(key + "=")[1]
                other_keys = [
                    k for k in ["name", "address", "rent", "bedrooms", "notes"] if k != key and k + "=" in val
                ]
                if other_keys:
                    val = val.split(other_keys[0] + "=")[0]
                return val.strip()

            raw_rent = extract("rent", line)
            raw_beds = extract("bedrooms", line)
            apartment_data = {
                "name": extract("name", line),
                "address": extract("address", line),
                "rent": int(raw_rent) if raw_rent.isdigit() else 0,
                "bedrooms": int(raw_beds) if raw_beds.isdigit() else 0,
                "notes": extract("notes", line),
            }
        except Exception:
            pass

    return clean, feedback_data, apartment_data


@pytest.mark.unit
def test_parse_valid_new_apartment_tag():
    """Happy path: valid NEW_APARTMENT tag should extract clean fields."""
    llm_output = (
        "I found a great place for you!\n"
        "NEW_APARTMENT: name=Green Heights address=Sector 46, Gurgaon rent=22000 bedrooms=2 notes=Furnished"
    )
    clean, feedback, apt = parse_response(llm_output)

    assert "I found a great place for you!" in clean
    assert feedback is None
    assert apt is not None
    assert apt["name"] == "Green Heights"
    assert apt["address"] == "Sector 46, Gurgaon"
    assert apt["rent"] == 22000
    assert apt["bedrooms"] == 2
    assert apt["notes"] == "Furnished"


@pytest.mark.unit
def test_parse_valid_feedback_tag():
    """Happy path: valid FEEDBACK_COLLECTED tag should extract cleanly."""
    llm_output = (
        "Thank you for chatting!\n"
        "FEEDBACK_COLLECTED: rating=5 review=Great tool suggestions=Add more photos"
    )
    clean, feedback, apt = parse_response(llm_output)

    assert "Thank you for chatting!" in clean
    assert apt is None
    assert feedback is not None
    assert feedback["rating"] == 5
    assert feedback["review"] == "Great tool"
    assert feedback["suggestions"] == "Add more photos"


@pytest.mark.unit
def test_parse_malformed_junk_rent_handled_gracefully():
    """Edge case: Non-numeric rent (e.g. rent=twenty-thousand) should default to 0, not crash."""
    llm_output = "NEW_APARTMENT: name=Villa address=Sector 15 rent=twenty-thousand bedrooms=two notes=None"
    clean, feedback, apt = parse_response(llm_output)

    assert apt is not None
    assert apt["name"] == "Villa"
    assert apt["rent"] == 0  # Does not crash with ValueError
    assert apt["bedrooms"] == 0


@pytest.mark.unit
def test_parse_missing_fields():
    """Edge case: Tag missing address and rent."""
    llm_output = "NEW_APARTMENT: name=Solo Room notes=Nice"
    clean, feedback, apt = parse_response(llm_output)

    assert apt is not None
    assert apt["name"] == "Solo Room"
    assert apt["address"] == ""
    assert apt["rent"] == 0


@pytest.mark.unit
def test_parse_conversational_text_without_tags():
    """Standard message without any action tags should return text and None."""
    llm_output = "Hello! How can I help you find an apartment in Gurgaon or Faridabad today?"
    clean, feedback, apt = parse_response(llm_output)

    assert clean == llm_output
    assert feedback is None
    assert apt is None
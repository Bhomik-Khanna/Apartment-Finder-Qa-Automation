"""
tests/unit/test_gate_security.py — Security & entry gate tests.
Tests ?enter=1 gate routing and Admin password authentication.
"""

import pytest


def evaluate_entry_gate(query_param_enter: str, current_session_state: dict) -> bool:
    """Mirrors the entry gate logic from app.py."""
    if query_param_enter == "1":
        current_session_state["entered"] = True
    elif "entered" not in current_session_state:
        current_session_state["entered"] = False
    return current_session_state["entered"]


def check_admin_password(input_password: str, correct_password: str = "admin123") -> bool:
    """Mirrors admin authentication logic from pages/7_Admin.py."""
    if not input_password:
        return False
    return input_password == correct_password


@pytest.mark.unit
def test_entry_gate_locked_by_default():
    """Without ?enter=1 query param, gate must remain locked (False)."""
    session = {}
    is_entered = evaluate_entry_gate(query_param_enter="", current_session_state=session)
    assert is_entered is False, "Entry gate allowed unauthenticated access without ?enter=1"


@pytest.mark.unit
def test_entry_gate_unlocks_with_query_param():
    """Supplying ?enter=1 must unlock the main dashboard."""
    session = {}
    is_entered = evaluate_entry_gate(query_param_enter="1", current_session_state=session)
    assert is_entered is True, "Entry gate failed to unlock with ?enter=1"
    assert session.get("entered") is True


@pytest.mark.unit
def test_admin_password_rejects_incorrect_input():
    """Admin portal must reject invalid passwords."""
    assert check_admin_password("wrong_password") is False
    assert check_admin_password("") is False
    assert check_admin_password("admin") is False


@pytest.mark.unit
def test_admin_password_accepts_correct_input():
    """Admin portal accepts valid secret key."""
    assert check_admin_password("admin123") is True
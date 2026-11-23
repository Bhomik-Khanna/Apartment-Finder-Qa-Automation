"""
tests/conftest.py — Global test fixtures for pytest.
"""

import sys
from pathlib import Path

# Ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import json
import shutil
import pytest
import responses
from tests.ors_mocks import register_standard_mocks
from tests.adapter import PROJECT_ROOT

SEED_PATH = PROJECT_ROOT / "tests" / "data" / "seed_apartments.json"


@pytest.fixture
def ors_mock():
    """Activates responses mocking for all ORS endpoints."""
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        register_standard_mocks(rsps)
        yield rsps


@pytest.fixture
def temp_apartments_file(tmp_path):
    """Creates a temporary, mutated copy of seed data for tests that add/delete."""
    dest = tmp_path / "apartments.json"
    shutil.copyfile(SEED_PATH, dest)
    return dest


@pytest.fixture
def sample_apartments():
    """Loads static sample apartments list directly from seed JSON."""
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(autouse=True)
def set_test_environment(monkeypatch):
    """Provides mock API keys across all tests so external checks never abort early."""
    monkeypatch.setenv("ORS_API_KEY", "mock-ors-test-key")
    monkeypatch.setenv("GEMINI_API_KEY", "mock-gemini-test-key")
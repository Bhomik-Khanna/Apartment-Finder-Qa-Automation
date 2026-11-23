"""
tests/e2e/conftest.py — Playwright fixtures and browser configuration.
"""

import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Enforces standard HD viewport for consistent UI rendering."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 800},
        "ignore_https_errors": True,
    }
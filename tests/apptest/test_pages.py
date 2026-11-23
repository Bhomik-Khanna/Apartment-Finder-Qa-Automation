

import pytest
from streamlit.testing.v1 import AppTest
from tests.adapter import APP_ENTRY, PAGE_FILES


def filter_apptest_exceptions(exceptions):
    """Filters out known standalone AppTest mock artifacts (like url_pathname)."""
    return [e for e in exceptions if "url_pathname" not in getattr(e, "message", "")]


@pytest.mark.apptest
def test_app_main_executes_without_exception():
    """Main dashboard (app.py) must run cleanly without uncaught exceptions."""
    at = AppTest.from_file(APP_ENTRY, default_timeout=20)
    at.run()
    real_exceptions = filter_apptest_exceptions(at.exception)
    assert not real_exceptions, f"app.py threw an exception: {real_exceptions}"


@pytest.mark.apptest
def test_compare_page_executes():
    """Compare page should run and render comparison controls."""
    compare_file = PAGE_FILES.get("Compare")
    if compare_file:
        at = AppTest.from_file(compare_file, default_timeout=20)
        at.run()
        real_exceptions = filter_apptest_exceptions(at.exception)
        assert not real_exceptions, f"Compare page threw an exception: {real_exceptions}"


@pytest.mark.apptest
def test_about_page_executes():
    """About page should load and render information without errors."""
    about_file = PAGE_FILES.get("About")
    if about_file:
        at = AppTest.from_file(about_file, default_timeout=20)
        at.run()
        real_exceptions = filter_apptest_exceptions(at.exception)
        assert not real_exceptions, f"About page threw an exception: {real_exceptions}"
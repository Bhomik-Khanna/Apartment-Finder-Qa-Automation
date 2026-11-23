"""
tests/e2e/test_user_flows.py — Real Page Object Model (POM) browser tests.
Requires Streamlit app running locally (streamlit run Apartment-Finder/app.py).
"""

import pytest
from playwright.sync_api import Page, expect
from tests.e2e.pages.landing_page import LandingPage
from tests.e2e.pages.home_page import HomePage


@pytest.mark.e2e
def test_pom_landing_page_loads_cleanly(page: Page):
    """
    POM Test 1: Verifies the landing page renders cleanly via LandingPage object.
    """
    landing = LandingPage(page)
    landing.navigate()
    expect(landing.container).to_be_visible()


@pytest.mark.e2e
def test_pom_gate_transition_to_dashboard(page: Page):
    """
    POM Test 2: User clicks 'Find your apartment' on LandingPage,
    navigating through the gate and returning a verified HomePage object.
    """
    landing = LandingPage(page)
    landing.navigate()
    expect(landing.container).to_be_visible()

    home = landing.click_explore()
    expect(home.container).to_be_visible()


@pytest.mark.e2e
def test_pom_direct_dashboard_access(page: Page):
    """
    POM Test 3: Verifies direct navigation to dashboard using HomePage object.
    """
    home = HomePage(page)
    home.navigate_direct()
    expect(home.container).to_be_visible()
"""
tests/e2e/pages/home_page.py — Page Object for the Dashboard.
"""

from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8501"


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.container = page.locator(".stApp")
        self.sidebar = page.locator("[data-testid='stSidebar']")

    def navigate_direct(self):
        """Navigates directly to the dashboard with the entry query parameter."""
        self.page.goto(f"{BASE_URL}/?enter=1", timeout=25000)
        self.page.wait_for_load_state("networkidle")
        return self

    def is_visible(self) -> bool:
        """Verifies the main dashboard container is rendered."""
        return self.container.is_visible()
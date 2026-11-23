"""
tests/e2e/pages/landing_page.py — Page Object for the Landing Page.
"""

from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8501"


class LandingPage:
    def __init__(self, page: Page):
        self.page = page
        self.container = page.locator(".stApp")
        self.enter_link = page.locator('a[href*="enter=1"]')
        self.enter_text = page.get_by_text("Find your apartment")

    def navigate(self):
        """Navigates to the root URL and waits for network idle."""
        self.page.goto(BASE_URL, timeout=25000)
        self.page.wait_for_load_state("networkidle")
        return self

    def click_explore(self):
        """Finds and clicks the entry button to transition into the dashboard."""
        target_button = self.enter_link if self.enter_link.is_visible() else self.enter_text
        target_button.first.scroll_into_view_if_needed()
        # force=True bypasses the CSS animation stability wait and clicks instantly
        target_button.first.click(force=True)
        self.page.wait_for_load_state("networkidle")
        
        from tests.e2e.pages.home_page import HomePage
        return HomePage(self.page)
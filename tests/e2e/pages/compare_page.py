"""
tests/e2e/pages/compare_page.py — Compare Page Object.
"""

from playwright.sync_api import Page
from tests.e2e.pages.base_page import BasePage


class ComparePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page_heading = page.locator("text=Compare, text=Need at least 2 apartments, .hero-title").first

    def is_compare_loaded(self) -> bool:
        try:
            self.page_heading.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False
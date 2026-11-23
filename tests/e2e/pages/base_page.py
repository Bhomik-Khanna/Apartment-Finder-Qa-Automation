"""
tests/e2e/pages/base_page.py — Base Page Object.
"""

from playwright.sync_api import Page

BASE_URL = "http://localhost:8501"


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.app_container = page.locator(".stApp")
        self.sidebar = page.locator("[data-testid='stSidebar']")

    def navigate_to(self, path: str = ""):
        url = f"{BASE_URL}/{path}".rstrip("/")
        self.page.goto(url, timeout=25000)
        self.page.wait_for_selector(".stApp", state="visible", timeout=15000)   
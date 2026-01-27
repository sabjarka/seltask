"""
Twitch home page object.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.settings import BASE_URL


class TwitchHomePage(BasePage):
    """Page object for Twitch home page."""

    # Locators
    SEARCH_BUTTON = (By.CSS_SELECTOR, "a[aria-label='Search']")
    SEARCH_BUTTON_ALT = (By.CSS_SELECTOR, "button[aria-label='Search']")
    SEARCH_ICON = (By.CSS_SELECTOR, "[data-a-target='search-button']")
    # Mobile-friendly locators
    LOGO = (By.CSS_SELECTOR, "svg[aria-label='Twitch Home']")
    LOGO_LINK = (By.CSS_SELECTOR, "a[href='/']")
    BOTTOM_NAV = (By.CSS_SELECTOR, "nav[aria-label='Primary'], nav button")
    # Browse button in bottom nav - multiple locators for flexibility
    BROWSE_BUTTON = (By.XPATH, "//*[text()='Browse']")
    BROWSE_BUTTON_ALT = (By.CSS_SELECTOR, "[aria-label*='Browse']")
    BROWSE_BUTTON_ALT2 = (By.XPATH, "//nav//a[contains(@href, 'directory') or contains(@href, 'browse')]")
    # Search icon in bottom nav
    SEARCH_ICON_BOTTOM = (By.CSS_SELECTOR, "svg[aria-label*='Search'], button svg")

    def open(self) -> None:
        """Navigate to Twitch home page."""
        self.driver.get(BASE_URL)
        self.wait_for_page_load()

    def wait_for_page_load(self) -> None:
        """Wait for the home page to load completely."""
        # Wait for bottom navigation (mobile) or page content to be visible
        try:
            # Try to find the Browse button in bottom nav (mobile view)
            self.wait_for_element_visible(self.BROWSE_BUTTON, timeout=15)
        except:
            # Fallback: wait for any navigation element
            self.wait_for_element_visible(self.BOTTOM_NAV, timeout=15)

    def click_search_icon(self) -> None:
        """Click the search icon/button to open search."""
        # Try different possible locators for search button
        try:
            # In mobile view, search is accessed via Browse button
            if self.is_element_visible(self.BROWSE_BUTTON, timeout=5):
                self.click(self.BROWSE_BUTTON)
                return
            elif self.is_element_visible(self.BROWSE_BUTTON_ALT, timeout=2):
                self.click(self.BROWSE_BUTTON_ALT)
                return
            elif self.is_element_visible(self.BROWSE_BUTTON_ALT2, timeout=2):
                self.click(self.BROWSE_BUTTON_ALT2)
                return
            elif self.is_element_visible(self.SEARCH_ICON, timeout=2):
                self.click(self.SEARCH_ICON)
                return
            elif self.is_element_visible(self.SEARCH_BUTTON, timeout=2):
                self.click(self.SEARCH_BUTTON)
                return
            elif self.is_element_visible(self.SEARCH_BUTTON_ALT, timeout=2):
                self.click(self.SEARCH_BUTTON_ALT)
                return
            else:
                # Last resort: try JavaScript click on any element containing "Browse"
                browse_element = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Browse')]")
                if browse_element:
                    self.driver.execute_script("arguments[0].click();", browse_element[0])
                    return
                raise Exception("Search button not found with any locator")
        except Exception as e:
            # Take screenshot for debugging
            self.take_screenshot("search_button_not_found")
            raise e

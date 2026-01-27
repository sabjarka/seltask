"""
Base page class with common methods and explicit waits.
All page objects should inherit from this class.
"""
from typing import Tuple, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By

from config.settings import EXPLICIT_WAIT_TIMEOUT
from utils.helpers import scroll_page, take_screenshot


class BasePage:
    """Base page class containing common methods for all page objects."""

    def __init__(self, driver: WebDriver):
        """
        Initialize the base page.

        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT_TIMEOUT)

    def find_element(self, locator: Tuple[By, str]) -> WebElement:
        """
        Find an element with explicit wait for presence.

        Args:
            locator: Tuple of (By, locator_string)

        Returns:
            WebElement if found

        Raises:
            TimeoutException: If element not found within timeout
        """
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator: Tuple[By, str]) -> List[WebElement]:
        """
        Find all elements matching the locator.

        Args:
            locator: Tuple of (By, locator_string)

        Returns:
            List of WebElements
        """
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator: Tuple[By, str]) -> None:
        """
        Click an element with explicit wait for clickability.

        Args:
            locator: Tuple of (By, locator_string)
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type(self, locator: Tuple[By, str], text: str, clear_first: bool = True) -> None:
        """
        Type text into an input field.

        Args:
            locator: Tuple of (By, locator_string)
            text: Text to type
            clear_first: Whether to clear the field before typing
        """
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: Tuple[By, str]) -> str:
        """
        Get text from an element.

        Args:
            locator: Tuple of (By, locator_string)

        Returns:
            Text content of the element
        """
        element = self.find_element(locator)
        return element.text

    def is_element_visible(self, locator: Tuple[By, str], timeout: int = None) -> bool:
        """
        Check if an element is visible on the page.

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional custom timeout

        Returns:
            True if element is visible, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout or EXPLICIT_WAIT_TIMEOUT)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator: Tuple[By, str]) -> bool:
        """
        Check if an element is present in the DOM.

        Args:
            locator: Tuple of (By, locator_string)

        Returns:
            True if element is present, False otherwise
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def wait_for_element_visible(self, locator: Tuple[By, str], timeout: int = None) -> WebElement:
        """
        Wait for an element to be visible.

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional custom timeout

        Returns:
            WebElement when visible
        """
        wait = WebDriverWait(self.driver, timeout or EXPLICIT_WAIT_TIMEOUT)
        return wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator: Tuple[By, str], timeout: int = None) -> WebElement:
        """
        Wait for an element to be clickable.

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional custom timeout

        Returns:
            WebElement when clickable
        """
        wait = WebDriverWait(self.driver, timeout or EXPLICIT_WAIT_TIMEOUT)
        return wait.until(EC.element_to_be_clickable(locator))

    def wait_for_invisibility(self, locator: Tuple[By, str], timeout: int = None) -> bool:
        """
        Wait for an element to become invisible or be removed from DOM.

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional custom timeout

        Returns:
            True if element becomes invisible
        """
        wait = WebDriverWait(self.driver, timeout or EXPLICIT_WAIT_TIMEOUT)
        return wait.until(EC.invisibility_of_element_located(locator))

    def scroll_down(self, times: int = 1, pixels: int = 800) -> None:
        """
        Scroll down the page multiple times.

        Args:
            times: Number of times to scroll
            pixels: Pixels to scroll each time
        """
        for _ in range(times):
            scroll_page(self.driver, pixels)

    def scroll_to_element(self, locator: Tuple[By, str]) -> None:
        """
        Scroll to make an element visible in viewport.

        Args:
            locator: Tuple of (By, locator_string)
        """
        element = self.find_element(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element
        )

    def take_screenshot(self, name: str = None) -> str:
        """
        Take a screenshot of the current page.

        Args:
            name: Optional name for the screenshot

        Returns:
            Path to saved screenshot
        """
        return take_screenshot(self.driver, name)

    def get_current_url(self) -> str:
        """
        Get the current page URL.

        Returns:
            Current URL
        """
        return self.driver.current_url

    def get_page_title(self) -> str:
        """
        Get the current page title.

        Returns:
            Page title
        """
        return self.driver.title

    def refresh_page(self) -> None:
        """Refresh the current page."""
        self.driver.refresh()

    def handle_modal_if_present(self, modal_locator: Tuple[By, str],
                                close_button_locator: Tuple[By, str],
                                timeout: int = 5) -> bool:
        """
        Handle modal/popup if present by clicking close button.

        Args:
            modal_locator: Locator for the modal element
            close_button_locator: Locator for the close button
            timeout: Time to wait for modal to appear

        Returns:
            True if modal was handled, False if no modal appeared
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(modal_locator))
            self.click(close_button_locator)
            self.wait_for_invisibility(modal_locator, timeout=timeout)
            return True
        except TimeoutException:
            return False

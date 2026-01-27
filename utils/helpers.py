"""
Helper utility functions for the framework.
"""
from datetime import datetime
from pathlib import Path
from typing import Optional

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from config.settings import SCREENSHOTS_DIR


def take_screenshot(driver: WebDriver, name: Optional[str] = None) -> str:
    """
    Take a screenshot and save it to the screenshots directory.

    Args:
        driver: WebDriver instance
        name: Optional name for the screenshot. If not provided, uses timestamp.

    Returns:
        Path to the saved screenshot
    """
    if name is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"screenshot_{timestamp}"

    # Ensure .png extension
    if not name.endswith('.png'):
        name = f"{name}.png"

    screenshot_path = SCREENSHOTS_DIR / name
    driver.save_screenshot(str(screenshot_path))

    return str(screenshot_path)


def scroll_to_element(driver: WebDriver, element) -> None:
    """
    Scroll to make an element visible in the viewport.

    Args:
        driver: WebDriver instance
        element: WebElement to scroll to
    """
    # Use instant scroll to avoid needing time.sleep
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", element)


def scroll_page(driver: WebDriver, pixels: int = 800) -> None:
    """
    Scroll the page by a specified number of pixels.

    Args:
        driver: WebDriver instance
        pixels: Number of pixels to scroll (positive for down, negative for up)
    """
    driver.execute_script(f"window.scrollBy(0, {pixels});")
    # Wait for scroll to complete by checking if scroll position has changed
    wait = WebDriverWait(driver, 2)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")


def get_current_timestamp() -> str:
    """
    Get current timestamp in a readable format.

    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

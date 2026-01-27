"""
WebDriver factory for creating and managing browser instances.
"""
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from config.settings import (
    MOBILE_DEVICES,
    DEFAULT_DEVICE,
    HEADLESS_MODE,
    CHROME_ARGUMENTS,
    PAGE_LOAD_TIMEOUT
)


class DriverFactory:
    """Factory class for creating WebDriver instances."""

    _instance = None

    @staticmethod
    def get_chrome_options(headless: bool = HEADLESS_MODE, device_name: str = DEFAULT_DEVICE) -> Options:
        """
        Configure Chrome options with mobile emulation.

        Args:
            headless: Whether to run in headless mode
            device_name: Name of the mobile device to emulate

        Returns:
            Configured ChromeOptions instance
        """
        chrome_options = Options()

        # Add standard arguments
        for arg in CHROME_ARGUMENTS:
            chrome_options.add_argument(arg)

        # Headless mode
        if headless:
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--window-size=1920,1080")

        # Mobile emulation
        if device_name in MOBILE_DEVICES:
            mobile_emulation = MOBILE_DEVICES[device_name]
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

        # Disable automation flags
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # Additional preferences
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0
        }
        chrome_options.add_experimental_option("prefs", prefs)

        return chrome_options

    @classmethod
    def create_driver(cls, headless: bool = HEADLESS_MODE, device_name: str = DEFAULT_DEVICE) -> webdriver.Chrome:
        """
        Create a new Chrome WebDriver instance with mobile emulation.

        Args:
            headless: Whether to run in headless mode
            device_name: Name of the mobile device to emulate

        Returns:
            Chrome WebDriver instance
        """
        # Get Chrome options
        chrome_options = cls.get_chrome_options(headless=headless, device_name=device_name)

        # Create driver - Selenium Manager will automatically download and manage ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Set timeouts
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

        return driver

    @classmethod
    def get_driver(cls, headless: bool = HEADLESS_MODE, device_name: str = DEFAULT_DEVICE) -> webdriver.Chrome:
        """
        Get WebDriver instance (singleton pattern for session reuse).

        Args:
            headless: Whether to run in headless mode
            device_name: Name of the mobile device to emulate

        Returns:
            Chrome WebDriver instance
        """
        if cls._instance is None:
            cls._instance = cls.create_driver(headless=headless, device_name=device_name)
        return cls._instance

    @classmethod
    def quit_driver(cls) -> None:
        """Quit the WebDriver instance and reset singleton."""
        if cls._instance is not None:
            cls._instance.quit()
            cls._instance = None

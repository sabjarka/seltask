"""
Configuration settings for the Selenium automation framework.
"""
import os
from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).parent.parent

# Base URL
BASE_URL = "https://www.twitch.tv"

# Timeouts (in seconds)
EXPLICIT_WAIT_TIMEOUT = 10
PAGE_LOAD_TIMEOUT = 30
IMPLICIT_WAIT_TIMEOUT = 0  # Not recommended, use explicit waits instead

# Mobile device settings
MOBILE_DEVICES = {
    "iPhone 12 Pro": {
        "deviceName": "iPhone 12 Pro"
    },
    "Pixel 5": {
        "deviceName": "Pixel 5"
    },
    "Custom": {
        "deviceMetrics": {
            "width": 375,
            "height": 812,
            "pixelRatio": 3.0
        },
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    }
}

# Default mobile device
DEFAULT_DEVICE = "iPhone 12 Pro"

# Browser settings
HEADLESS_MODE = False  # Can be overridden by command line argument
CHROME_ARGUMENTS = [
    "--disable-notifications",
    "--disable-popup-blocking",
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]

# Directory paths
SCREENSHOTS_DIR = ROOT_DIR / "screenshots"
REPORTS_DIR = ROOT_DIR / "reports"

# Create directories if they don't exist
SCREENSHOTS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Screenshot settings
SCREENSHOT_ON_FAILURE = True

# Logging
LOG_LEVEL = "INFO"

"""
PyTest configuration and fixtures.
"""
import pytest
from datetime import datetime
from pathlib import Path

from utils.driver_factory import DriverFactory
from config.settings import SCREENSHOTS_DIR, HEADLESS_MODE, DEFAULT_DEVICE


def pytest_addoption(parser):
    """Add custom command-line options for pytest."""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--device-name",
        action="store",
        default=DEFAULT_DEVICE,
        help=f"Mobile device to emulate (default: {DEFAULT_DEVICE})"
    )


@pytest.fixture(scope="session")
def headless(request):
    """Get headless mode from command line or use default."""
    return request.config.getoption("--headless") or HEADLESS_MODE


@pytest.fixture(scope="session")
def device_name(request):
    """Get device name from command line or use default."""
    return request.config.getoption("--device-name")


@pytest.fixture(scope="session")
def driver(headless, device_name):
    """
    Create and provide WebDriver instance for the entire test session.

    This fixture is session-scoped to reuse the same browser instance
    across all tests for better performance.

    Args:
        headless: Whether to run in headless mode
        device_name: Name of mobile device to emulate

    Yields:
        WebDriver instance
    """
    # Create driver
    driver_instance = DriverFactory.create_driver(
        headless=headless,
        device_name=device_name
    )

    yield driver_instance

    # Cleanup: quit driver after all tests
    driver_instance.quit()
    DriverFactory.quit_driver()


@pytest.fixture(scope="function", autouse=True)
def screenshot_on_failure(request, driver):
    """
    Automatically capture screenshot on test failure.

    This fixture runs for every test function and captures a screenshot
    if the test fails.

    Args:
        request: PyTest request object
        driver: WebDriver fixture
    """
    yield

    # Check if test failed
    if request.node.rep_call.failed:
        # Generate screenshot name from test name and timestamp
        test_name = request.node.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"{test_name}_{timestamp}.png"
        screenshot_path = SCREENSHOTS_DIR / screenshot_name

        # Capture screenshot
        try:
            driver.save_screenshot(str(screenshot_path))
            print(f"\n📸 Screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"\n❌ Failed to capture screenshot: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to make test results available to fixtures.

    This allows the screenshot_on_failure fixture to check if a test failed.
    """
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # Set a report attribute for each phase of a call
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="function")
def test_name(request):
    """
    Provide the current test name.

    Args:
        request: PyTest request object

    Returns:
        Test function name
    """
    return request.node.name

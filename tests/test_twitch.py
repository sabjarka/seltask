"""
Test cases for Twitch.tv automation.
"""
import pytest

from pages.twitch_home_page import TwitchHomePage
from pages.twitch_search_page import TwitchSearchPage
from pages.twitch_stream_page import TwitchStreamPage


@pytest.mark.twitch
@pytest.mark.smoke
def test_twitch_starcraft_stream(driver):
    """
    Test case: Search for StarCraft II streams on Twitch.

    Test Steps:
    1. Navigate to twitch.com
    2. Click the search icon
    3. Input "StarCraft II" in search
    4. Scroll down 2 times
    5. Select one streamer
    6. Handle any modals/popups
    7. Verify stream loaded successfully

    Args:
        driver: WebDriver fixture from conftest.py
    """
    # Step 1: Go to twitch.com
    print("\n🎮 Step 1: Navigating to Twitch.com...")
    home_page = TwitchHomePage(driver)
    home_page.open()
    assert "Twitch" in driver.title, "Failed to load Twitch homepage"
    print("✅ Successfully loaded Twitch homepage")

    # Step 2: Click search icon
    print("\n🔍 Step 2: Clicking search icon...")
    home_page.click_search_icon()
    print("✅ Search opened successfully")

    # Step 3: Input "StarCraft II"
    print("\n⌨️  Step 3: Searching for 'StarCraft II'...")
    search_page = TwitchSearchPage(driver)
    search_page.search_for("StarCraft II")
    print("✅ Search query submitted")

    # Step 4: Scroll down 2 times
    print("\n📜 Step 4: Scrolling down to see more results...")
    search_page.scroll_down(times=2)
    print("✅ Scrolled down 2 times")

    # Step 5: Select one streamer (first available)
    print("\n🎯 Step 5: Selecting a streamer...")
    search_page.select_streamer(index=0)
    print("✅ Streamer selected and clicked")

    # Step 6: Handle modal/popup if present
    print("\n🚪 Step 6: Handling any modals/popups...")
    stream_page = TwitchStreamPage(driver)
    stream_page.handle_modals()
    print("✅ Modals handled")

    # Step 7: Verify stream loaded
    print("\n📺 Step 7: Verifying stream loaded...")
    stream_page.verify_stream_loaded()
    print("✅ Stream loaded successfully!")

    # Additional verification
    current_url = driver.current_url
    assert "twitch.tv" in current_url, f"Not on Twitch domain: {current_url}"

    print("\n🎉 Test completed successfully!")


@pytest.mark.twitch
def test_twitch_homepage_loads(driver):
    """
    Simple smoke test to verify Twitch homepage loads.

    Args:
        driver: WebDriver fixture
    """
    print("\n🏠 Testing Twitch homepage loading...")
    home_page = TwitchHomePage(driver)
    home_page.open()

    # Verify page title
    assert "Twitch" in driver.title, "Twitch homepage title not found"

    # Verify we're on the correct URL
    assert "twitch.tv" in driver.current_url, "Not on Twitch domain"

    print("✅ Twitch homepage loaded successfully!")


@pytest.mark.twitch
def test_twitch_search_opens(driver):
    """
    Test that search functionality can be accessed.

    Args:
        driver: WebDriver fixture
    """
    print("\n🔎 Testing search functionality...")
    home_page = TwitchHomePage(driver)
    home_page.open()

    # Click search
    home_page.click_search_icon()

    # Verify search input is visible
    search_page = TwitchSearchPage(driver)
    assert search_page.is_element_visible(search_page.SEARCH_INPUT, timeout=5) or \
           search_page.is_element_visible(search_page.SEARCH_INPUT_ALT, timeout=2) or \
           search_page.is_element_visible(search_page.SEARCH_INPUT_ALT2, timeout=2), \
           "Search input not visible"

    print("✅ Search functionality accessible!")

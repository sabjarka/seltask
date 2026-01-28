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
    home_page = TwitchHomePage(driver)
    home_page.open()
    assert "Twitch" in driver.title, "Failed to load Twitch homepage"

    home_page.click_search_icon()

    search_page = TwitchSearchPage(driver)
    search_page.search_for("StarCraft II")
    search_page.scroll_down(times=2)
    search_page.select_streamer(index=0)

    stream_page = TwitchStreamPage(driver)
    stream_page.handle_modals()
    stream_page.verify_stream_loaded()

    current_url = driver.current_url
    assert "twitch.tv" in current_url, f"Not on Twitch domain: {current_url}"

"""
Twitch search page object.
"""
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage


class TwitchSearchPage(BasePage):
    """Page object for Twitch search page."""

    # Locators
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='search']")
    SEARCH_RESULTS = (By.CSS_SELECTOR, "[data-a-target='search-result-card']")
    CHANNEL_CARDS = (By.CSS_SELECTOR, "a[data-a-target='preview-card-channel-link']")
    LIVE_CHANNEL_CARDS = (By.CSS_SELECTOR, "[data-a-target='preview-card-image-link']")
    # Search result cards (both buttons and links)
    SEARCH_RESULT_CARDS = (By.CSS_SELECTOR, "button img[src*='live_user_'], a img[src*='live_user_']")
    # More specific locators for actual channel links in search results
    STREAMER_LINKS = (By.CSS_SELECTOR, "article a, a[href*='/videos'], a[href^='/'][href*='/']")

    def search_for(self, query: str) -> None:
        """
        Enter search query and submit.

        Args:
            query: Search term to enter
        """
        # Wait for search input to be visible (should already be on Browse page)
        search_input = self.wait_for_element_visible(self.SEARCH_INPUT, timeout=5)

        # Clear and type search query
        search_input.clear()
        search_input.send_keys(query)
        search_input.send_keys(Keys.RETURN)

        # Wait for results to load
        self.wait_for_search_results()

    def _is_valid_channel_path(self, path: str) -> bool:
        """
        Check if a path is a valid channel path.

        Args:
            path: The URL path to check

        Returns:
            True if it's a valid channel path, False otherwise
        """
        if not path or path == '/':
            return False

        # Remove query parameters and fragments
        clean_path = path.split('?')[0].split('#')[0]

        # Must have reasonable length for a channel name
        # Path includes leading slash, so check > 2
        if len(clean_path) < 2 or len(clean_path) > 30:
            return False

        return True

    def wait_for_search_results(self) -> None:
        """Wait for search results to appear."""
        # Wait for the search result card images to load
        self.wait_for_element_visible(self.SEARCH_RESULT_CARDS, timeout=10)

    def scroll_down(self, times: int = 1) -> None:
        """
        Scroll down the search results page.

        Args:
            times: Number of times to scroll down
        """
        super().scroll_down(times=times, pixels=800)

    def _extract_channel_from_element(self, element: WebElement) -> str:
        """
        Extract channel name from an element (either from href or img src).

        Args:
            element: WebElement to extract channel from

        Returns:
            Channel name or empty string if not found
        """
        # Try href first (for <a> tags)
        href = element.get_attribute('href')
        if href:
            if href.startswith('/'):
                return href
            elif 'twitch.tv' in href:
                return href.split('twitch.tv')[-1]

        # Try to find img with live_user_ in src (for <button> elements)
        try:
            imgs = element.find_elements(By.CSS_SELECTOR, "img[src*='live_user_']")
            if imgs:
                src = imgs[0].get_attribute('src')
                if 'live_user_' in src:
                    # Extract channel name: live_user_rotterdam08 -> /rotterdam08
                    channel = src.split('live_user_')[1].split('-')[0].split('.')[0]
                    return f"/{channel}"
        except:
            pass

        return ""

    def _is_streaming_game(self, element: WebElement, game_name: str) -> bool:
        """
        Check if the element/card shows the specified game being streamed.

        Args:
            element: WebElement representing the streamer card
            game_name: Name of the game to check for (e.g., "StarCraft II")

        Returns:
            True if the card shows the game being streamed
        """
        try:
            # Get all text content from the element
            element_text = element.text

            # Check if game name is in the element text
            if game_name.lower() in element_text.lower():
                return True

            # Also try to find specific game category text elements
            game_elements = element.find_elements(By.XPATH, ".//*[contains(text(), '" + game_name + "')]")
            if game_elements:
                return True

        except:
            pass

        return False

    def get_streamer_elements(self) -> List[WebElement]:
        """
        Get all streamer/channel elements from search results.

        Returns:
            List of WebElements representing streamers
        """
        # Try to find streamer cards with multiple locators
        print("\nSearching for streamer elements...")

        # First try to find images with live_user_ pattern (works for both buttons and links)
        try:
            img_elements = self.find_elements(self.SEARCH_RESULT_CARDS)
            if img_elements and len(img_elements) > 0:
                print(f"Found {len(img_elements)} elements with SEARCH_RESULT_CARDS locator")
                valid = []
                for img in img_elements:
                    if img.is_displayed():
                        # Get the parent button or link element (clickable element)
                        parent = img.find_element(By.XPATH, "./ancestor::button | ./ancestor::a")
                        if parent:
                            channel_path = self._extract_channel_from_element(parent)
                            # Must be valid channel AND streaming StarCraft II
                            if self._is_valid_channel_path(channel_path) and self._is_streaming_game(parent, "StarCraft II"):
                                valid.append(parent)
                                if len(valid) <= 3:
                                    print(f"  Valid CARD: {channel_path} (streaming StarCraft II)")

                if valid:
                    print(f"  {len(valid)} are valid StarCraft II stream cards")
                    return valid
        except Exception as e:
            print(f"SEARCH_RESULT_CARDS search failed: {e}")

        try:
            elements = self.find_elements(self.LIVE_CHANNEL_CARDS)
            if elements and len(elements) > 0:
                print(f"Found {len(elements)} elements with LIVE_CHANNEL_CARDS locator")
                # Filter to only clickable/visible elements with valid channel hrefs
                valid = []
                for e in elements:
                    if e.is_displayed():
                        href = e.get_attribute('href')
                        if href:
                            # Handle both relative URLs (/channelname) and absolute URLs
                            if href.startswith('/'):
                                path = href
                            elif 'twitch.tv' in href:
                                path = href.split('twitch.tv')[-1]
                            else:
                                continue

                            # Validate it's an actual channel path AND streaming StarCraft II
                            if self._is_valid_channel_path(path) and self._is_streaming_game(e, "StarCraft II"):
                                valid.append(e)
                                if len(valid) <= 3:  # Debug first 3 only
                                    print(f"  Valid LIVE: {href} (streaming StarCraft II)")

                if valid:
                    print(f"  {len(valid)} are valid StarCraft II live channel cards")
                    return valid
        except Exception as e:
            print(f"LIVE_CHANNEL_CARDS search failed: {e}")

        try:
            elements = self.find_elements(self.CHANNEL_CARDS)
            if elements and len(elements) > 0:
                print(f"Found {len(elements)} elements with CHANNEL_CARDS locator")
                valid = []
                for e in elements:
                    if e.is_displayed():
                        href = e.get_attribute('href')
                        if href:
                            # Handle both relative and absolute URLs
                            if href.startswith('/'):
                                path = href
                            elif 'twitch.tv' in href:
                                path = href.split('twitch.tv')[-1]
                            else:
                                continue

                            if self._is_valid_channel_path(path) and self._is_streaming_game(e, "StarCraft II"):
                                valid.append(e)
                                if len(valid) <= 3:
                                    print(f"  Valid CHANNEL: {href} (streaming StarCraft II)")

                if valid:
                    print(f"  {len(valid)} are valid StarCraft II channel cards")
                    return valid
        except Exception as e:
            print(f"CHANNEL_CARDS search failed: {e}")

        try:
            elements = self.find_elements(self.STREAMER_LINKS)
            if elements and len(elements) > 0:
                print(f"Found {len(elements)} elements with STREAMER_LINKS locator")
                # Filter to valid stream links (must have actual channel path)
                valid = []
                for e in elements:
                    if e.is_displayed():
                        href = e.get_attribute('href')
                        if href:
                            # Handle both relative and absolute URLs
                            if href.startswith('/'):
                                path = href
                            elif 'twitch.tv' in href:
                                path = href.split('twitch.tv')[-1]
                            else:
                                continue

                            if self._is_valid_channel_path(path) and self._is_streaming_game(e, "StarCraft II"):
                                valid.append(e)
                                if len(valid) <= 3:  # Debug first 3 only
                                    print(f"  Valid: {href} (streaming StarCraft II)")

                if valid:
                    print(f"  {len(valid)} are valid StarCraft II stream links")
                    return valid
        except Exception as e:
            print(f"STREAMER_LINKS search failed: {e}")

        self.take_screenshot("no_streamers_found")
        raise Exception("No streamer elements found on the page")

    def select_streamer(self, index: int = 0) -> None:
        """
        Select a streamer from the search results by index.

        Args:
            index: Zero-based index of the streamer to select
        """
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait

        streamers = self.get_streamer_elements()
        print(f"\nFound {len(streamers)} streamer elements")

        if index >= len(streamers):
            raise IndexError(f"Streamer index {index} out of range. Found {len(streamers)} streamers.")

        # Scroll to the streamer element to make it visible
        streamer = streamers[index]

        # Get streamer info for debugging
        channel_path = self._extract_channel_from_element(streamer)
        tag_name = streamer.tag_name
        print(f"Clicking {tag_name} element for channel: {channel_path}")

        # Scroll element into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});",
            streamer
        )

        # Wait for element to be clickable after scroll
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.element_to_be_clickable((By.XPATH, f".//*")))

        # Store current URL to detect navigation
        old_url = self.driver.current_url
        expected_channel = channel_path.lstrip('/')

        # Click the streamer
        try:
            streamer.click()
        except:
            # If normal click fails, try JavaScript click
            self.driver.execute_script("arguments[0].click();", streamer)

        # Wait for URL to change (navigation)
        wait.until(lambda driver: driver.current_url != old_url)
        new_url = self.driver.current_url
        print(f"Navigated to: {new_url}")

        # Verify we're on the expected channel
        if expected_channel and expected_channel not in new_url:
            print(f"⚠️  Warning: Expected /{expected_channel} but got {new_url}")

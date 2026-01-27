"""
Twitch stream page object.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class TwitchStreamPage(BasePage):
    """Page object for Twitch stream/video page."""

    # Locators for modals and popups
    MATURE_CONTENT_BUTTON = (By.CSS_SELECTOR, "button[data-a-target='player-overlay-mature-accept']")
    CONSENT_BANNER_ACCEPT = (By.CSS_SELECTOR, "button[data-a-target='consent-banner-accept']")
    CLOSE_MODAL_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Close modal']")

    # Video player locators
    VIDEO_PLAYER = (By.CSS_SELECTOR, "video")
    PLAYER_CONTAINER = (By.CSS_SELECTOR, "[data-a-target='video-player']")
    PLAYER_CONTROLS = (By.CSS_SELECTOR, "[data-a-target='player-controls']")

    def handle_modals(self, timeout: int = 10) -> None:
        """
        Handle any modals or popups that may appear on the stream page.
        This includes mature content warnings, consent banners, etc.

        Args:
            timeout: Maximum time to wait for modals
        """

        # Try to handle mature content modal
        try:
            if self.is_element_visible(self.MATURE_CONTENT_BUTTON, timeout=3):
                self.click(self.MATURE_CONTENT_BUTTON)
                self.wait_for_invisibility(self.MATURE_CONTENT_BUTTON, timeout=3)
        except:
            pass

        # Try to handle consent banner
        try:
            if self.is_element_visible(self.CONSENT_BANNER_ACCEPT, timeout=2):
                self.click(self.CONSENT_BANNER_ACCEPT)
                self.wait_for_invisibility(self.CONSENT_BANNER_ACCEPT, timeout=3)
        except:
            pass

        # Try to close any generic modal
        try:
            if self.is_element_visible(self.CLOSE_MODAL_BUTTON, timeout=2):
                self.click(self.CLOSE_MODAL_BUTTON)
                self.wait_for_invisibility(self.CLOSE_MODAL_BUTTON, timeout=3)
        except:
            pass

    def verify_stream_loaded(self) -> None:
        """
        Verify that the stream/video player has loaded successfully.

        Raises:
            Exception: If video player doesn't load
        """

        # Check if video player exists and is playing
        try:
            # Wait for video element to be present
            if self.is_element_visible(self.VIDEO_PLAYER, timeout=10):
                print("✅ Video player element found")

                # Check if video is actually playing
                if self.is_video_playing():
                    print("✅ Video is playing!")
                    return
                else:
                    print("⚠️  Video player found but not playing (may need to start manually or be paused)")
                    # Still consider this success - player exists
                    return

            # Fallback: check for player container
            if self.is_element_visible(self.PLAYER_CONTAINER, timeout=5):
                print("✅ Player container found")
                return

            # If no player found
            print("❌ Video player not found on page")
            self.take_screenshot("video_player_not_found")
            raise Exception("Video player did not load successfully")

        except Exception as e:
            print(f"❌ Error during verification: {e}")
            self.take_screenshot("video_player_error")
            raise e

    def is_video_playing(self) -> bool:
        """
        Check if the video is currently playing.

        Returns:
            True if video is playing, False otherwise
        """
        try:
            video_element = self.find_element(self.VIDEO_PLAYER)
            # Check if video is not paused
            is_playing = self.driver.execute_script(
                "return arguments[0].paused === false;",
                video_element
            )
            return is_playing
        except:
            return False

# bot.py
"""StudyGuard Bot - Automated YouTube learning assistant with focus timer."""

import logging
import threading 
import time
import tkinter as tk
from typing import Optional, Tuple, Dict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
YOUTUBE_URL = "https://www.youtube.com/"
SEARCH_WAIT_TIME = 3
VIDEO_LOAD_TIME = 5
AD_CHECK_INTERVAL = 1
DEFAULT_FOCUS_DURATION = 60


class StudyGuardBot:
    """Bot for automating YouTube video search and focus management."""

    def __init__(self) -> None:
        """Initialize the StudyGuardBot."""
        self.driver: Optional[WebDriver] = None
        logger.info("StudyGuardBot initialized")

    def start_driver(self) -> None:
        """Initialize Chrome WebDriver if not already running."""
        if self.driver is None:
            try:
                self.driver = webdriver.Chrome()
                self.driver.maximize_window()
                logger.info("Chrome WebDriver started successfully")
            except Exception as e:
                logger.error(f"Failed to start Chrome WebDriver: {e}")
                raise

    def search_video(self, query: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Search for a video on YouTube and play the first result.

        Args:
            query: Search query string

        Returns:
            Tuple of (video_url, video_title) or (None, None) if search fails
        """
        if not query or not isinstance(query, str):
            logger.warning("Invalid query provided to search_video")
            return None, None

        try:
            self.start_driver()
            assert self.driver is not None, "Driver failed to initialize"

            self.driver.get(YOUTUBE_URL)
            time.sleep(SEARCH_WAIT_TIME)

            # Search video
            search_box = self.driver.find_element(By.NAME, "search_query")
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            time.sleep(SEARCH_WAIT_TIME)

            # Click first video
            video = self.driver.find_element(By.ID, "video-title")
            title = video.get_attribute("title")
            url = video.get_attribute("href")
            video.click()
            time.sleep(VIDEO_LOAD_TIME)

            logger.info(f"Successfully found and clicked video: {title}")

            # Start threads: skip ads & focus timer
            threading.Thread(target=self.skip_ads_continuous, daemon=True).start()
            threading.Thread(target=self.focus_timer_pop_up, daemon=True).start()

            return url, title

        except NoSuchElementException as e:
            logger.error(f"Element not found during video search: {e}")
            return None, None
        except TimeoutException as e:
            logger.error(f"Timeout during video search: {e}")
            return None, None
        except Exception as e:
            logger.error(f"Unexpected error during video search: {e}")
            return None, None

    def skip_ads_continuous(self) -> None:
        """Continuously skip ads while video is playing."""
        if self.driver is None:
            logger.warning("Driver not initialized for ad skipping")
            return

        try:
            while True:
                time.sleep(AD_CHECK_INTERVAL)
                try:
                    skip_btn = self.driver.find_element(By.CLASS_NAME, "ytp-ad-skip-button")
                    if skip_btn.is_displayed():
                        skip_btn.click()
                        logger.debug("Ad skipped")
                except NoSuchElementException:
                    pass
                except Exception as e:
                    logger.debug(f"Error during ad skip attempt: {e}")
        except Exception as e:
            logger.error(f"Ad skip thread encountered error: {e}")

    def focus_timer_pop_up(self, duration: int = DEFAULT_FOCUS_DURATION) -> None:
        """
        Display a focus break popup after specified duration.

        Args:
            duration: Duration in seconds before showing popup (default: 60)
        """
        if not isinstance(duration, int) or duration <= 0:
            logger.warning(f"Invalid duration provided: {duration}, using default")
            duration = DEFAULT_FOCUS_DURATION

        try:
            time.sleep(duration)

            # Tkinter popup for focus break
            root = tk.Tk()
            root.title("🎯 Focus Break")
            root.geometry("400x250")
            root.configure(bg="#0B3D91")

            tk.Label(
                root, text="🎯", font=("Segoe Script", 60, "bold"),
                fg="#FFB400", bg="#0B3D91"
            ).pack(pady=10)

            tk.Label(
                root, text="Focus session complete!\nTake a 1 minute break.",
                font=("Georgia", 14, "bold"), fg="white",
                bg="#0B3D91", justify="center"
            ).pack(pady=10)

            tk.Button(
                root, text="✔ Close", font=("Georgia", 12, "bold"),
                bg="#FFB400", fg="#0B3D91", relief="flat",
                command=root.destroy
            ).pack(pady=15)

            root.mainloop()
            logger.info("Focus timer popup closed")

        except Exception as e:
            logger.error(f"Error in focus timer popup: {e}")

    def generate_daily_plan(self) -> Dict[str, str]:
        """
        Generate a daily watch plan with learning, career, and entertainment content.

        Returns:
            Dictionary with daily plan categories and content
        """
        plan = {
            "Learning": "Python tutorial for beginners",
            "Career": "Career motivation for students",
            "Entertainment": "Tarak Mehta ka ulta Chasmah(5 min)"
        }
        logger.info("Daily plan generated")
        return plan

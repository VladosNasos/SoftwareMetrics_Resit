"""Module to perform Selenium-based infinite scroll tests using unittest.

This module contains a test suite that verifies the infinite scroll functionality
on a sample webpage using Selenium WebDriver and Python's unittest framework.
"""

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class InfiniteScrollTest(unittest.TestCase):
    """Test suite for verifying infinite scroll functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up the Selenium WebDriver before any tests are run."""
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.url = "https://the-internet.herokuapp.com/infinite_scroll"

    def test_scroll_behavior(self):
        """Test if scrolling loads new content on the webpage.

        This test navigates to the infinite scroll page, verifies the page header,
        takes a screenshot before scrolling, performs a scroll action, waits
        for new content to load, takes another screenshot, and finally checks that
        new content has been loaded after scrolling.
        """
        driver = self.driver
        driver.get(self.url)

        page_header = driver.find_element(By.CSS_SELECTOR, '#content h3')
        self.assertIn("Infinite Scroll", page_header.text, "Page header text mismatch.")

        driver.save_screenshot('before_scroll.png')

        initial_count = len(driver.find_elements(By.CLASS_NAME, 'jscroll-added'))

        actions = ActionChains(driver)
        actions.move_to_element(driver.find_element(By.TAG_NAME, 'footer')).perform()
        time.sleep(3)

        driver.save_screenshot('after_scroll.png')

        updated_count = len(driver.find_elements(By.CLASS_NAME, 'jscroll-added'))

        self.assertGreater(updated_count, initial_count, "New content was not loaded after scrolling.")

    @classmethod
    def tearDownClass(cls):
        """Quit the Selenium WebDriver after all tests have run."""
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

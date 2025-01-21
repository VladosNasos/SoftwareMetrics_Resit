"""Example module demonstrating performance metric collection and processing tests."""

import unittest
import json
import logging
from collections import defaultdict

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By

# Logging configuration for debug output
logging.basicConfig(level=logging.DEBUG)

# Constants
TEST_URL = "https://en.wikipedia.org/wiki/Software_metric"
REPEAT_COUNT = 10


class PerformanceMetricsTest(unittest.TestCase):
    """Tests for collecting and processing performance metrics from a webpage."""

    def setUp(self):
        """Set up test variables and environment."""
        self.target_url = TEST_URL
        self.num_cycles = REPEAT_COUNT

    def _collect_performance_data(self):
        """
        Collect performance entries from the target URL over multiple runs.

        Returns:
            dict: A dictionary mapping resource names to lists of durations.
        """
        url_performance_data = defaultdict(list)

        for _ in range(self.num_cycles):
            options = webdriver.ChromeOptions()
            options.add_argument("--incognito")
            browser = webdriver.Chrome(options=options)

            browser.get(self.target_url)
            heading_element = browser.find_element(By.CSS_SELECTOR, "#firstHeading > span")
            self.assertIn("Software metric", heading_element.text)

            perf_script = (
                "return window.performance.getEntries().map(item => [item.name, item.duration])"
            )
            collected_entries = browser.execute_script(perf_script)

            for entry_name, duration in collected_entries:
                url_performance_data[entry_name].append(duration)

            browser.quit()

        return url_performance_data

    @staticmethod
    def _save_json_file(filename, data):
        """
        Save a dictionary as a JSON file.

        Args:
            filename (str): Path to the output JSON file.
            data (dict): Data to save.
        """
        with open(filename, "w", encoding="utf8") as file_obj:
            json.dump(data, file_obj, indent=4)

    @staticmethod
    def _calculate_nonzero_average(values):
        """
        Calculate the average of non-zero values in the given list.

        Args:
            values (list): List of numeric values.

        Returns:
            float: Average of non-zero values, or 0 if none are non-zero.
        """
        filtered = [val for val in values if val != 0]
        if not filtered:
            return 0
        return sum(filtered) / len(filtered)

    def test_metrics_collection_and_processing(self):
        """Collect performance data, verify samples, compute averages, and validate results."""
        url_performance_data = self._collect_performance_data()

        first_key = next(iter(url_performance_data))
        self.assertEqual(len(url_performance_data[first_key]), self.num_cycles)

        self._save_json_file("dataMap.json", url_performance_data)

        sample_values = [1, 2, 3, 4, 5]  # Expect average of 3
        sample_avg = self._calculate_nonzero_average(sample_values)
        self.assertEqual(sample_avg, 3)

        average_results = defaultdict(list)
        for entry_name, durations in url_performance_data.items():
            avg_val = self._calculate_nonzero_average(durations)
            average_results[entry_name].append(avg_val)

        first_avg_key = next(iter(average_results))
        self.assertEqual(len(average_results[first_avg_key]), 1)

        self._save_json_file("processedMap.json", average_results)

    def tearDown(self):
        """Clean up after tests."""
        print("Test series completed.")


if __name__ == "__main__":
    unittest.main()

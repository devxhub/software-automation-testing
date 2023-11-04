import unittest
import time
import os  # Import the 'os' module
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import xmlrunner  # Import the 'xmlrunner' library

class TestDevxHub(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://devxhub.com")
        self.driver.maximize_window()

    def test_title(self):
        expected_title = "DevxHub"
        actual_title = self.driver.title
        self.assertEqual(expected_title, actual_title)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    report_dir = "test-reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f"DevxHubTestReport_{now}.xml"

    suite = unittest.TestLoader().loadTestsFromTestCase(TestDevxHub)

    with open(os.path.join(report_dir, report_name), "wb") as output:
        runner = xmlrunner.XMLTestRunner(output=output, verbosity=2)
        runner.run(suite)

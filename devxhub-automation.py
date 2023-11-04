import os
import unittest
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from HtmlTestRunner import HTMLTestRunner
from zapv2 import ZAPv2

class TestDevxHub(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger(cls.__name__)
        cls.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Log to a file
        file_handler = logging.FileHandler('test.log')
        file_handler.setFormatter(formatter)
        cls.logger.addHandler(file_handler)

        # Load configuration from a JSON file
        with open("config.json") as config_file:
            config = json.load(config_file)

        cls.browser = config["browser"]
        cls.driver = cls.setup_driver(cls.browser)
        cls.driver.get(config["base_url"])
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)

    @classmethod
    def setup_driver(cls, browser):
        if browser == "chrome":
            return webdriver.Chrome()
        elif browser == "firefox":
            return webdriver.Firefox()
        else:
            raise Exception("Invalid browser specified in the configuration.")

    def test_title(self):
        self.logger.info("Running test_title")
        self.wait.until(EC.title_contains("DevxHub"))
        actual_title = self.driver.title
        self.assertEqual("DevxHub", actual_title, "Page title does not match the expected title")

    def test_boundary_value(self):
        self.logger.info("Running test_boundary_value")
        # Example of a boundary test (assuming some boundary condition)
        self.wait.until(EC.presence_of_element_located((By.ID, "boundaryElement")))
        # Perform a test for a boundary condition here
        # self.assertEqual(result, expected_result, "Test failed")

    def test_negative_case(self):
        self.logger.info("Running test_negative_case")
        # Example of a negative test case
        self.wait.until(EC.presence_of_element_located((By.ID, "nonExistentElement")))
        # Perform a negative test here
        # self.assertTrue(condition, "Test failed")

    def test_performance(self):
        self.logger.info("Running test_performance")
        # Implement performance testing here (e.g., page load time, response time)
        # You can use libraries like Selenium performance plugin or JMeter for more advanced performance testing.

    def test_security(self):
        self.logger.info("Running test_security")
        # Initialize ZAP proxy
        zap = ZAPv2()
        # Implement security testing using ZAP or another security testing tool

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    report_dir = "test-reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f"DevxHubTestReport_{now}.html"

    suite = unittest.TestLoader().loadTestsFromTestCase(TestDevxHub)

    # Create an HTMLTestRunner object with the custom report title and verbosity set to 2
    runner = HTMLTestRunner(output=report_dir, report_title="DEVxHUB Automation Testing Report", verbosity=2)

    # Run the test suite and save the report as an HTML file
    result = runner.run(suite)

    # Calculate and display the overall test suite success message
    if result.wasSuccessful():
        print("All tests passed successfully.")
    else:
        print("Some tests failed. Check the test reports for details.")

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

# Define a custom HTMLTestRunner with a custom title
class CustomHTMLTestRunner(HTMLTestRunner):
    def _generate_report_name(self):
        return self.report_name

    class CustomHTMLTestRunner(HTMLTestRunner):
        def __init__(self, **kwargs):
            super(CustomHTMLTestRunner, self).__init__(**kwargs)
            self.title = 'DEVxHUB Automation Testing Report'  # Custom report title

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

        cls.base_url = config["base_url"]  # Store base_url for later use
        cls.browser = config["browser"]
        cls.driver = cls.setup_driver(cls.browser)
        cls.driver.get(cls.base_url)
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

    def create_scenario(self, scenario_name):
        scenario_report = self.subTest(scenario_name=scenario_name)
        scenario_report.report_title = f"{self.__class__.__name__} - {scenario_name}"
        return scenario_report

    def test_boundary_value(self):
        with self.create_scenario("Boundary Value Testing"):
            self.logger.info("Running test_boundary_value")
            boundary_element = self.wait.until(EC.presence_of_element_located((By.ID, "boundaryElement")))
            self.assertTrue(self.is_boundary_condition_satisfied(boundary_element), "Boundary test failed")

    def test_negative_case(self):
        with self.create_scenario("Negative Test Cases"):
            self.logger.info("Running test_negative_case")
            non_existent_element = self.wait.until(EC.presence_of_element_located((By.ID, "nonExistentElement")))
            self.assertTrue(self.is_negative_scenario_successful(non_existent_element), "Negative test failed")

    def test_performance(self):
        with self.create_scenario("Performance Testing"):
            self.logger.info("Running test_performance")
            # Implement performance testing using a performance testing tool or library
            # Example: Use Locust to simulate load and measure response times

    def test_security(self):
        with self.create_scenario("Security Testing"):
            self.logger.info("Running test_security")
            # Initialize ZAP proxy or other security testing tools
            # Perform various security tests, like scanning for vulnerabilities and penetration testing

    def test_open_website_and_scenario1(self):
        with self.create_scenario("Scenario 1 - Open Website"):
            self.logger.info("Opening the target website")
            self.driver.get(self.base_url)
            # Add assertions or verifications if needed

    def test_scroll_to_footer_and_scenario2(self):
        with self.create_scenario("Scenario 2 - Scroll to Footer"):
            self.logger.info("Scrolling to the footer")
            footer_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__nuxt"]/div/div[2]/section/div[2]/div/div/div')))
            self.driver.execute_script("arguments[0].scrollIntoView();", footer_element)
            # Add assertions or verifications if needed

    def test_click_company_dropdown_and_scenario3(self):
        with self.create_scenario("Scenario 3 - Click Company Dropdown"):
            self.logger.info("Clicking on the Company Dropdown Button")
            company_dropdown_button = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__nuxt"]/div/div[1]/div/div/ul/li[1]/p/span')))
            company_dropdown_button.click()
            # Add assertions or verifications if needed

    def test_click_career_button_and_scenario4(self):
        with self.create_scenario("Scenario 4 - Click Career Button"):
            self.logger.info("Navigating directly to the Career Page URL")
            career_url = "https://devxhub.com/career"
            self.driver.get(career_url)
            # Add assertions or verifications if needed

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    report_dir = "test-reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")  # Replace colons with hyphens
    report_name = f"DevxHubTestReport_{now}.html"

    suite = unittest.TestLoader().loadTestsFromTestCase(TestDevxHub)

    # Create a custom HTMLTestRunner object with custom title
    runner = CustomHTMLTestRunner(
        output=report_dir,
        report_name=report_name,
        stream=open(os.devnull, 'w'),  # Disable stdout during the test run
        descriptions="Detailed Test Results by Scenario",
        combine_reports=True,  # Combine results of subtests into a single report
        add_timestamp=True,  # Add timestamp to the report
        open_in_browser=True,  # Open the report in the default web browser
    )

    # Run the test suite and save the report as an HTML file
    result = runner.run(suite)

    # Calculate and display the overall test suite success message
    if result.wasSuccessful():
        print("All tests passed successfully.")
    else:
        print("Some tests failed. Check the test reports for details.")

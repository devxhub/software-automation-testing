import os
import unittest
import logging
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Set up logging
log_filename = "test.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TestDevxHub(unittest.TestCase):
    def setUp(self):
        # Load configuration from a JSON file
        with open("config.json") as config_file:
            config = json.load(config_file)

        browser = config["browser"]
        self.driver = self.setup_driver(browser)
        self.driver.get(config["base_url"])
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def setup_driver(self, browser):
        if browser == "chrome":
            return webdriver.Chrome()
        elif browser == "firefox":
            return webdriver.Firefox()
        else:
            raise Exception("Invalid browser specified in the configuration.")

    def test_title(self):
        self.wait.until(EC.title_contains("DevxHub"))
        actual_title = self.driver.title
        self.assertEqual("DevxHub", actual_title, "Page title does not match the expected title")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    report_dir = "test-reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f"DevxHubTestReport_{now}.html"

    suite = unittest.TestLoader().loadTestsFromTestCase(TestDevxHub)

    # Define custom report variables
    test_results = []

    with open(os.path.join(report_dir, report_name), "w", encoding="utf-8") as output:
        custom_title = "Software Automation Testing Contributor Program by DEVxHUB 2023"
        custom_report = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>{custom_title}</title>
        </head>
        <body>
            <h1>{custom_title}</h1>
            <p>Test Results:</p>
            <table>
                <tr>
                    <th>Test Case</th>
                    <th>Result</th>
                </tr>
        '''

        output.write(custom_report)

        for test in suite:
            result = unittest.TextTestResult(output, descriptions=True, verbosity=2)
            test(result)
            status = "Passed" if result.wasSuccessful() else "Failed"
            test_results.append((test, status))

        for test, status in test_results:
            custom_report = f'''
                <tr>
                    <td>{test.id()}</td>
                    <td>{status}</td>
                </tr>
            '''
            output.write(custom_report)

        custom_report = '''
            </table>
        </body>
        </html>
        '''

        output.write(custom_report)

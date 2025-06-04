import json
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Load test data from JSON file once
with open('test_data.json') as f:
    test_data = json.load(f)

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")
    service = Service('/usr/local/bin/chromedriver')  # explicitly use existing chromedriver
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def test_amazon_login_page_elements(driver):
    driver.get("https://www.amazon.com/ap/signin")
    assert "Amazon Sign-In" in driver.title
    email_input = driver.find_element(By.ID, "ap_email")
    assert email_input.is_displayed()
    continue_button = driver.find_element(By.ID, "continue")
    assert continue_button.is_displayed()

def test_amazon_login_invalid_email(driver):
    driver.get("https://www.amazon.com/ap/signin")
    email_input = driver.find_element(By.ID, "ap_email")
    email_input.send_keys(test_data["invalid_email"])
    continue_button = driver.find_element(By.ID, "continue")
    continue_button.click()
    time.sleep(2)
    error_msg = driver.find_element(By.CSS_SELECTOR, "div.a-alert-content")
    assert "Enter your email or mobile phone number" in error_msg.text or "We cannot find an account" in error_msg.text


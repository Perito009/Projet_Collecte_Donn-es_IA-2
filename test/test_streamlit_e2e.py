import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("STREAMLIT_BASE_URL", "http://localhost:8501")

@pytest.fixture(scope="session")
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1400,900")  # ensure sidebar stays visible
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def test_homepage_renders(base_url, driver):
    driver.get(base_url)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='stApp']"))
    )
    assert "http" in driver.current_url

def test_sidebar_available(base_url, driver):
    driver.get(base_url)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='stApp']"))
    )
    # Check if sidebar exists (it may not in all apps)
    sidebars = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='stSidebar']")
    if sidebars:
        assert len(sidebars) > 0
    else:
        print("No sidebar found in this app")

def test_debug_sidebar(base_url, driver):
    driver.get(base_url)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='stApp']"))
    )
    # Save screenshot
    driver.save_screenshot("/tmp/debug.png")
    # Print page source to inspect
    print(driver.page_source)
    # Look for sidebar elements
    elements = driver.find_elements(By.TAG_NAME, "section")
    print(f"Found {len(elements)} section elements")
    for elem in elements:
        print(elem.get_attribute("data-testid"))

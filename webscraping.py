from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector
import json
import time

# Step 1: Configure Selenium WebDriver
options = Options()
options.headless = True  # Run in headless mode (no GUI)
options.add_argument("--window-size=1920,1080")  # Set browser window size
options.add_argument("--disable-extensions")  # Disable extensions for better performance
options.add_argument("--disable-gpu")  # Disable GPU to avoid errors in headless mode
options.add_argument("start-maximized")  # Start browser maximized
options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection

# Disable images to improve performance
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

# Initialize the driver
driver = webdriver.Chrome(options=options)

try:
    # Step 2: Navigate to the Twitch.tv Art section
    driver.get("https://www.twitch.tv/directory/game/Art")

    # Step 3: Wait for the page to load specific elements
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-target='directory-first-item']"))
    )

    # Step 4: Get the page source
    page_source = driver.page_source

    # Step 5: Parse the HTML using Parsel
    sel = Selector(text=page_source)

    # Step 6: Extract data from the HTML
    scraped_data = []
    for item in sel.xpath("//div[contains(@class,'tw-tower')]/div[@data-target]"):
        data = {
            "title": item.css("h3::text").get(),
            "url": item.css(".tw-link::attr(href)").get(),
            "username": item.css(".tw-link::text").get(),
            "tags": item.css(".tw-tag::text").getall(),
            "viewers": ''.join(item.css(".tw-media-card-stat::text").re(r"(\d+)"))
        }
        scraped_data.append(data)

    # Step 7: Print the extracted data
    print(json.dumps(scraped_data, indent=2))

finally:
    # Step 8: Quit the browser
    driver.quit()

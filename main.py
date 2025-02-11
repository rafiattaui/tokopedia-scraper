# https://www.scrapingbee.com/blog/selenium-python/

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Path to ChromeDriver
DRIVER_PATH = "chromedriver-win64/chromedriver.exe"

# Set Chrome options
options = Options()
#options.add_argument("--headless=new")  # New headless mode (better performance)
options.add_argument("--window-size=1920,1200")
options.add_argument("--disable-gpu")  # Helps prevent crashes in headless mode
options.add_argument("--no-sandbox")  # Useful for running in certain environments

# Initialize Chrome driver using Service
service = Service(DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# Product to search
product = "rtx 3060"

# Navigate to the tokopedia rtx 3060 website
driver.get("https://www.tokopedia.com/search?st=product&q=" + product)
for i in range(3):
    product = driver.find_elements(By.XPATH, f"""""") # Todo: Find the xpath of the product price
    print(f"Product {i+1} price: {product}")

# Close the browser
print("Closing the browser...")
print("Browser title:", driver.title)
print("Browser URL:", driver.current_url)
driver.quit()
print("Browser closed.")

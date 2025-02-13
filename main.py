from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Path to ChromeDriver
DRIVER_PATH = "chromedriver-win64/chromedriver.exe"

# Set Chrome options
options = Options()
options.add_argument("--window-size=1920,1200")
options.add_argument("--disable-gpu")  
options.add_argument("--no-sandbox")  

# Initialize Chrome driver
service = Service(DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# Product to search
product_query = "rtx 3060"
keywords = []
filterwords = ["pc gaming"]
products = {}
search_length = 5

# Navigate to Tokopedia search page
driver.get(f"https://www.tokopedia.com/search?st=product&q={product_query}")

# Wait for the page to load
driver.implicitly_wait(5)

# Find all product price elements
prices = driver.find_elements(By.XPATH, "//div[contains(@class, '_67d6E1xDKIzw+i2D2L0tjw== ')]")  # Product prices
names = driver.find_elements(By.XPATH, "//span[contains(@class, '_0T8-iGxMpV6NEsYEhwkqEg==')]")  # Product names
for i, name in enumerate(names):  # Use enumerate() to track index efficiently
    if product_query.lower() in name.text.lower():
        print(f"Filtering {name.text}")
        if all(filterword.lower() not in name.text.lower() for filterword in filterwords):
            products[name.text] = prices[i].text  # Use i from enumerate()
            
        if len(products) == search_length:
            break  # Stop if we reach the required number of products

# Print product prices
for i in range(len(products)):
    try:
        print(f"Product {i+1}:")
        print("Name:", names[i].text)
        print("Price:", prices[i].text)
        print()
    except:
        print(f"Product {i+1} not found.\n")
        break

# Close the browser
print("Closing the browser...")
print("Browser title:", driver.title)
print("Browser URL:", driver.current_url)
driver.quit()
print("Browser closed.")

# TODO - Filter products based on keywords
# TODO - Display products on a GUI or HTML page

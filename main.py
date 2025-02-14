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

# Input variables
product_query = "rtx 3060"
filterwords = ["pc gaming", "legion", "pc"]
products = []
search_length = 5

# Navigate to Tokopedia search page
driver.get(f"https://www.tokopedia.com/search?st=product&q={product_query}")

# Wait for the page to load
driver.implicitly_wait(5)

# Find product names and prices
names = driver.find_elements(By.XPATH, "//span[contains(@class, '_0T8-iGxMpV6NEsYEhwkqEg==')]")
prices = driver.find_elements(By.XPATH, "//div[contains(@class, '_67d6E1xDKIzw+i2D2L0tjw== ')]")
print(f"Found {len(names)} products.\n")

# Ensure the two lists are the same length
if len(names) != len(prices):
    print("Warning: Mismatched name-price elements. Skipping inconsistent results.")
    matched_results = zip(names[:len(prices)], prices)
else:
    matched_results = zip(names, prices)

# Filter products
for name, price in matched_results:
    product_name = name.text.lower()
    if product_query.lower() in product_name and all(fw.lower() not in product_name for fw in filterwords):
        products.append((name.text, price.text))
    
    if len(products) >= search_length:
        print("")
        break  # Stop after collecting enough products
    
# Print results
for i, (name, price) in enumerate(products, start=1):
    print(f"Product {i}:")
    print("Name:", name)
    print("Price:", price)
    print()

# Close the browser
print("Closing the browser...")
print("Browser title:", driver.title)
print("Browser URL:", driver.current_url)
driver.quit()
print("Browser closed.")


# TODO - Filter products based on keywords (Done)
# TODO - Load more items if not enough valid products.
# TODO - Display products on a GUI or HTML page
# TODO - Detect outliers

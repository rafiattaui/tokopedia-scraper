from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

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
driver.implicitly_wait(10)

# Find product names and prices
i = 0
while len(products) < search_length:
    name = driver.find_element(By.XPATH, f"(//span[contains(@class, '_0T8-iGxMpV6NEsYEhwkqEg==')])[{i+1}]")
    price = driver.find_element(By.XPATH, f"(//div[contains(@class, '_67d6E1xDKIzw+i2D2L0tjw== ')])[{i+1}]")
    
    print(f"Scanning product, {name.text}: {price.text}\n")
    
    matched_result = (name.text, price.text)
    product_name, product_price = matched_result

    # Filtering products
    if product_query.lower() in product_name.lower() and all(fw.lower() not in product_name.lower() for fw in filterwords):
        products.append((product_name, product_price))

    i += 1

print(f"Found {i} products in total\nAccepted {len(products)} valid products\n")
        
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

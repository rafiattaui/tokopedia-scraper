from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from product import Product
import time

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
search_length = 20

# Navigate to Tokopedia search page
driver.get(f"https://www.tokopedia.com/search?st=product&q={product_query}")

# Wait for the page to load, and scroll to the end of the page to load all options.
driver.implicitly_wait(10)
for _ in range(0, 6500, 500):
            time.sleep(0.1)
            driver.execute_script("window.scrollBy(0,500)")

# Find product names and prices
i = 0
while len(products) < search_length:  # Continually search for valid products until we have enough results
    try:
        name = driver.find_element(By.XPATH, f"(//span[contains(@class, '_0T8-iGxMpV6NEsYEhwkqEg==')])[{i+1}]")
        price = driver.find_element(By.XPATH, f"(//div[contains(@class, '_67d6E1xDKIzw+i2D2L0tjw==')])[{i+1}]")
        url = driver.find_element(By.XPATH, f"(//a[contains(@class, 'oQ94Awb6LlTiGByQZo8Lyw== IM26HEnTb-krJayD-R0OHw==')])[{i+1}]")
        
        print(f"Scanning product: {name.text}: {price.text}")
        
        matched_result = (name.text, price.text, url.get_attribute("href"))
        product_name, product_price, product_url = matched_result

        # Filtering products
        if product_query.lower() in product_name.lower() and all(fw.lower() not in product_name.lower() for fw in filterwords):
            products.append(Product(product_name, product_price, product_url))

    except NoSuchElementException:
        print("No such items were found, or no more items could be found.")
        break  # Stop the loop if no more elements are found

    finally:
        i += 1  # Always increment i, even if an exception occurs


print(f"Found {i} products before accepting {len(products)} valid products.\n")
        
# Print results
for i, product in enumerate(products, start=1):
    print(product)

# Close the browser
print("Closing the browser...")
print("Browser title:", driver.title)
print("Browser URL:", driver.current_url)
driver.quit()
print("Browser closed.")


# TODO - Filter products based on keywords (Done)
# TODO - Store more information of a product in a compact manner, using a Product class. (Done)
# TODO - Load more items if not enough valid products. (Solved by scrolling to the end of the page to load all items)
# TODO - Display products on a GUI or HTML page
# TODO - Detect outliers

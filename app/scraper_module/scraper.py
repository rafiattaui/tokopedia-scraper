from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from scraper_module.product import Product
import time
import csv

class Scraper:
    def __init__(self, headless, driver_path="chromedriver-win64/chromedriver.exe"):
        self.DRIVER_PATH = driver_path

        # Set Chrome options
        self.options = Options()
        self.options.add_argument("--window-size=1920,1200")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        if headless: self.options.add_argument("--headless")  # Run in headless mode

        # Initialize Chrome driver
        self.service = Service(self.DRIVER_PATH)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

        # Define XPath variables
        self.XPATH_PRODUCT_NAME = "//span[contains(@class, '_0T8-iGxMpV6NEsYEhwkqEg==')]"
        self.XPATH_PRODUCT_PRICE = "//div[contains(@class, '_67d6E1xDKIzw+i2D2L0tjw==')]"
        self.XPATH_PRODUCT_URL = "//a[contains(@class, 'oQ94Awb6LlTiGByQZo8Lyw== IM26HEnTb-krJayD-R0OHw==')]"

    def search(self, query, search_length=20, *filterwords):
        product_query = query.lower()
        products = []
        filterwords = [fw.lower() for fw in filterwords]  # Normalize filter words

        # Navigate to Tokopedia search page
        self.driver.get(f"https://www.tokopedia.com/search?st=product&q={query}")
        self.driver.implicitly_wait(10)

        # Scroll dynamically until enough products are found
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while len(products) < search_length:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)  # Allow content to load
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # Stop if no more products are loading
            last_height = new_height

        max_products = len(self.driver.find_elements(By.XPATH, self.XPATH_PRODUCT_NAME))

        i = 0
        while len(products) < search_length and i < max_products:
            try:
                name_elem = self.driver.find_element(By.XPATH, f"({self.XPATH_PRODUCT_NAME})[{i+1}]")
                price_elem = self.driver.find_element(By.XPATH, f"({self.XPATH_PRODUCT_PRICE})[{i+1}]")
                url_elem = self.driver.find_element(By.XPATH, f"({self.XPATH_PRODUCT_URL})[{i+1}]")

                product_name = name_elem.text.strip()
                product_price = price_elem.text.strip()
                product_url = url_elem.get_attribute("href")

                # Filtering products
                if product_query in product_name.lower() and not any(fw in product_name.lower() for fw in filterwords):
                    products.append(Product(product_name, product_price, product_url))

            except NoSuchElementException:
                print(f"\nProduct at index {i+1} not found. Skipping...")
            
            i += 1  # Always increment index

        print(f"Found {i} products before accepting {len(products)} valid products.\n")
        return products

    def save_to_csv(self, products, filename="products.csv"):
        """Save product data to a CSV file."""
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Price", "URL"])  # Header row
            for product in products:
                writer.writerow([product.name, product.price, product.url])
        print(f"Data saved to {filename}")

    def quit(self):
        """Close the browser."""
        print("Closing the browser...")
        self.driver.quit()
        print("Browser closed.")

# Usage Example
if __name__ == "__main__":
    scraper = Scraper(False)
    products = scraper.search("iphone", 10, "samsung", "xiaomi")  # Search for iPhones, filter out Samsung/Xiaomi
    scraper.save_to_csv(products)  # Save results to CSV
    scraper.quit()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from product import Product
import time

class Scraper:
    def __init__(self):
        self.DRIVER_PATH = "chromedriver-win64/chromedriver.exe"

        # Set Chrome options
        self.options = Options()
        self.options.add_argument("--window-size=1920,1200")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")

        # Initialize Chrome driver
        self.service = Service(self.DRIVER_PATH)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        
    def search(self, query, search_length, filterwords):
        
        product_query = query
        products = []
        search_length = 20

        # Navigate to Tokopedia search page
        self.driver.get(f"https://www.tokopedia.com/search?st=product&q={product_query}")

        # Wait for the page to load, and scroll to the end of the page to load all options.
        self.driver.implicitly_wait(10)
        for _ in range(0, 6500, 500):
                    time.sleep(0.1)
                    self.driver.execute_script("window.scrollBy(0,500)")

        # Find product names and prices
        # Find product names and prices
        i = 0
        max_products = len(self.driver.find_elements(By.XPATH, "//span[contains(@class, '_0T8-iGxMpV6NEsYEhwkqEg==')]"))
        product_query = product_query.lower()
        filterwords = [fw.lower() for fw in filterwords]

        while len(products) < search_length and i < max_products:
            try:
                name = self.driver.find_element(By.XPATH, f"(//span[contains(@class, '_0T8-iGxMpV6NEsYEhwkqEg==')])[{i+1}]")
                price = self.driver.find_element(By.XPATH, f"(//div[contains(@class, '_67d6E1xDKIzw+i2D2L0tjw==')])[{i+1}]")
                url = self.driver.find_element(By.XPATH, f"(//a[contains(@class, 'oQ94Awb6LlTiGByQZo8Lyw== IM26HEnTb-krJayD-R0OHw==')])[{i+1}]")

                print(f"Scanning product: {name.text}: {price.text}")

                product_name = name.text or ""
                product_price = price.text
                product_url = url.get_attribute("href")
                
                # Filtering products
                if product_query in product_name.lower() and all(fw not in product_name.lower() for fw in filterwords):
                    products.append(Product(product_name, product_price, product_url))

            except NoSuchElementException:
                print(f"Product at index {i+1} not found. Skipping...")
            
            i += 1  # Always increment i



        print(f"Found {i} products before accepting {len(products)} valid products.\n")
                
        # Print results
        for i, product in enumerate(products, start=1):
            print(product)
            
    def quit(self):
        
        # Close the browser
        print("Closing the browser...")
        print("Browser title:", self.driver.title)
        print("Browser URL:", self.driver.current_url)
        self.driver.quit()
        print("Browser closed.")


# TODO - Filter products based on keywords (Done)
# TODO - Store more information of a product in a compact manner, using a Product class. (Done)
# TODO - Load more items if not enough valid products. (Solved by scrolling to the end of the page to load all items)
# TODO - Find products based on rating      
# TODO - Display products on a GUI or HTML page
# TODO - Detect outliers

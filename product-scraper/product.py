class Product:
    
    def __init__(self, name, price, url):
        self.name = name
        self.price = price
        self.url = url
        
    def __str__(self):
        return f"Product Name: {self.name}\nPrice: {self.price}\nURL: {self.url}"
    
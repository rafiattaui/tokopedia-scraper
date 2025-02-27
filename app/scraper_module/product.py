class Product:
    
    def __init__(self, name, price, url, rating = None):
        self.name = name
        self.price = price
        self.url = url
        self.rating = rating
        
    def __str__(self):
        if self.rating:
            return f"Product Name: {self.name}\nPrice: {self.price}\nRating: {self.rating}\nURL: {self.url}\n"
        else:
            return f"Product Name: {self.name}\nPrice: {self.price}\nURL: {self.url}\n"
    
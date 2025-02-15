query = "rtx 3050"
filterwords = ["pc gaming"]
products = ["pc gaming | rtx 3050", "rtx 3050", "rtx 2080"]
result = []

for product in products:
    if query.lower() in product.lower():
        if all(filterword.lower() not in product.lower() for filterword in filterwords):
            result.append(product)
            
print(result)
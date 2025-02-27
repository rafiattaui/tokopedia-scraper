from flask import Flask, render_template, request
from scraper_module.scraper import Scraper

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def index_query():
    query = request.form["query"].lower()
    print(f"Searching for products with query: {query}")
    
    scraper = Scraper(False, "scraper_module/chromedriver-win64/chromedriver.exe")
    scraper.search(query, 10, "samsung", "xiaomi")
    scraper.quit()
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
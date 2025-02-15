from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search=<query>")
def index_query():
    return render_template()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
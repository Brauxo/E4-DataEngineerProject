from flask import Flask, render_template
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch("http://elasticsearch:9200")

@app.route("/")
def home():
    return render_template('home_page.html')

@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html')

@app.route("/restaurant")
def restaurant():
    return render_template('restaurant.html')

@app.route("/analyse")
def analyse():
    return render_template('restaurant.html')

if __name__ == "__main__":
    app.run(debug=True)

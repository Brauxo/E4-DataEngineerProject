from flask import Flask, render_template
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch("http://elasticsearch:9200")

@app.route("/")
def home():
    return render_template('home_page.html')

if __name__ == "__main__":
    app.run(debug=True)

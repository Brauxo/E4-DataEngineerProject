from flask import Flask, render_template
from elastic_tools import get_connection

app = Flask(__name__)
#es = Elasticsearch("http://elasticsearch:9200")

@app.route("/")
def home():
    return render_template('home_page.html')

@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html')

@app.route("/restaurant")
def restaurant():
    es = get_connection()
    index_name = "gaultmillau_restaurants"

    # Récupérer les 10 premiers documents (ou ajuster selon besoin)
    response = es.search(index=index_name, body={"query": {"match_all": {}}}, size=30)
    restaurants = [doc['_source'] for doc in response['hits']['hits']]

    return render_template('restaurant.html', restaurants=restaurants)

@app.route("/analyse")
def analyse():
    return render_template('analyse.html')

if __name__ == "__main__":
    app.run(debug=True)

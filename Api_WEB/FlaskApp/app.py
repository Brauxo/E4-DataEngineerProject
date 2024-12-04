from flask import Flask, render_template, request
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

    # Récupérer les paramètres de la requête
    min_rating = request.args.get('min_rating', None)
    department = request.args.get('department', None)
    selected_cuisines = request.args.getlist('cuisine')  # Liste des types de cuisine sélectionnés

    # Récupérer les paramètres de pagination
    page = int(request.args.get('page', 1))  # Page actuelle (par défaut 1)
    size = 18  # Nombre de résultats par page
    start = (page - 1) * size  # Calculer l'offset

    # Construire la requête Elasticsearch
    query = {"bool": {"must": []}}

    # Filtre par note minimale
    if min_rating:
        min_rating = float(min_rating)
        if min_rating > 0:
            query["bool"]["must"].append({
                "range": {
                    "rating": {"gte": min_rating}
                }
            })

    # Filtre par département
    if department:
        query["bool"]["must"].append({
            "wildcard": {
                "address": f"{department}*"
            }
        })

    # Filtre par types de cuisine
    if selected_cuisines:
        query["bool"]["must"].append({
            "match": {
                "cuisine": " ".join(selected_cuisines)
            }
        })

    # Exécuter la requête Elasticsearch pour obtenir les restaurants de la page actuelle
    sort = [{"rating": "desc"}]
    print({"query": query, "sort": sort, "from": start, "size": size})  # Affiche la requête
    response = es.search(index=index_name, body={"query": query, "sort": sort}, from_=start, size=size)

    # Utiliser un dictionnaire pour supprimer les doublons
    restaurants_dict = {doc['_source']['name']: doc['_source'] for doc in response['hits']['hits']}
    restaurants = list(restaurants_dict.values())  # Convertir en liste unique
    total_hits = response['hits']['total']['value']  # Nombre total de résultats

    # Récupérer tous les documents pour les départements et cuisines uniques
    scroll_response = es.search(index=index_name, body={"query": {"match_all": {}}}, scroll='2m', size=1000)
    scroll_id = scroll_response['_scroll_id']
    all_addresses = scroll_response['hits']['hits']

    while True:
        scroll_response = es.scroll(scroll_id=scroll_id, scroll='2m')
        if not scroll_response['hits']['hits']:
            break
        all_addresses.extend(scroll_response['hits']['hits'])

    # Extraire les départements uniques
    unique_departments = sorted(set(
        [addr['_source']['address'][:2] for addr in all_addresses
         if addr['_source'].get('address') and addr['_source']['address'][:2].isdigit()]
    ))

    unique_cuisines = set()
    for doc in all_addresses:
        cuisine_field = doc['_source'].get('cuisine')
        if cuisine_field and isinstance(cuisine_field, list):
            unique_cuisines.update(cuisine_field)  # Ajouter chaque élément de la liste

    # Nombre total de restaurants sans filtre
    total_restaurants = len(all_addresses)

    return render_template(
        'restaurant.html',
        restaurants=restaurants,
        unique_departments=unique_departments,
        page=page,
        unique_cuisines=sorted(unique_cuisines),
        total_hits=total_hits,
        size=size,
        total_restaurants=total_restaurants
    )





@app.route("/analyse")
def analyse():
    return render_template('analyse.html')

if __name__ == "__main__":
    app.run(debug=True)

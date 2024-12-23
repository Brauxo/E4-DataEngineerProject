"""
Authors: Elliot CAMBIER, Owen BRAUX
Created: January 2025
⚠ For personal and educational use only ⚠
"""
from flask import Flask, render_template, request
from elastic_tools import get_connection
import pandas as pd
import json

"""
L'application Flask principale pour la gestion et l'affichage des données des restaurants GaultMillau.
"""
app = Flask(__name__)
#es = Elasticsearch("http://elasticsearch:9200")

@app.route("/")
def home():
    """Affiche la page d'accueil."""
    return render_template('home_page.html')

@app.route("/aboutus")                                                                          
def aboutus():
    """Affiche la page 'À propos de nous'."""
    return render_template('aboutus.html')

@app.route("/restaurant")
def restaurant():
    """
    Gère la recherche et la page des restaurants dans Elasticsearch
    avec des filtres sur la note minimale, le département et la cuisine.
    """
    es = get_connection()
    index_name = "gaultmillau_restaurants"

    # Récupére les paramètres de la requête
    min_rating = request.args.get('min_rating', None)
    department = request.args.get('department', None)
    selected_cuisines = request.args.getlist('cuisine')  # Liste des types de cuisine sélectionnés

    # Récupére les paramètres de page
    page = int(request.args.get('page', 1))  # Page actuelle (valeur : 1 de base)
    size = 18  # Nombre de résultats par page
    start = (page - 1) * size  # offsett

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

    # Exécute la requête Elasticsearch pour obtenir les restaurants de la page actuelle
    sort = [{"rating": "desc"}]
    print({"query": query, "sort": sort, "from": start, "size": size})  # Affiche la requête
    response = es.search(index=index_name, body={"query": query, "sort": sort}, from_=start, size=size)

    # Utilise un dictionnaire pour supprimer les doublons
    restaurants_dict = {doc['_source']['name']: doc['_source'] for doc in response['hits']['hits']}
    restaurants = list(restaurants_dict.values())  # Convertir en liste unique
    total_hits = response['hits']['total']['value']  # Nombre total de résultats

    # Récupére tous les documents pour les départements et cuisines uniques
    scroll_response = es.search(index=index_name, body={"query": {"match_all": {}}}, scroll='2m', size=1000)
    scroll_id = scroll_response['_scroll_id']
    all_addresses = scroll_response['hits']['hits']

    while True:
        scroll_response = es.scroll(scroll_id=scroll_id, scroll='2m')
        if not scroll_response['hits']['hits']:
            break
        all_addresses.extend(scroll_response['hits']['hits'])

    # Extrait les départements uniques
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
    """
    Page d'analyse des données des restaurants de notre elasticSearch pour générer des graphiques et une carte.
    """

    es = get_connection()
    index_name = "gaultmillau_restaurants"

    # Effectue une recherche Elasticsearch pour extraire des données nécessaires
    response = es.search(index=index_name, body={"query": {"match_all": {}}}, size=1000)
    hits = [hit['_source'] for hit in response['hits']['hits']]

    # Convertie les résultats en DataFrame pandas
    data = pd.DataFrame(hits)

    # Nettoye les données : Exemple pour les départements
    data['department'] = data['address'].str[:2]
    data = data[data['department'].fillna('0').str.isdigit()]   # Filtrer les départements valides

    # Compte les restaurants par département
    dept_counts = data['department'].value_counts().reset_index()
    dept_counts.columns = ['department', 'count']

    # Crée un dictionnaire GeoJSON des départements avec le nombre de restaurants
    geojson_data = create_geojson(dept_counts)

    # Prépare les autres données pour les graphiques
    graph_data = {
        'dept_counts': dept_counts.to_dict(orient='records'),
        'rating_histogram': data['rating'].dropna().tolist(),
        'cuisine_distribution': data['cuisine'].explode().value_counts().reset_index().to_dict(orient='records'),
        'geojson_data': geojson_data  # Passer les données GeoJSON pour la carte
    }

    # Passe les données au template
    return render_template('analyse.html', graph_data=graph_data)

def create_geojson(dept_counts):
    """
    Crée un GeoJSON représentant les départements et le nombre de restaurants associés.

    :param dept_counts: DataFrame contenant les départements et leur nombre de restaurants.
    :return: Dictionnaire GeoJSON.
    """
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # Vous devez avoir une liste des départements français avec leurs coordonnées géographiques
    # Vous pouvez charger cette information depuis un fichier GeoJSON ou une API.
    
    # Exemple de départements (vous devrez remplacer cela par des données réelles de géométrie)
    # Chaque département doit être associé à un "department" et avoir un nombre de restaurants
    for _, row in dept_counts.iterrows():
        department = row['department']
        restaurant_count = row['count']
        
        # Exemple simple de structure GeoJSON, remplacez "geometry" par la vraie géométrie des départements
        feature = {
            "type": "Feature",
            "properties": {
                "nom": department,
                "restaurant_count": restaurant_count
            },
            "geometry": {
                "type": "Polygon",  # Ceci est un exemple, chaque département doit avoir sa propre géométrie
                "coordinates": [[0, 0]]  # Remplacer par les coordonnées réelles des départements
            }
        }
        geojson["features"].append(feature)

    return geojson

if __name__ == "__main__":
    app.run(debug=True)

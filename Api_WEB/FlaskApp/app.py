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

#liste des departements (utilisé dans le code)
DEPARTMENTS = {
    '01': 'Ain', '02': 'Aisne', '03': 'Allier', '04': 'Alpes-de-Haute-Provence', '05': 'Hautes-Alpes',
    '06': 'Alpes-Maritimes', '07': 'Ardèche', '08': 'Ardennes', '09': 'Ariège', '10': 'Aube', '11': 'Aude',
    '12': 'Aveyron', '13': 'Bouches-du-Rhône', '14': 'Calvados', '15': 'Cantal', '16': 'Charente',
    '17': 'Charente-Maritime', '18': 'Cher', '19': 'Corrèze', '2A': 'Corse-du-Sud', '2B': 'Haute-Corse',
    '21': 'Côte-d\'Or', '22': 'Côtes-d\'Armor', '23': 'Creuse', '24': 'Dordogne', '25': 'Doubs', '26': 'Drôme',
    '27': 'Eure', '28': 'Eure-et-Loir', '29': 'Finistère', '30': 'Gard', '31': 'Haute-Garonne', '32': 'Gers',
    '33': 'Gironde', '34': 'Hérault', '35': 'Ille-et-Vilaine', '36': 'Indre', '37': 'Indre-et-Loire',
    '38': 'Isère', '39': 'Jura', '40': 'Landes', '41': 'Loir-et-Cher', '42': 'Loire', '43': 'Haute-Loire',
    '44': 'Loire-Atlantique', '45': 'Loiret', '46': 'Lot', '47': 'Lot-et-Garonne', '48': 'Lozère',
    '49': 'Maine-et-Loire', '50': 'Manche', '51': 'Marne', '52': 'Haute-Marne', '53': 'Mayenne',
    '54': 'Meurthe-et-Moselle', '55': 'Meuse', '56': 'Morbihan', '57': 'Moselle', '58': 'Nièvre', '59': 'Nord',
    '60': 'Oise', '61': 'Orne', '62': 'Pas-de-Calais', '63': 'Puy-de-Dôme', '64': 'Pyrénées-Atlantiques',
    '65': 'Hautes-Pyrénées', '66': 'Pyrénées-Orientales', '67': 'Bas-Rhin', '68': 'Haut-Rhin', '69': 'Rhône',
    '70': 'Haute-Saône', '71': 'Saône-et-Loire', '72': 'Sarthe', '73': 'Savoie', '74': 'Haute-Savoie',
    '75': 'Paris', '76': 'Seine-Maritime', '77': 'Seine-et-Marne', '78': 'Yvelines', '79': 'Deux-Sèvres',
    '80': 'Somme', '81': 'Tarn', '82': 'Tarn-et-Garonne', '83': 'Var', '84': 'Vaucluse', '85': 'Vendée',
    '86': 'Vienne', '87': 'Haute-Vienne', '88': 'Vosges', '89': 'Yonne', '90': 'Territoire de Belfort',
    '91': 'Essonne', '92': 'Hauts-de-Seine', '93': 'Seine-Saint-Denis', '94': 'Val-de-Marne', '95': 'Val-d\'Oise',
    '971': 'Guadeloupe', '972': 'Martinique', '973': 'Guyane', '974': 'La Réunion', '976': 'Mayotte',
}




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
    Page d'analyse des données des restaurants de notre Elasticsearch pour générer des graphiques et une carte.
    """

    es = get_connection()
    index_name = "gaultmillau_restaurants"

    # Récupérer les paramètres de filtre, si fournis
    department = request.args.get('department', None)
    selected_cuisines = request.args.getlist('cuisine')  # Liste des types de cuisine sélectionnés

    # Fonction pour récupérer tous les restaurants
    def get_all_restaurants(es, index_name, size=1000):
        all_hits = []
        from_index = 0

        while True:
            query = {
                "query": {
                    "match_all": {}
                },
                "size": size,
                "from": from_index
            }

            response = es.search(index=index_name, body=query)
            hits = [hit['_source'] for hit in response['hits']['hits']]
            if not hits:
                break

            all_hits.extend(hits)
            from_index += size  # Passe à la page suivante

        return all_hits

    # Récupérer tous les restaurants
    hits = get_all_restaurants(es, index_name)

    # Convertir en DataFrame pandas pour faciliter la manipulation
    data = pd.DataFrame(hits)

    # Appliquer les filtres si spécifiés
    if department:
        data = data[data['address'].str.startswith(department)]

    if selected_cuisines:
        # Filtrer selon les cuisines sélectionnées (en supposant que 'cuisine' soit une liste dans vos données)
        data = data[data['cuisine'].apply(lambda x: any(cuisine in x for cuisine in selected_cuisines))]

    # Nettoyage des données (comme pour le département)
    data['department'] = data['address'].str[:2]
    data = data[data['department'].fillna('0').str.isdigit()]  # Filtrer les départements valides

    # Ajouter le nom du département
    data['department_name'] = data['department'].map(DEPARTMENTS)

    # Vérification et ajustement des notes
    data['rating'] = data['rating'].apply(lambda x: float(x) if isinstance(x, (int, float)) else None)
    data = data[data['rating'].notna()]  # Supprimer les valeurs manquantes
    data['rating'] = data['rating'].apply(lambda x: max(5, min(20, x)))  # Assurez-vous que les notes sont entre 5 et 20

    # Compter les restaurants par département
    dept_counts = data['department_name'].value_counts().reset_index()
    dept_counts.columns = ['department', 'count']

    # Créer le GeoJSON pour la carte
    geojson_data = create_geojson(dept_counts)

    # Sauvegarder le fichier GeoJSON dans le dossier statique
    geojson_path = "FlaskApp/static/geojson_enriched.json"
    with open(geojson_path, 'w') as geojson_file:
        json.dump(geojson_data, geojson_file)

    # Préparer les autres données pour les graphiques
    graph_data = {
        'dept_counts': dept_counts.to_dict(orient='records'),
        'geojson_data': geojson_data,  
        'geojson_path': geojson_path
    }

    # Ajouter des données pour les histogrammes
    rating_histogram = data['rating'].dropna().tolist()
    cuisine_distribution = data['cuisine'].explode().value_counts().reset_index().to_dict(orient='records')

    # Ajouter aux données du graphique
    graph_data['rating_histogram'] = rating_histogram
    graph_data['cuisine_distribution'] = cuisine_distribution

    # Passer les données au template
    return render_template('analyse.html', graph_data=graph_data)



def create_geojson(dept_counts):
    """
    Crée un GeoJSON représentant les départements et le nombre de restaurants associés.

    :param dept_counts: DataFrame contenant les départements et leur nombre de restaurants.
    :return: Dictionnaire GeoJSON.
    """
    with open('FlaskApp/static/departements.geojson', 'r') as geojson_file:
        geojson_template = json.load(geojson_file)
    
    # Map les données de counts sur les propriétés GeoJSON
    for feature in geojson_template['features']:
        department_code = feature['properties']['code']
        feature['properties']['restaurant_count'] = int(
            dept_counts[dept_counts['department'] == department_code]['count'].sum()
        )
    
    return geojson_template

if __name__ == "__main__":
    app.run(debug=True)

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

departements_coordinates = {
    "01": {"name": "Ain", "coordinates": [5.8102, 46.01086]},
    "02": {"name": "Aisne", "coordinates": [3.5583, 49.5594]},
    "03": {"name": "Allier", "coordinates": [3.1883, 46.3936]},
    "04": {"name": "Alpes-de-Haute-Provence", "coordinates": [6.2439, 44.1061]},
    "05": {"name": "Hautes-Alpes", "coordinates": [6.2631, 44.6636]},
    "06": {"name": "Alpes-Maritimes", "coordinates": [7.1164, 43.9375]},
    "07": {"name": "Ardèche", "coordinates": [4.4247, 44.7517]},
    "08": {"name": "Ardennes", "coordinates": [4.6408, 49.6156]},
    "09": {"name": "Ariège", "coordinates": [1.5039, 42.9208]},
    "10": {"name": "Aube", "coordinates": [4.1617, 48.3044]},
    "11": {"name": "Aude", "coordinates": [2.4142, 43.1033]},
    "12": {"name": "Aveyron", "coordinates": [2.6797, 44.2803]},
    "13": {"name": "Bouches-du-Rhône", "coordinates": [5.0864, 43.5433]},
    "14": {"name": "Calvados", "coordinates": [-0.3636, 49.0997]},
    "15": {"name": "Cantal", "coordinates": [2.6686, 45.0511]},
    "16": {"name": "Charente", "coordinates": [0.2017, 45.7181]},
    "17": {"name": "Charente-Maritime", "coordinates": [-0.6744, 45.7808]},
    "18": {"name": "Cher", "coordinates": [2.4911, 47.0647]},
    "19": {"name": "Corrèze", "coordinates": [1.8769, 45.3569]},
    "20": {"name": "Corse-du-Sud", "coordinates": [8.9881, 41.8636]},
    "21": {"name": "Côte-d'Or", "coordinates": [4.7722, 47.4247]},
    "22": {"name": "Côtes-d'Armor", "coordinates": [-2.8642, 48.4411]},
    "23": {"name": "Creuse", "coordinates": [2.0189, 46.0903]},
    "24": {"name": "Dordogne", "coordinates": [0.7414, 45.1042]},
    "25": {"name": "Doubs", "coordinates": [6.3617, 47.1653]},
    "26": {"name": "Drôme", "coordinates": [5.1681, 44.6842]},
    "27": {"name": "Eure", "coordinates": [0.9961, 49.1136]},
    "28": {"name": "Eure-et-Loir", "coordinates": [1.3703, 48.3875]},
    "29": {"name": "Finistère", "coordinates": [-4.0589, 48.2611]},
    "30": {"name": "Gard", "coordinates": [4.1803, 43.9933]},
    "31": {"name": "Haute-Garonne", "coordinates": [1.1728, 43.3586]},
    "32": {"name": "Gers", "coordinates": [0.4533, 43.6928]},
    "33": {"name": "Gironde", "coordinates": [-0.5753, 44.8253]},
    "34": {"name": "Hérault", "coordinates": [3.3672, 43.5797]},
    "35": {"name": "Ille-et-Vilaine", "coordinates": [-1.6386, 48.1544]},
    "36": {"name": "Indre", "coordinates": [1.5758, 46.7778]},
    "37": {"name": "Indre-et-Loire", "coordinates": [0.6914, 47.2581]},
    "38": {"name": "Isère", "coordinates": [5.5761, 45.2633]},
    "39": {"name": "Jura", "coordinates": [5.6978, 46.7283]},
    "40": {"name": "Landes", "coordinates": [-0.7839, 43.9656]},
    "41": {"name": "Loir-et-Cher", "coordinates": [1.4294, 47.6167]},
    "42": {"name": "Loire", "coordinates": [4.1658, 45.7264]},
    "43": {"name": "Haute-Loire", "coordinates": [3.8064, 45.1281]},
    "44": {"name": "Loire-Atlantique", "coordinates": [-1.6822, 47.3614]},
    "45": {"name": "Loiret", "coordinates": [2.3442, 47.9120]},
    "46": {"name": "Lot", "coordinates": [1.6047, 44.6242]},
    "47": {"name": "Lot-et-Garonne", "coordinates": [0.4603, 44.3675]},
    "48": {"name": "Lozère", "coordinates": [3.5003, 44.5172]},
    "49": {"name": "Maine-et-Loire", "coordinates": [-0.5642, 47.3908]},
    "50": {"name": "Manche", "coordinates": [-1.3275, 49.0794]},
    "51": {"name": "Marne", "coordinates": [4.2386, 48.9492]},
    "52": {"name": "Haute-Marne", "coordinates": [5.2264, 48.1094]},
    "53": {"name": "Mayenne", "coordinates": [-0.6581, 48.1467]},
    "54": {"name": "Meurthe-et-Moselle", "coordinates": [6.1650, 48.7869]},
    "55": {"name": "Meuse", "coordinates": [5.3817, 48.9894]},
    "56": {"name": "Morbihan", "coordinates": [-2.8100, 47.8464]},
    "57": {"name": "Moselle", "coordinates": [6.6633, 49.0372]},
    "58": {"name": "Nièvre", "coordinates": [3.5047, 47.1153]},
    "59": {"name": "Nord", "coordinates": [3.2206, 50.4472]},
    "60": {"name": "Oise", "coordinates": [2.4253, 49.4103]},
    "61": {"name": "Orne", "coordinates": [0.1289, 48.6236]},
    "62": {"name": "Pas-de-Calais", "coordinates": [2.2886, 50.4931]},
    "63": {"name": "Puy-de-Dôme", "coordinates": [3.1417, 45.7258]},
    "64": {"name": "Pyrénées-Atlantiques", "coordinates": [-0.7614, 43.2567]},
    "65": {"name": "Hautes-Pyrénées", "coordinates": [0.1639, 43.0531]},
    "66": {"name": "Pyrénées-Orientales", "coordinates": [2.5222, 42.6000]},
    "67": {"name": "Bas-Rhin", "coordinates": [7.5514, 48.6708]},
    "68": {"name": "Haut-Rhin", "coordinates": [7.2742, 47.8586]},
    "69": {"name": "Rhône", "coordinates": [4.6414, 45.8703]},
    "70": {"name": "Haute-Saône", "coordinates": [6.0861, 47.6411]},
    "71": {"name": "Saône-et-Loire", "coordinates": [4.5422, 46.6447]},
    "72": {"name": "Sarthe", "coordinates": [0.2222, 47.9944]},
    "73": {"name": "Savoie", "coordinates": [6.4436, 45.4775]},
    "74": {"name": "Haute-Savoie", "coordinates": [6.4281, 46.0344]},
    "75": {"name": "Paris", "coordinates": [2.3422, 48.8567]},
    "76": {"name": "Seine-Maritime", "coordinates": [1.0264, 49.6550]},
    "77": {"name": "Seine-et-Marne", "coordinates": [2.9333, 48.6267]},
    "78": {"name": "Yvelines", "coordinates": [1.8417, 48.8150]},
    "79": {"name": "Deux-Sèvres", "coordinates": [-0.3172, 46.5556]},
    "80": {"name": "Somme", "coordinates": [2.2778, 49.9581]},
    "81": {"name": "Tarn", "coordinates": [2.1661, 43.7853]},
    "82": {"name": "Tarn-et-Garonne", "coordinates": [1.2820, 44.0858]},
    "83": {"name": "Var", "coordinates": [6.2181, 43.4606]},
    "84": {"name": "Vaucluse", "coordinates": [5.1853, 43.9933]},
    "85": {"name": "Vendée", "coordinates": [-1.2978, 46.6747]},
    "86": {"name": "Vienne", "coordinates": [0.4603, 46.5639]},
    "87": {"name": "Haute-Vienne", "coordinates": [1.2353, 45.8917]},
    "88": {"name": "Vosges", "coordinates": [6.3806, 48.1967]},
    "89": {"name": "Yonne", "coordinates": [3.5644, 47.8397]},
    "90": {"name": "Territoire de Belfort", "coordinates": [6.9286, 47.6317]},
    "91": {"name": "Essonne", "coordinates": [2.2431, 48.5222]},
    "92": {"name": "Hauts-de-Seine", "coordinates": [2.2458, 48.8472]},
    "93": {"name": "Seine-Saint-Denis", "coordinates": [2.4781, 48.9175]},
    "94": {"name": "Val-de-Marne", "coordinates": [2.4689, 48.7775]},
    "95": {"name": "Val-d'Oise", "coordinates": [2.1311, 49.0831]}
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

    department = request.args.get('department', None)
    selected_cuisines = request.args.getlist('cuisine')  

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

    hits = get_all_restaurants(es, index_name)

    # Convertie en DF
    data = pd.DataFrame(hits)

    if department:
        data = data[data['address'].str.startswith(department)]

    if selected_cuisines:
        data = data[data['cuisine'].apply(lambda x: any(cuisine in x for cuisine in selected_cuisines))]


    data['department'] = data['address'].str[:2]
    data = data[data['department'].fillna('0').str.isdigit()] 

    data['department_name'] = data['department'].map(DEPARTMENTS)

    data['rating'] = data['rating'].apply(lambda x: float(x) if isinstance(x, (int, float)) else None)
    data = data[data['rating'].notna()]  
    data['rating'] = data['rating'].apply(lambda x: max(5, min(20, x)))  

    dept_counts = data['department_name'].value_counts().reset_index()
    dept_counts.columns = ['department', 'count']

    geojson_data = create_geojson(dept_counts)

    geojson_path = "FlaskApp/static/geojson_enriched.json"
    with open(geojson_path, 'w') as geojson_file:
        json.dump(geojson_data, geojson_file)

    graph_data = {
        'dept_counts': dept_counts.to_dict(orient='records'),
        'geojson_data': geojson_data,  
        'geojson_path': geojson_path
    }

    rating_histogram = data['rating'].dropna().tolist()
    cuisine_distribution = data['cuisine'].explode().value_counts().reset_index().to_dict(orient='records')

    graph_data['rating_histogram'] = rating_histogram
    graph_data['cuisine_distribution'] = cuisine_distribution

    return render_template('analyse.html', graph_data=graph_data)



def create_geojson(dept_counts):
    """
    Crée un GeoJSON représentant les départements et le nombre de restaurants associés.

    :param dept_counts: DataFrame contenant les départements et leur nombre de restaurants.
    :return: Dictionnaire GeoJSON.
    """
    with open('FlaskApp/static/departements.geojson', 'r') as geojson_file:
        geojson_template = json.load(geojson_file)
    
    for feature in geojson_template['features']:
        department_code = feature['properties']['code']
        feature['properties']['restaurant_count'] = int(
            dept_counts[dept_counts['department'] == department_code]['count'].sum()
        )
    
    return geojson_template

if __name__ == "__main__":
    app.run(debug=True)

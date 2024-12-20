![Static Badge](https://img.shields.io/badge/ESIEE%20Paris%20-%20Projet%20E4%20-%20green?style=flat)
![Static Badge](https://img.shields.io/badge/last%20commit%20-%20November%202024%20-%20blue)
<div align="center">
<img src="https://github.com/user-attachments/assets/78cac6dc-d058-4576-8eef-572581c74311" width="65%"/>
</div>
<a id="readme-top"></a>

# Description

Ce projet vise à extraire des données depuis le site 'gaultmillau.com', les stocker dans une base de données Elasticsearch, et les rendre consultables à travers une application Web créée avec Flask.
Pour offrir une expérience utilisateur fluide, nous avons utilisé Elasticsearch pour optimiser les capacités de recherche et conçu une interface interactive en combinant CSS et JavaScript. Le projet s’appuie sur Docker pour simplifier le déploiement, automatiser l’exécution des différentes étapes (scraping, stockage, service Web) et garantir une reproductibilité optimale sur différents environnements.

<a id="readme-top"></a>
# Sommaire

## Guide de l'utilisateur
1. [Prérequis d'installation](#1---Prérequis-dinstallation)
2. [Installation](#2---Installation)
3. [Lancer le projet](#3---Lancer-le-projet)
4. [Les différentes pages](#4---Les-differentes-pages)

## Guide du Développeur
1. [Aperçu global du projet](#1---Aperçu-global-du-projet)
2. [Scraping](#2---Scraping)
3. [API Web](#3---API-Web)
4. [Architecture et technologies utilisées](#4---Architecture-et-technologies-utilisées)

## Pour aller plus loin
1. [Idées d'améliorations](#1---Idées-daméliorations)
2. [Défis rencontrés](#2---Défis-rencontrés)
3. [Bugs connus](#3---Bugs-connus)


# Guide de l'utilisateur

## 1 - Prérequis d'installation

Dans un premier temps, regardons ce que vous devez installer pour récupérer et utiliser le projet.

Deux outils sont nécessaires :

[Git](https://github.com/cambierelliot/E4-DataEngineerProject) pour cloner le projet depuis le dépôt opensource GitHub.

[DockerDesktop](https://www.docker.com/products/docker-desktop/) pour faire fonctionner le projet.

Faites une installation classique de docker.

## 2 - Installation

Dans cette partie, nous allons importer le projet disponible sur GitHub afin de l’avoir sur votre machine (en local).

Pour ce faire, ouvrez le Git Bash ou tout autre terminal et rendez-vous dans le dossier où vous désirez stocker le projet grâce à la commande :
```
   $ cd <répertoire désiré>/
```
Lorsque vous êtes dans le dossier voulu, rentrez la commande suivante :
```
   $ git clone https://github.com/cambiere/E4-DataEngineerProject
```
⚠ Attendez l'importation totale du projet

## 3 - Lancer le projet

Commencez par rejoindre le dossier du projet :

```
   $ cd E4-DataEngineerProject/
```
Une fois que vous êtes bien dans ce répertoire, veuillez lancer l'application docker (e.g. DockerDesktop sur Windows). Elle doit être en fonctionnement pour continuer.

Pour exécuter le projet, il suffit de rentrer la commande suivante
```
$ docker compose up -d
```


Patientez jusqu'à l'apparition d'un groupe de conteneurs dans votre application Docker. Cela peut prendre quelques minutes, car le processus de scraping est en cours. Un volume est également créé pour les lancements ultérieurs : le scraping ne sera alors plus nécessaire, et les données locales seront utilisées.

⚠ Veillez à ne pas arrêter les services pour le bon fonctionnement de l'application Web.

Une fois le service flask en vert, vous pouvez cliquer sur le port surligné en jaune 5000 :5000 (voir image ci-dessous) ou bien cliquer ici : http://localhost:5000/
![image](https://github.com/user-attachments/assets/aa1cdcf7-a114-42f7-8e11-be71561aa07e)

<p align="center">(<a href="#readme-top">Haut de la page</a>)</p>

## 4 - Les différentes pages

<div align="center">
<h3>Page d'accueil du site</h3>
</div>

![home](img/home.gif)

La page d'accueil du site présente un design élégant et intuitif, permettant aux utilisateurs de rechercher et découvrir des restaurants selon leurs préférences. Voici les principales caractéristiques de cette page :

#### Barre de recherche personnalisée
- Trois menus déroulants pour affiner les critères de recherche :
  - **Département** : Permet de sélectionner une région géographique.
  - **Type de cuisine** : Offre des options comme "Français", "Italien", "Japonais", etc.
  - **Note minimale** : Permet de filtrer les restaurants en fonction de leur score.
- Un bouton **"Rechercher"** pour effectuer la recherche selon les critères sélectionnés.

#### Navigation rapide par types de cuisine
- Une section en dessous de la barre de recherche met en avant **6 types de cuisine populaires**.
- Chaque catégorie est **cliquable** et redirige l'utilisateur vers une page dédiée pour explorer des restaurants spécifiques.

#### Header interactif
- Un header fixe contenant des liens vers les sections principales du site :
  - **Les restaurants**
  - **Analyse**
  - **À propos de nous**
- Le header disparaît automatiquement lors du défilement vers le bas pour laisser plus d'espace à l'utilisateur et réapparaît en haut.

#### Footer informatif
- Le footer inclut des liens supplémentaires, des informations sur les auteurs du projet et un design sobre pour clôturer la page.

<div align="center">
<h3> Page exploration restaurant </h3>
</div>

![resto.gif](img/resto.gif)
La page est dédiée à la recherche et à l'exploration de restaurants. Les principaux composants de la page :

#### Filtres de Recherche de Restaurants
Les utilisateurs peuvent filtrer les restaurants selon plusieurs critères :
- **Curseur de Note** : Un curseur permet de définir une note minimale pour les restaurants recherchés.
- **Menu Déroulant Département** : Un menu déroulant permet aux utilisateurs de sélectionner un département spécifique en France pour affiner la recherche.
- **Cases à Cocher Types de Cuisine** : Un menu déroulant avec des cases à cocher permet aux utilisateurs de sélectionner un ou plusieurs types de cuisine (par exemple, Français, Italien, Japonais).
- **Bouton de Recherche** : Un bouton est disponible pour lancer la recherche selon les filtres sélectionnés.
- **Affichage des Résultats** : La page affiche le nombre de restaurants correspondant aux critères et propose un bouton pour réinitialiser les filtres.

#### Liste des Restaurants
Les restaurants sont affichés sous forme de liste, chacun comprenant :
- **Image** : Une image du restaurant avec sa catégorie.
- **Nom et Note** : Le nom et la note du restaurant.
- **Informations Supplémentaires** : Des détails tels que le nom du chef, le type(s) de cuisine, le budget et l'adresse.

#### Pagination
La liste des restaurants est paginée, et les utilisateurs peuvent naviguer entre plusieurs pages de résultats grâce aux boutons "précédent" et "suivant", ainsi qu'aux liens des numéros de pages.


<div align="center">
<h3> Page d'analyse </h3>
</div>

<div align="center">
<h3> Page a propos de nous </h3>
</div>

![home](img/about.gif)
La page "À propos de nous" présente les contributeurs principaux du projet avec leurs profils respectifs et les outils utilisés dans le développement du site.

- **Présentation des contributeurs** : Chaque contributeur est affiché avec une photo, un descriptif de son parcours, et ses domaines d'expertise.
- **Contact direct** : Les adresses email des contributeurs sont fournies pour toute communication.
- **Technologies utilisées** : Une section en bas met en avant les principaux outils et technologies comme Elasticsearch, Docker, Scrapy, GitHub, et Flask.

<p align="center">(<a href="#readme-top">Haut de la page</a>)</p>

# Guide du Développeur

## 1 - Aperçu global
Le projet propose une solution intégrée permettant de scrapper les données de restaurants depuis **Gault & Millau**, de les stocker dans **MongoDb** et **Elasticsearch**, et de les rendre accessibles via une application web construite avec **Flask**. L'architecture repose sur Docker pour assurer un déploiement reproductible.

## 2 - Scrapping
Le projet utilise **Scrapy** pour effectuer le scraping des données disponibles sur le site Gault&Millau.

Il fonctionne de la manière suivante : 
1. Le scraper navigue sur les pages du site Gault&Millau en suivant une logique de pagination.
2. Il extrait les informations pertinentes pour chaque restaurant, telles que :
   - Nom,
   - Adresse,
   - Chef,
   - Spécialité culinaire,
   - Note (ou catégorie spéciale comme "Membre de l'Académie Gault&Millau"),
   - Budget,
   - URL du restaurant,
   - Photo.
3. Les données extraites sont stockées sous forme d'objets définis par le fichier `items.py`.

## 3 - API Web
Le backend, basé sur **Flask**, offre des endpoints pour :
- Afficher la liste des restaurants.
- Obtenir des détails spécifiques à un restaurant.
- Rechercher par mot-clé ou critères (ex. spécialité, localisation).

N'ayant jamais utilisé **Flask** auparavant, nous avons suivi des tutoriels pour apprendre les bases et développer notre API, notamment la série de cours disponible ici : [Tutoriel Flask sur YouTube](https://www.youtube.com/watch?v=o3bCVqF9gI0&list=PL7yh-TELLS1EyAye_UMnlsTGKxg8uatkM).

L'un d'entre nous avait déjà acquis des compétences en **HTML**, **CSS** et **JavaScript** lors d'un stage d'un mois effectué pendant l'été, ce qui a facilité le développement de la partie frontend de notre projet.

Flask repose sur le principe des **routes**, qui définissent les points d'accès à notre application web. Le fichier principal, `app.py`, joue le rôle de cœur de l'application et redirige les requêtes vers des pages spécifiques, comme `restaurant.html` dans notre cas.

Par exemple, dans la capture ci-dessous, on voit une route définie avec le décorateur `@app.route("/restaurant")`. Cette route est chargée de :

1. **Récupérer les paramètres** de la requête (comme `min_rating`, `department` et `cuisine`).
2. **Construire une requête Elasticsearch** pour filtrer les restaurants.
3. **Envoyer les données filtrées** à la page HTML via `render_template()`.

La page **HTML**, ici `restaurant.html`, reçoit les données renvoyées par Flask (comme la liste des restaurants, les départements uniques et les types de cuisines) pour les afficher dynamiquement sur le frontend.

Ce découpage entre le fichier principal `app.py` (backend) et les fichiers **HTML** (frontend) permet une architecture claire et modulaire. Chaque route dans Flask peut gérer des logiques spécifiques et renvoyer des résultats adaptés à la page correspondante.

<div align="center">
<img src="img/code.png" width="55%"/>
</div>

## 4 - Architecture et technologies utilisées
- **Backend** : Python, Flask.
- **Scraping** : Scrapy
- **Base de données** : Elasticsearch, MongoDB.
- **Frontend** : HTML/CSS/JS.
- **Déploiement** : Docker Compose.

**Pourquoi avons-nous choisit ces technologies ?** 

Nous avons opté pour **MongoDB** et **Elasticsearch** en raison de leur flexibilité dans la gestion des objets et de leur simplicité d'utilisation. Ces bases de données permettent une intégration rapide des données tout en offrant des performances élevées pour la recherche et l'analyse.

Concernant le backend, nous avons choisi **Flask** afin d'explorer une alternative à Dash, utilisé dans un précédent projet lors de la période 1. Flask s'est révélé être un choix pertinent grâce à sa prise en main facile, sa légèreté et ses nombreuses fonctionnalités qui facilitent le développement d'API et d'applications web.

Enfin, l'utilisation de **Docker Compose** permet de simplifier le déploiement et l'orchestration des différents composants de notre architecture, assurant ainsi une solution cohérente et facilement réplicable.

#### Architecture simplifiée de notre application web
![archi.png](img/archi.png)

#### Architecture global du projet
Nous avons segmenté notre code en plusieurs dossiers afin de le rendre plus facilement compréhensible. Deux dossiers principaux structurent notre projet : 

1. **`Api_WEB`** : Ce dossier gère tout ce qui concerne l'application Flask.
2. **`gaultmillau_scraper`** : Ce dossier s'occupe de l'ensemble de la phase de scraping effectuée en amont.

Avantages de cette Architecture : 
- **Modularité** : Lors du développement, il n'est pas nécessaire de pousser l'intégralité du projet sur le dépôt, mais uniquement les branches modifiées, ce qui simplifie la gestion des versions.
- **Lisibilité** : La séparation claire des responsabilités facilite la compréhension et le travail collaboratif sur le projet.


<div align="center">
<img src="img/archicomplet.png" width="45%"/>
</div>

<p align="center">(<a href="#readme-top">Haut de la page</a>)</p>

# Pour aller plus loin

## 1 - Idées d'améliorations
- Ajouter des **filtres dynamiques** (par budget, distance).
- Intégrer une **interface mobile-friendly** ou créer une app mobile.
- Mettre en place une **API REST avancée** pour d’autres types de clients (apps tierces).

## 2 - Défis rencontrés
- Contournement des **limitations des sites web** (CAPTCHA, restrictions IP).
- Optimisation des requêtes Elasticsearch.
- Assurer une **compatibilité front-end** entre navigateurs.

## 3 - Bugs connus
- [en partie résolu] Il se peut qu'une des pages du site de gault et millau soit down et que le scrapping s'arrête plus tôt. La page est donc skip mais reste manquante jusqu'à que les créateurs du site répare le problème
- De temps en temps, suite au scrapping, le graphique réprésentant les notes dans la partie analyse est totalement incohérent (affichant 400 notes à 12 et 12.5 et rien d'autres)

Si vous rencontrez d'autres bugs n'hesitez pas à nous contacter. 

<p align="center">(<a href="#readme-top">Haut de la page</a>)</p>

**Owen et Elliot**

*Notre recette : un projet bien épicé, une pincée de code, et beaucoup de passion. 🧑‍🍳💻*

*Bonne correction et merci pour votre temps ! 😊*

<p align="center">(<a href="#readme-top">Haut de la page</a>)</p>


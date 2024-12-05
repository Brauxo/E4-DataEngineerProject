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





![img.png](img.png)

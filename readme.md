# Sommaire

## Guide de l'utilisateur
1. [Prérequis d'installation](#1---Prérequis-dinstallation)
2. [Installation](#2---Installation)
3. [Lancer le projet](#3---Lancer le projet)


# Guide de l'utilisateur

## 1 - Prérequis d'installation

Dans un premier temps, regardons ce que vous devez installer pour récupérer et utiliser le projet.

Deux outils sont nécessaires :

*Git* pour cloner le projet depuis le dépôt opensource GitHub.

*DockerDesktop* pour faire fonctionner le projet.

Faites une installation classique.

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

<p align="right">(<a href="#readme-top">back to top</a>)</p>




![img.png](img.png)

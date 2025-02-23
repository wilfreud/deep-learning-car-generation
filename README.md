# Prédiction de Prix et Génération d'Images

### M2GLSI (j)

## Description du Mini-Projet

Ce mini-projet est composé de deux parties distinctes : un client React pour l'envoi de la description d'un véhicule et un backend en Python, utilisant FastAPI, pour effectuer la prédiction de prix et générer des images via Stable Diffusion.

---

## Architecture du Projet

- **Frontend (Client React)** : L'application React permet à l'utilisateur de saisir une description d'un véhicule. Cette description est envoyée au backend via une API REST pour la prédiction du prix et la génération d'une image associée.
- **Backend (FastAPI en Python)** : Le backend utilise FastAPI pour exposer une API REST permettant de :
  - Charger un modèle de prédiction préexistant pour estimer le prix d'un véhicule basé sur des features d'entrée.
  - Utiliser le modèle Stable Diffusion pour générer une image basée sur la description du véhicule et le prix prédit.

Le backend est accessible sur l'URL suivante :  
`http://localhost:8000/generate` (endpoint pour générer l'image et obtenir la prédiction de prix).

---

## Prérequis

Avant de démarrer le projet, assurez-vous d'avoir installé les éléments suivants :

- **Python 3.x** : Assurez-vous d'avoir Python 3 installé sur votre machine.
- **Keras** : Utilisé pour charger et exécuter le modèle de prédiction.
- **Diffusers** : Bibliothèque permettant de charger et d'utiliser le modèle Stable Diffusion pour la génération d'images.
- **FastAPI** : Framework web utilisé pour construire l'API REST.
- **Uvicorn** : Serveur ASGI pour exécuter l'application FastAPI.

Les dépendances nécessaires sont listées dans le fichier `requirements.txt`. Vous pouvez les installer en exécutant :

```bash
pip install -r requirements.txt
```

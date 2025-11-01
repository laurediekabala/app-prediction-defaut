# Service de Prédiction de Défaut de Paiement

Ce composant est responsable de l'évaluation du risque de défaut de paiement des clients bancaires en utilisant un modèle XGBoost. Il analyse les caractéristiques financières et comportementales des clients pour prédire la probabilité qu'un client ne rembourse pas son prêt.

## Fonctionnalités

- API REST avec Flask
- Modèle de prédiction XGBoost
- Tests unitaires
- Conteneurisation avec Docker

## Installation

```bash
pip install -r requirements.txt
```

## Démarrage

Pour lancer le service de prédiction :

```bash
python prediction.py
```

## Docker

Pour construire et exécuter avec Docker :

```bash
docker build -t prediction-service .
docker run -p 5000:5000 prediction-service
```

## Structure des Fichiers

- `prediction.py` : Service principal de prédiction
- `test.py` : Tests unitaires
- `xboost.joblib` : Modèle XGBoost sauvegardé
- `requirements.txt` : Dépendances du projet
- `Dockerfile` : Configuration Docker
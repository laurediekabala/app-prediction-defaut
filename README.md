# Application de Prédiction de Défaut de Paiement Bancaire

Cette application permet de prédire le risque de défaut de paiement des clients d'une banque en utilisant des techniques d'apprentissage automatique. Elle aide les institutions bancaires à évaluer les risques associés à chaque client en analysant leurs données financières et comportementales.

L'application est composée de deux composants principaux :
- Une interface utilisateur web construite avec Streamlit pour visualiser et analyser les prédictions
- Un service de prédiction basé sur Flask utilisant un modèle XGBoost pour évaluer les risques


## Structure du Projet

```
application_default/
├── appstreamlit/        # Interface utilisateur Streamlit
├── prediction/          # Service de prédiction
├── assets/             # Fichiers CSS et styles
├── connection/         # Gestion de l'authentification
├── dataset/           # Jeux de données
├── traitement/        # Traitement des données
└── utils/             # Utilitaires
```

## Prérequis

- Python 3.11+
- Les dépendances listées dans les fichiers `requirements.txt` de chaque composant

## Installation

1. Clonez le repository
2. Installez les dépendances de l'interface Streamlit :
```bash
cd appstreamlit
pip install -r requirements.txt
```

3. Installez les dépendances du service de prédiction :
```bash
cd ../prediction
pip install -r requirements.txt
```

## Démarrage de l'Application

1. Lancez le service de prédiction :
```bash
cd prediction
python prediction.py
```

2. Dans un autre terminal, lancez l'interface Streamlit :
```bash
cd appstreamlit
streamlit run app.py
```
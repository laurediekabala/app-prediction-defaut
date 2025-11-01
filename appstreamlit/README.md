# Interface Utilisateur Streamlit - Prédiction de Défaut de Paiement

Cette partie du projet contient l'interface utilisateur web construite avec Streamlit pour l'analyse et la prédiction des défauts de paiement des clients bancaires. Elle permet aux analystes et gestionnaires de risques d'évaluer rapidement la probabilité de défaut de paiement d'un client.

## Fonctionnalités

- Interface utilisateur interactive
- Visualisation de données avec plotly et matplotlib
- Analyse des prédictions avec SHAP
- Menu d'options pour la navigation
- Gestion de l'authentification des utilisateurs

## Installation

```bash
pip install -r requirements.txt
```

## Démarrage

Pour lancer l'application Streamlit :

```bash
streamlit run app.py
```

## Structure des Fichiers

- `app.py` : Point d'entrée de l'application
- `analyse.py` : Fonctionnalités d'analyse des données
- `home.py` : Page d'accueil
- `machinelearning.py` : Logique de prédiction
- `requirements.txt` : Dépendances du projet
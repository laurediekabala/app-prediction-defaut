# Image de base Python 3.11
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier l'application Streamlit
COPY ./appstreamlit /app/appstreamlit

# Copier les autres dossiers nécessaires
COPY ./config /app/config
COPY ./assets /app/assets
COPY ./connection /app/connection
COPY ./dataset /app/dataset
COPY ./assets /app/assets
COPY ./traitement /app/traitement
COPY ./utils /app/utils
COPY ./xboost.joblib /app/xboost.joblib

# Copier les fichiers de base de données
COPY ./user.db /app/user.db
COPY ./users.db /app/users.db

# Définir le répertoire de travail sur l’app Streamlit
WORKDIR /app/streamlit

# Installer les dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exposer le port Streamlit
EXPOSE 8501

# Lancer Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

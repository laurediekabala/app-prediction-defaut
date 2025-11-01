# Utiliser Python 3.11.5 officiel
FROM python:3.11.5-slim

# Définir le répertoire de travail
WORKDIR /appstreamlit

# Copier les fichiers requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application
COPY . .

# Exposer le port Streamlit
EXPOSE 8501

# Lancer l'application Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
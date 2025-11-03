# =========================
# Dockerfile Streamlit App
# =========================

# Image de base
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le contenu du dossier Streamlit
COPY . /app
# ✅ Ajouter appstreamlit au PYTHONPATH pour que les imports internes fonctionnent
# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port Streamlit
EXPOSE 8501

# Lancer l'application
CMD ["streamlit", "run","app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# =========================
# Dockerfile Streamlit App - DÉFINITIF
# =========================

# 1. Image de base : Passer à la version Debian complète pour plus de fiabilité.
# Cette image inclut les outils de compilation et les librairies runtime C/Fortran nécessaires.
FROM python:3.11

# 2. Définir le répertoire de travail
WORKDIR /app

# 3. Supprimer l'installation des outils système (car ils sont inclus dans l'image complète)
# Si jamais vous aviez besoin d'autres dépendances, vous les ajouteriez ici, par exemple :
# RUN apt-get update && apt-get install -y ffmpeg

# 4. Copier UNIQUEMENT le fichier des exigences d'abord (Meilleure gestion du cache Docker)
COPY requirements.txt .

# 5. Installer les dépendances
# Utilisez le drapeau --prefer-binary pour forcer l'utilisation des roues (wheels) précompilées
RUN pip install --upgrade pip
RUN pip install --default-timeout=1000 --no-cache-dir --prefer-binary -r requirements.txt

# 6. Copier le contenu de l'application (Streamlit et autres fichiers)
COPY . /app

# Exposer le port Streamlit
EXPOSE 8501

# Lancer l'application
CMD ["streamlit", "run","app.py", "--server.port=8501", "--server.address=0.0.0.0"]
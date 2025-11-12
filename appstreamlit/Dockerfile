# =========================================================================
# Dockerfile Streamlit App - Version Slim (Optimisée pour NumPy)
# Ce fichier utilise l'image slim pour un conteneur plus petit,
# tout en incluant les dépendances système nécessaires pour NumPy et SciPy.
# =========================================================================

# 1. Image de base : python:3.11-slim pour une taille réduite.
FROM python:3.11-slim

# 2. Définir le répertoire de travail dans le conteneur
WORKDIR /app

# 3. Installation des dépendances système nécessaires à la compilation de librairies comme NumPy
#    - build-essential & python3-dev : Outils de compilation essentiels.
#    - libgfortran5 : Librairie Fortran requise par NumPy et SciPy pour les calculs optimisés.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libgfortran5 \
    # Nettoyage pour réduire la taille finale (supprime les listes de paquets)
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4. Copier UNIQUEMENT le fichier des exigences d'abord (Meilleure gestion du cache Docker)
COPY requirements.txt .

# 5. Installer les dépendances Python
# Utiliser --prefer-binary et --upgrade pour garantir une installation propre et stable.
RUN pip install --upgrade pip
RUN pip install --default-timeout=1000 --no-cache-dir --prefer-binary --upgrade -r requirements.txt \
    # Nettoyage du cache pip
    && rm -rf /root/.cache/pip

# 6. Copier le contenu de l'application (Streamlit et autres fichiers)
COPY . /app

# 7. Exposer le port Streamlit
EXPOSE 8501

# 8. Lancer l'application
CMD ["streamlit", "run","app.py", "--server.port=8501", "--server.address=0.0.0.0"]
# =========================================================================
# Dockerfile Streamlit App - Version Slim (Optimisée pour NumPy et SciPy)
# Cette version inclut toutes les librairies système requises (BLAS/LAPACK)
# pour une installation réussie de vos packages de Data Science.
# =========================================================================

# 1. Image de base : python:3.11-slim pour une taille réduite.
FROM python:3.11-slim

# 2. Définir le répertoire de travail dans le conteneur
WORKDIR /app

# 3. Installation des dépendances système critiques
# Cette étape est cruciale pour résoudre le problème 'numpy.core'
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Outils de compilation essentiels
    build-essential \
    python3-dev \
    # Librairies pour l'algèbre linéaire (BLAS/LAPACK) : CRITICAL
    libopenblas-dev \
    liblapack-dev \
    # Librairie Fortran requise par SciPy et certaines parties de NumPy
    libgfortran5 \
    # Nettoyage pour réduire la taille finale
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4. Copier UNIQUEMENT le fichier des exigences d'abord (Meilleure gestion du cache Docker)
COPY requirements.txt .

# 5. Installer les dépendances Python
# Utilisation de --prefer-binary pour des wheels précompilées, plus stable.
RUN pip install --upgrade pip
RUN pip install --default-timeout=1000 --no-cache-dir --prefer-binary -r requirements.txt

# Optionnel mais recommandé : Nettoyage du cache pip
RUN rm -rf /root/.cache/pip

# 6. Copier le contenu de l'application (Streamlit et autres fichiers)
COPY . /app

# 7. Exposer le port Streamlit
EXPOSE 8501

# 8. Lancer l'application
CMD ["streamlit", "run","app.py", "--server.port=8501", "--server.address=0.0.0.0"]
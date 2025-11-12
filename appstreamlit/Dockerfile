# =========================
# Dockerfile Streamlit App - Version Slim (Optimisée)
# =========================

# 1. Image de base : Passer à la version SLIM pour réduire la taille du conteneur
FROM python:3.11-slim

# 2. Définir le répertoire de travail
WORKDIR /app

# 3. Installation des dépendances système pour NumPy/SciPy
# C'est l'étape critique. Nous installons les outils de compilation et les librairies Fortran.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libgfortran5 \
    # Nettoyage pour réduire la taille finale (supprime les listes de paquets)
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /root/.cache/pip

# 4. Copier UNIQUEMENT le fichier des exigences d'abord (Meilleure gestion du cache Docker)
COPY requirements.txt .

# 5. Installer les dépendances Python
RUN pip install --upgrade pip
RUN pip install --default-timeout=1000 --no-cache-dir --prefer-binary --upgrade -r requirements.txt \
    # Nettoyage du cache pip
    && rm -rf /root/.cache/pip

# 6. Copier le contenu de l'application (Streamlit et autres fichiers)
COPY . /app

# Exposer le port Streamlit
EXPOSE 8501

# Lancer l'application
CMD ["streamlit", "run","app.py", "--server.port=8501", "--server.address=0.0.0.0"]
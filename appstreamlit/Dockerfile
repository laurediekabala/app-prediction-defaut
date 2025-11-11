# =========================
# Dockerfile Streamlit App - CORRIGÉ
# =========================

# 1. Utiliser une image Python plus complète ou une image slim avec les outils de construction
# L'image 'buster' ou 'bullseye' est recommandée pour la Data Science car elle inclut plus de dépendances système.
# Nous allons rester sur 'slim' mais ajouter les outils de construction.
FROM python:3.11-slim

# 2. Définir le répertoire de travail
WORKDIR /app

# 3. Installer les dépendances système nécessaires à la compilation (CRITIQUE pour NumPy/SciPy)
# build-essential et python3-dev sont nécessaires pour la compilation C/C++ des libs scientifiques.
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    # Optionnel: Nettoyage pour réduire la taille du conteneur
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4. Copier UNIQUEMENT le fichier des exigences d'abord (Meilleure gestion du cache Docker)
COPY requirements.txt .

# 5. Installer les dépendances (avec le timeout augmenté comme vous l'aviez fait)
RUN pip install --upgrade pip
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# 6. Copier le contenu de l'application (Streamlit et autres fichiers)
COPY . /app

# Exposer le port Streamlit
EXPOSE 8501

# Lancer l'application
CMD ["streamlit", "run","app.py", "--server.port=8501", "--server.address=0.0.0.0"]
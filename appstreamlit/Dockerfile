# =========================================================================
# Dockerfile Streamlit App - Version Standard (La plus fiable)
# Utilise l'image Python complète, qui est plus stable pour les librairies
# scientifiques comme NumPy, Pandas et SciPy.
# =========================================================================

# 1. Image de base : python:3.11 (Image Debian standard)
FROM python:3.11

# 2. Définir le répertoire de travail dans le conteneur
WORKDIR /app

# 3. L'installation des dépendances système devient inutile, car elles sont incluses.
#    -> Étape 3 de l'ancien Dockerfile est supprimée.

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
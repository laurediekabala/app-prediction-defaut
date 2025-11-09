# ---- Étape 1 : Image de base légère ----
FROM python:3.11-slim AS base

# Empêcher la création de fichiers .pyc et activer les logs directs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Créer le dossier de travail
WORKDIR /app

# ---- Étape 2 : Installation des dépendances système ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libatlas-base-dev \
    liblapack-dev \
    gfortran \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ---- Étape 3 : Installer les dépendances Python ----
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# ---- Étape 4 : Copier tout le code de ton application ----
# Ici, on copie tout le contenu du dossier courant (y compris les sous-dossiers)
COPY . .

# ---- Étape 5 : Port et commande de démarrage ----
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

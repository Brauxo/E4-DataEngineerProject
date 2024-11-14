# Utilise l'image Python
FROM python:3.9

# Définit le répertoire de travail
WORKDIR /app

# Copie les dépendances et les installe
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copie le reste du code
COPY . .

# Définit la commande de lancement de Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

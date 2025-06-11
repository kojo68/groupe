# Utiliser une image de base Python
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /code

# Copier les fichiers requirements.txt et installer les dépendances
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application (y compris le worker.py)
COPY . /code/

# Définir les variables d'environnement
ENV DJANGO_DB_HOST=db
ENV DJANGO_DB_NAME=boutique
ENV DJANGO_DB_USER=user
ENV DJANGO_DB_PASSWORD=password

# Exposer le port de l'application Django
EXPOSE 8000

# Lancer le serveur de développement Django par défaut
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

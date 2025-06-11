# Application Boutique - Django + RabbitMQ

Ce dépôt contient un petit projet **Django** illustrant l'envoi de messages dans une file RabbitMQ puis leur traitement par un *worker* qui les enregistre dans PostgreSQL.

## Prérequis
- [Docker](https://www.docker.com/) et [Docker Compose](https://docs.docker.com/compose/) installés.
- Facultatif : Python 3.10+ si vous souhaitez exécuter l'application sans Docker.

## Démarrage rapide avec Docker
1. Construisez et lancez l'ensemble des services :
   ```bash
   docker-compose up --build
   ```
   Trois conteneurs démarrent :
   - **web** : l'application Django exposée sur `http://localhost:8001/`.
   - **db** : PostgreSQL.
   - **rabbitmq** : serveur RabbitMQ (interface sur `http://localhost:15672`, identifiants `guest`/`guest`).
2. Dans un autre terminal, exécutez le *worker* qui consommera la file `commandes` :
   ```bash
   docker-compose exec web python worker.py
   ```
3. Créez une table `boutique_log` dans la base si elle n'existe pas :
   ```sql
   CREATE TABLE boutique_log (
       id SERIAL PRIMARY KEY,
       message TEXT,
       created_at TIMESTAMP
   );
   ```
4. Rendez-vous sur `http://localhost:8001/` et cliquez sur **Acheter** pour envoyer un message.
   Le *worker* affiche le message reçu et l'insère dans la base.

## Utilisation sans Docker (optionnel)
1. Installez les dépendances Python :
   ```bash
   pip install -r requirements.txt
   ```
2. Assurez-vous de disposer d'une instance PostgreSQL et RabbitMQ accessibles, puis configurez les variables d'environnement :
   `DJANGO_DB_HOST`, `DJANGO_DB_NAME`, `DJANGO_DB_USER`, `DJANGO_DB_PASSWORD`.
3. Lancez le serveur :
   ```bash
   python manage.py runserver
   ```
4. Démarrez `worker.py` de la même manière que ci-dessus.


## CI/CD
Une *pipeline* GitHub Actions (`.github/workflows/ci.yml`) vérifie automatiquement le code :

1. Installation des dépendances et lancement de `flake8` puis `pytest`.
2. Analyse de la qualité via **SonarCloud**.

Renseignez les secrets `SONAR_TOKEN`, `SONAR_PROJECT_KEY` et `SONAR_ORGANIZATION` dans les paramètres du dépôt pour activer l'analyse.

## Arborescence principale
```
Dockerfile           # Image Docker de l'application
README.md            # Ce fichier
docker-compose.yml   # Définition des services web/db/rabbitmq
requirements.txt     # Dépendances Python
shop/
├── manage.py        # Entrée du projet Django
├── worker.py        # Consommateur RabbitMQ
├── boutique/        # Application Django (vues, templates)
└── shop/            # Configuration du projet (settings, urls)
```

## Contribution
Les propositions d'améliorations ou de correctifs sont les bienvenues ! Forkez le dépôt, créez une branche et ouvrez une merge request.

import pika
import psycopg2

# Connexion à RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='commandes')

# Connexion PostgreSQL
conn = psycopg2.connect(
    dbname='boutique',
    user='user',
    password='password',
    host='db'
)
cursor = conn.cursor()

def callback(ch, method, properties, body):
    print(f" [x] Reçu: {body.decode()}")  # Le print ici affiche le message reçu
    try:
        cursor.execute("INSERT INTO boutique_log (message, created_at) VALUES (%s, NOW())", (body.decode(),))
        conn.commit()
        print("Message inséré avec succès dans la base de données")  # Affiche un message après l'insertion
    except Exception as e:
        print(f"Erreur d'insertion dans la base de données: {e}")
        conn.rollback()

channel.basic_consume(queue='commandes', on_message_callback=callback, auto_ack=True)

print(' [*] En attente de messages...')
channel.start_consuming()

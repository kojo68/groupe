
from django.shortcuts import render
import pika

def acheter(request):
    message = ""
    if request.method == "POST":
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="rabbitmq")
            )
            channel = connection.channel()
            channel.queue_declare(queue="commandes")
            channel.basic_publish(exchange='', routing_key='commandes', body='maillot acheté')
            connection.close()
            message = "Commande envoyée avec succès !"
        except Exception as e:
            message = f"Erreur lors de l'envoi : {str(e)}"
    return render(request, "acheter.html", {"message": message})

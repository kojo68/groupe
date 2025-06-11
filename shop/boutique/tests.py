from django.test import TestCase, Client
from django.conf import settings
from unittest.mock import patch, MagicMock
from django.urls import reverse

# Use SQLite for tests to avoid requiring PostgreSQL
settings.DATABASES["default"].update(
    {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
)


class AcheterViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_acheter_returns_page(self):
        response = self.client.get(reverse('acheter'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h2>Acheter un maillot</h2>', html=True)

    @patch('boutique.views.pika.BlockingConnection')
    def test_post_acheter_sends_message(self, mock_connection):
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel

        response = self.client.post(reverse('acheter'))

        self.assertEqual(response.status_code, 200)
        mock_connection.assert_called()
        mock_channel.queue_declare.assert_called_with(queue='commandes')
        mock_channel.basic_publish.assert_called_with(
            exchange='', routing_key='commandes', body='maillot acheté'
        )
        self.assertContains(response, 'Commande envoyée avec succès !')

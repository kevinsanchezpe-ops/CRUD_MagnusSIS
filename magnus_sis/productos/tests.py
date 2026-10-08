from django.test import TestCase
from django.urls import reverse


class HumoTests(TestCase):
    def test_lista_responde(self):
        self.assertEqual(self.client.get(reverse('productos:lista')).status_code, 200)

    def test_formulario_responde(self):
        self.assertEqual(self.client.get(reverse('productos:crear')).status_code, 200)

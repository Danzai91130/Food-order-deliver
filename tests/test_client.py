# test_client.py
from src.classes.client import Client

def test_creation_client():
    # Création d'un client
    client = Client("John Doe", "john@example.com")

    # Vérification des attributs du client
    assert client.nom == "John Doe"
    assert client.email == "john@example.com"

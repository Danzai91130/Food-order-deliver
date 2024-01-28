# test_commande.py
from src.classes.client import Client
from src.classes.sandwich import Sandwich
from src.classes.commande import Commande

def test_creation_commande():
    # Création d'un client
    client = Client("Alice", "alice@example.com")

    # Création de plusieurs sandwiches
    sandwich1 = Sandwich("Jambon-Fromage", "Jambon", ["Mayonnaise"], ["Salade", "Tomate"])
    sandwich2 = Sandwich("Poulet Algérien", "Poulet", ["Algérienne"], ["Oignons"])

    # Création d'une commande avec ces sandwiches
    commande = Commande(client, [sandwich1, sandwich2])

    # Vérification des détails de la commande
    assert commande.client == client
    assert commande.sandwichs == [sandwich1, sandwich2]

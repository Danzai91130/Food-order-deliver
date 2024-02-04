import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Check if Firebase app is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("secrets/order-page-c92f2-firebase-adminsdk-e270q-2bea0532f9.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()


def inserer_client(nom, email):
    """Insère un client dans la base de données."""
    _,client_ref = db.collection('clients').add({
        'nom': nom,
        'email': email
    })
    print(type(client_ref))
    print(client_ref)
    print(f"Added document with id {client_ref.id}")
    return client_ref.id

def inserer_commande_sandwich(id_client, nom_sandwich, proteine, sauces, ingredients):
    """Insère une commande de sandwich dans la base de données."""
    _,commande_ref = db.collection('commandes_sandwichs').add({
        'id_client': id_client,
        'nom_sandwich': nom_sandwich,
        'proteine': proteine,
        'sauces': sauces,
        'ingredients': ingredients,
        'preparee': False  # Firestore does not have boolean, so use False instead of 0
    })
    return commande_ref.id

def marquer_commande_preparee(db,id_commande):
    """Marque une commande comme préparée dans la base de données."""
    commande_ref = db.collection('commandes_sandwichs').document(id_commande)
    commande_ref.update({
        'preparee': True
    })


# Code de test pour vérifier le bon fonctionnement des fonctions
if __name__ == "__main__":

    # Insertion d'un client
    inserer_client("John Doe", "john@example.com")

    # Insertion d'une commande de sandwich
    inserer_commande_sandwich( 1, "Jambon-Fromage", "Jambon", "Mayonnaise", "Salade, Tomate")
    
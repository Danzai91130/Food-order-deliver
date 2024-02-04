import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Check if Firebase app is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("secrets/order-page-c92f2-firebase-adminsdk-e270q-2bea0532f9.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
# Fonction pour enregistrer un nouveau client
def enregistrer_nouveau_client(nom, email):
    db.collection('clients').add({
        'nom': nom,
        'email': email
    })

# Fonction pour passer une nouvelle commande
def passer_nouvelle_commande(nom_client, email_client, nom_sandwich, proteine, sauces, ingredients):
    client_ref = db.collection('clients').add({
        'nom': nom_client,
        'email': email_client
    })
    client_id = client_ref.id

    commande_ref = db.collection('commandes_sandwichs').add({
        'id_client': client_id,
        'nom_sandwich': nom_sandwich,
        'proteine': proteine,
        'sauces': sauces,
        'ingredients': ingredients,
        'preparee': False
    })

    commande_id = commande_ref.id
    return commande_id

# Fonction pour récupérer les détails d'une commande depuis la base de données
def recuperer_details_commande(db,non_prepares_seulement=False):
    query = db.collection('commandes_sandwichs').where('preparee', '==', False).limit(1) if non_prepares_seulement else db.collection('commandes_sandwichs').limit(1)
    commandes = query.get()

    for commande in commandes:
        commande_data = commande.to_dict()
        client_ref = db.collection('clients').document(commande_data['id_client'])
        client_data = client_ref.get().to_dict()
        
        return {
            'id': commande.id,
            'nom_client': client_data['nom'],
            'email_client': client_data['email'],
            'nom_sandwich': commande_data['nom_sandwich'],
            'proteine': commande_data['proteine'],
            'sauces': commande_data['sauces'],
            'ingredients': commande_data['ingredients']
        }

    return None

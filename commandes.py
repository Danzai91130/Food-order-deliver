import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


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

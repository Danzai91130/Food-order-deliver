import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def recuperer_details_commande(db, non_prepares_seulement=False):
    # Query for orders where commande_enfant is True
    query_enfant = db.collection('commandes_sandwichs').where('commande_enfant', '==', True)
    if non_prepares_seulement:
        query_enfant = query_enfant.where('preparee', '==', False)
    commandes_enfant = query_enfant.limit(1).get()
    commandes_enfant_nb = query_enfant.get()
    # Count remaining commandes_enfant
    nombre_commandes_enfant_restantes = len(commandes_enfant_nb)

    # Check if there are any orders with commande_enfant == True
    if commandes_enfant:
        for commande in commandes_enfant:
            commande_data = commande.to_dict()
            client_ref = db.collection('clients').document(commande_data['id_client'])
            client_data = client_ref.get().to_dict()

            return {
                'id': commande.id,
                'nom_client': client_data['nom'],
                'prenom_client': client_data['prenom'],
                'email_client': client_data['email'],
                'proteine': commande_data['proteine'],
                'sauces': commande_data['sauces'],
                'ingredients': commande_data['ingredients'],
                'commande_enfant': commande_data['commande_enfant'],
                'nombre_commandes_restantes': nombre_commandes_enfant_restantes - 1  # Minus the one we're returning
            }

    # If no commande_enfant == True, query for all orders
    query_nom = db.collection('commandes_sandwichs')
    if non_prepares_seulement:
        query_nom = query_nom.where('preparee', '==', False)
    commandes_nom = query_nom.get()

    # Count remaining commandes_nom
    nombre_commandes_nom_restantes = len(commandes_nom)

    commandes_nom_list = []
    # Get client information and append to commandes_nom_list
    for commande in commandes_nom:
        commande_data = commande.to_dict()
        client_ref = db.collection('clients').document(commande_data['id_client'])
        client_data = client_ref.get().to_dict()
        commande_data.update({
            'nom_client': client_data['nom'],
            'prenom_client': client_data['prenom'],
            'email_client': client_data['email']
        })
        commandes_nom_list.append((commande.id, commande_data))

    # Sort the commandes_nom_list by 'nom_client'
    commandes_nom_list.sort(key=lambda x: x[1]['nom_client'])

    # Return the first order from the sorted list
    if commandes_nom_list:
        commande_id, commande_data = commandes_nom_list[0]
        return {
            'id': commande_id,
            'nom_client': commande_data['nom_client'],
            'prenom_client': commande_data['prenom_client'],
            'email_client': commande_data['email_client'],
            'proteine': commande_data['proteine'],
            'sauces': commande_data['sauces'],
            'ingredients': commande_data['ingredients'],
            'commande_enfant': commande_data['commande_enfant'],
            'nombre_commandes_restantes': nombre_commandes_nom_restantes - 1  # Minus the one we're returning
        }

    return None

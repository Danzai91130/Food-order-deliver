
def inserer_client(db,nom, email):
    """Insère un client dans la base de données."""
    _,client_ref = db.collection('clients').add({
        'nom': nom,
        'email': email
    })
    print(type(client_ref))
    print(client_ref)
    print(f"Added document with id {client_ref.id}")
    return client_ref.id

def inserer_commande_sandwich(db,id_client, nom_sandwich, proteine, sauces, ingredients):
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


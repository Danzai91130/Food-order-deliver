from datetime import datetime

from commandes import recuperer_details_commande

def inserer_client(db, nom, email):
    """Insère un client dans la base de données."""
    _, client_ref = db.collection('clients').add({
        'nom': nom,
        'email': email
    })
    print(type(client_ref))
    print(client_ref)
    print(f"Added document with id {client_ref.id}")
    return client_ref.id

def inserer_commande_sandwich(db, id_client, nom_sandwich, proteine, sauces, ingredients):
    """Insère une commande de sandwich dans la base de données."""
    placement_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    _, commande_ref = db.collection('commandes_sandwichs').add({
        'id_client': id_client,
        'nom_sandwich': nom_sandwich,
        'proteine': proteine,
        'sauces': sauces,
        'ingredients': ingredients,
        'preparee': False,
        'placement_time': placement_time
    })
    return commande_ref.id

def marquer_commande_preparee(db, id_commande):
    """Marque une commande comme préparée dans la base de données."""
    commande_ref = db.collection('commandes_sandwichs').document(id_commande)
    commande_ref.update({
        'preparee': True,
    })

def set_all_preparee_false(db):
    """Set all 'preparee' attributes to False in the 'commandes_sandwichs' collection."""
    sandwiches_ref = db.collection('commandes_sandwichs')
    sandwiches = sandwiches_ref.get()
    for sandwich in sandwiches:
        sandwich_ref = sandwiches_ref.document(sandwich.id)
        sandwich_ref.update({'preparee': False})
    print("All 'preparee' attributes set to False.")

def set_completion_time(db, order_id):
    """Set completion time for the order and placement time for the next upcoming order."""
    order_ref = db.collection('commandes_sandwichs').document(order_id)
    completion_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    order_ref.update({'completion_time': completion_time})
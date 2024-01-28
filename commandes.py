# Import des classes et des fonctions nécessaires
from stockage import creer_tables, inserer_client, inserer_commande_sandwich, creer_connexion
from src.classes.client import Client
from src.classes.sandwich import Sandwich
from src.classes.commande import Commande

# Fonction pour enregistrer un nouveau client
def enregistrer_nouveau_client(nom, email):
    inserer_client(nom, email)

# Fonction pour passer une nouvelle commande
def passer_nouvelle_commande(nom_client, email_client, nom_sandwich, proteine, sauces, ingredients):
    conn = creer_connexion()
    client = Client(nom_client, email_client)
    sandwich = Sandwich(nom_sandwich, proteine, sauces, ingredients)
    commande = Commande(client, sandwich)
    inserer_commande_sandwich(conn, client.id, sandwich.nom, sandwich.proteine, sandwich.sauces, sandwich.ingredients)
    conn.close()
    return commande

# Fonction pour récupérer les détails d'une commande depuis la base de données
def recuperer_details_commande(non_prepares_seulement=False):
    conn = creer_connexion()
    cursor = conn.cursor()

    # Requête SQL pour récupérer les détails de la première commande non préparée
    if non_prepares_seulement:
        cursor.execute("""SELECT cs.id, c.nom, c.email, cs.nom_sandwich, cs.proteine, cs.sauces, cs.ingredients
                          FROM commandes_sandwichs AS cs
                          JOIN clients AS c ON cs.id_client = c.id
                          WHERE cs.preparee = 0
                          ORDER BY cs.id
                          LIMIT 1""")
    else:
        cursor.execute("""SELECT cs.id, c.nom, c.email, cs.nom_sandwich, cs.proteine, cs.sauces, cs.ingredients
                          FROM commandes_sandwichs AS cs
                          JOIN clients AS c ON cs.id_client = c.id
                          ORDER BY cs.id
                          LIMIT 1""")

    # Récupération de la première commande trouvée
    commande = cursor.fetchone()

    # Fermeture de la connexion à la base de données
    conn.close()

    # Si une commande a été trouvée, retourne ses détails
    if commande:
        # Convertit les détails de la commande en un objet ou une structure de données appropriée
        details_commande = {
            "id": commande[0],
            "nom_client": commande[1],
            "email_client": commande[2],
            "nom_sandwich": commande[3],
            "proteine": commande[4],
            "sauces": commande[5],
            "ingredients": commande[6]
        }
        return details_commande
    else:
        return None



# Autres fonctions nécessaires...

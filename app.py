import hashlib
import streamlit as st
import os
from src.classes.commande import  Commande
from src.classes.client import Client
from src.classes.sandwich import Sandwich
from src.utils import envoyer_email
from stockage import creer_connexion, inserer_commande_sandwich, inserer_client
# Variable pour stocker le mot de passe administrateur
MOT_DE_PASSE_ADMIN = "mot_de_passe_securise"

# Fonction d'authentification
def authentification():
    mdp_key = hashlib.md5("mdp".encode()).hexdigest()
    # Champ de saisie pour le mot de passe
    mot_de_passe = st.text_input("Mot de passe", type="password", key = mdp_key)

    # Vérifie si le mot de passe est correct
    if mot_de_passe == MOT_DE_PASSE_ADMIN:
        return True
    else:
        return False
    
# Ingrédients disponibles
ingredients_disponibles = ["Salade", "Tomate", "Oignons", "Fromage"]

# Sauces disponibles
sauces_disponibles = ["Mayonnaise", "Ketchup", "Algerienne","Samourai","Harissa", "BBQ"]

# Protéines disponibles
proteines_disponibles = ["Jambon", "Poulet"]

# Interface utilisateur pour commander un sandwich
def commande_sandwich():
    st.title("Commander un Sandwich")

    #Générer une clé unique pour chaque widget en utilisant une fonction de hachage
    nom_key = hashlib.md5("Nom".encode()).hexdigest()
    email_key = hashlib.md5("Email".encode()).hexdigest()
    nom_sandwich_key = hashlib.md5("Nommme ton sandwich du turfu".encode()).hexdigest()
    ingredients_key = hashlib.md5("ingredient_select".encode()).hexdigest()
    sauces_key = hashlib.md5("sauces_select".encode()).hexdigest()
    proteines_key = hashlib.md5("proteines_select".encode()).hexdigest()

    # Saisie du nom et de l'email
    nom = st.text_input("Nom", key=nom_key)
    email = st.text_input("Email", key=email_key)
    nom_sandwich = st.text_input("Nommme ton sandwich du turfu", key=nom_sandwich_key)


    # Sélection des ingrédients
    ingredients_selectionnes = st.multiselect("Sélectionnez les ingrédients", ingredients_disponibles, key = ingredients_key)

    # Sélection des sauces
    sauces_selectionnees = st.multiselect("Sélectionnez les sauces", sauces_disponibles, key = sauces_key)

    # Sélection des protéines
    proteines_selectionnees = st.selectbox("Sélectionnez les protéines", proteines_disponibles, key = proteines_key)

    if st.button("Commander"):
        # Création de l'objet Client
        client = Client(nom, email)

        # Création de l'objet Sandwich
        sandwich = Sandwich(nom_sandwich, proteines_selectionnees, sauces_selectionnees, ingredients_selectionnes)

        # Création de l'objet Commande avec le client et le sandwich
        commande = Commande(client, sandwich)

        #Connexion a la BDD
        conn = creer_connexion()

        # Insertion du client dans la base de données et récupération de son ID
        id_client = inserer_client(conn, client.nom, client.email)

        # Construction de la liste d'ingrédients, de sauces et de protéines sous forme de chaînes de caractères séparées par des virgules
        ingredients = ", ".join(ingredients_selectionnes)
        sauces = ", ".join(commande.sandwichs.sauces)
        proteines = ", ".join(commande.sandwichs.ingredients)

        # Insertion de la commande de sandwich avec l'ID du client associé
        inserer_commande_sandwich(conn, id_client, commande.sandwichs.nom, commande.sandwichs.proteine, sauces, proteines)

        st.success("Commande passée avec succès !")
        
        # # Envoyer un e-mail de confirmation
        # destinataire = "adresse_email_utilisateur@example.com"
        # sujet = "Confirmation de votre commande de sandwich"
        # contenu = "Votre commande a été passée avec succès !"
        # envoyer_email(destinataire, sujet, contenu)
        
        # Insérez votre logique de commande ici
        st.experimental_rerun()

# Interface administrateur pour terminer les commandes
def admin_terminer_commandes():
    st.title("Administration")

    # Authentification de l'administrateur
    if authentification():
        # Bouton pour terminer les commandes
        if st.button("Commandes terminées"):
            # Met ici le code pour marquer toutes les commandes comme terminées dans la base de données
            st.success("Toutes les commandes ont été marquées comme terminées.")
    else:
        st.error("Accès refusé.")

# Affiche l'interface utilisateur ou l'interface administrateur selon le cas
if st.sidebar.button("Mode Administrateur"):
    admin_terminer_commandes()
else:
    commande_sandwich()
# Affiche l'interface utilisateur pour commander un sandwich
commande_sandwich()

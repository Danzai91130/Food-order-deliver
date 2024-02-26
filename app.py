import hashlib
import streamlit as st
from src.classes.commande import Commande
from src.classes.client import Client
from src.classes.sandwich import Sandwich
from email_sender import send_order_email
from stockage import inserer_commande_sandwich, inserer_client
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import ast

# Convert the string to a dictionary
db_creds = ast.literal_eval(st.secrets.db_credentials['json_credentials'])

# Check if Firebase app is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(db_creds)
    firebase_admin.initialize_app(cred)

db = firestore.client()


# Initialize variables
success = False
def no_more_to_show(client):
    # Centered text
    st.write(f"<h1 style='text-align: center;'>\
             Commande passée avec succès ! 🎉 {client.nom} 🎉\
             L'équipe du pôle service de Jeevapathai te \
             remercie pour ta commande. Tu vas recevoir un email à l'adresse suivante: {client.email} </h1>", unsafe_allow_html=True)

    # Centered GIF
    col1, col2, col3 = st.columns([1, 3, 1])  # Adjust column widths as needed
    with col1:
        st.write("")  # Add space for better centering
    with col2:
        st.image("data/gifs/bien-joue.gif", use_column_width=True)
    with col3:
        st.write("")  # Add space for better centering

    # Clear session state to remove content from commande_sandwich function
    st.session_state.clear()

# Ingrédients disponibles
ingredients_disponibles = ["Salade", "Tomate", "Oignons", "Fromage"]

# Sauces disponibles
sauces_disponibles = ["Mayonnaise", "Ketchup", "Algerienne", "Samourai", "Harissa", "BBQ"]

# Protéines disponibles
proteines_disponibles = ["Jambon", "Poulet"]

placeholder = st.empty()
# Affiche l'interface utilisateur ou l'interface administrateur selon le cas

with placeholder.form("Commander un Sandwich"):
    container =  st.container(border=False)
    container.title("Commander un Sandwich")

    #Générer une clé unique pour chaque widget en utilisant une fonction de hachage
    nom_key_1 = hashlib.md5("Nom".encode()).hexdigest()
    email_key_1 = hashlib.md5("Email".encode()).hexdigest()
    nom_sandwich_key_1 = hashlib.md5("Nommme ton sandwich du turfu".encode()).hexdigest()
    ingredients_key_1 = hashlib.md5("ingredient_select".encode()).hexdigest()
    sauces_key_1 = hashlib.md5("sauces_select".encode()).hexdigest()
    proteines_key_1 = hashlib.md5("proteines_select".encode()).hexdigest()

    # Saisie du nom et de l'email
    nom = container.text_input("Nom", key=nom_key_1, value="")
    email = container.text_input("Email", key=email_key_1, value="")
    nom_sandwich = container.text_input("Nommme ton sandwich du turfu", key=nom_sandwich_key_1, value="")

    # Sélection des ingrédients
    ingredients_selectionnes = container.multiselect("Sélectionnez les ingrédients", ingredients_disponibles, key=ingredients_key_1, default=[])

    # Sélection des sauces
    sauces_selectionnees = container.multiselect("Sélectionnez les sauces", sauces_disponibles, key=sauces_key_1, default=[])

    # Sélection des protéines
    proteines_selectionnees = container.selectbox("Sélectionnez les protéines", proteines_disponibles, key=proteines_key_1, index=0)
    
    commander_button = st.form_submit_button("Commander")
    if commander_button:
        # Création de l'objet Client
        client = Client(nom, email)

        # Création de l'objet Sandwich
        sandwich = Sandwich(nom_sandwich, proteines_selectionnees, sauces_selectionnees, ingredients_selectionnes)

        # Création de l'objet Commande avec le client et le sandwich
        commande = Commande(client, sandwich)

        # Insertion du client dans la base de données et récupération de son ID
        id_client = inserer_client(db,client.nom, client.email)

        # Construction de la liste d'ingrédients, de sauces et de protéines sous forme de chaînes de caractères séparées par des virgules
        sauces = ", ".join(commande.sandwichs.sauces)
        ingredients = ", ".join(commande.sandwichs.ingredients)

        # Insertion de la commande de sandwich avec l'ID du client associé
        inserer_commande_sandwich(db,id_client, commande.sandwichs.nom, commande.sandwichs.proteine, sauces, ingredients)
        send_order_email(st.secrets.email_cred.address, st.secrets.email_cred.pwd, client, ingredients_selectionnes, sauces_selectionnees, [proteines_selectionnees])
        success = True

        placeholder.empty()
if success:
    no_more_to_show(client)

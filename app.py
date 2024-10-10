import hashlib
import random
import re
import streamlit as st
from src.classes.commande import Commande
from src.classes.client import Client
from src.classes.sandwich import Sandwich
from email_sender import send_order_email, send_slack_notification
from stockage import inserer_commande_sandwich, inserer_client
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import ast
import base64
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("data/streamlit_data/background.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://i.pinimg.com/originals/f5/b3/d5/f5b3d5f92b3e330dd3bd787c1cf91aa3.jpg");
background-size: 100%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}
[data-testid="stForm"] {{
     background: #FFA07A;
}}
[data-testid="stCheckbox"] {{
     background: #FFA07A;
}}
#commander-un-sandwich{{
  text-align: center
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
[data-testid="stFormSubmitButton"] {{
  display: flex;
  align-items: center;
  justify-content: center;
}}
[data-testid="stButton"] {{
  display: flex;
  align-items: center;
  justify-content: center;
}}
[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
# Convert the string to a dictionary
db_creds = ast.literal_eval(st.secrets.db_credentials['json_credentials'])

# Check if Firebase app is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(db_creds)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def validate_email(email):
    # Regular expression for validating an email address
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

# Initialize variables
success = False

def no_more_to_show(agree,client):

    email_message = f" Tu vas recevoir un email à l'adresse suivante: {client.email}" if agree else ""
    
    # Afficher le message complet
    st.write(f"<h1 style='text-align: center;'>\
             Commande passée avec succès ! 🎉 {client.prenom} 🎉\
             L'équipe du pôle service de Jeevapathai te remercie pour ta commande.{email_message}</h1>", 
             unsafe_allow_html=True)
    # Define the upper limit for the random number (replace 100 with your desired upper limit)
    upper_limit = 5
    # Generate a random number between 1 and the upper limit
    rdm = random.randint(1, upper_limit)
    # Centered GIF
    col1, col2, col3 = st.columns([1, 3, 1])  # Adjust column widths as needed
    with col1:
        st.write("")  # Add space for better centering
    with col2:
        st.image(f"data/gifs/gif{rdm}.gif", use_column_width=True)
    with col3:
        st.write("")  # Add space for better centering

    # Clear session state to remove content from commande_sandwich function
    st.session_state.clear()

    # Créer un bouton
    if st.button('Commander à nouveau'):
        # Rafraîchir la page lorsque le bouton est cliqué
        st.experimental_rerun()

# Ingrédients disponibles
ingredients_disponibles = ["Salade", "Tomate", "Oignons", "Fromage"]

# Sauces disponibles
sauces_disponibles = ["Mayonnaise", "Ketchup", "Algerienne", "Samourai", "Harissa", "BBQ"]

# Protéines disponibles
proteines_disponibles = ["Jambon", "Poulet"]

# Noms disponibles
noms_disponibles = ["GAUTIER","SARAVANANE","PONNOU",\
                    "RAYAPOULE","MOUTALOU","SHANMOUGAM(Simon)",\
                    "IROUDAYARAJ","JARDIN","XAVIERE","LIZY(Daniel Tonton)",\
                    "GILOT(Marc tonton)","ALLISTER(Guru tonton)",\
                    "MOBIN(Bernard tonton)","MICHEL","AROUL(Jonathan)",\
                    "ANTOINE DASS","ANTOINERADJU(Remo)","LEPRINCE(Loki)",\
                    "JEANPIERRE(Nicolas tonton)","SILENCE(Jeci tatie)"
] # a modifier

# Placeholder pour le formulaire
placeholder = st.empty()


# Générer une clé unique pour chaque widget en utilisant une fonction de hachage
prenom_key_1 = hashlib.md5("Prénom".encode()).hexdigest()
nom_key_1 = hashlib.md5("Nom".encode()).hexdigest()
email_key_1 = hashlib.md5("Email".encode()).hexdigest()
ingredients_key_1 = hashlib.md5("ingredient_select".encode()).hexdigest()
sauces_key_1 = hashlib.md5("sauces_select".encode()).hexdigest()
proteines_key_1 = hashlib.md5("proteines_select".encode()).hexdigest()
agree_key_1 = hashlib.md5("agree_checkbox".encode()).hexdigest()
commande_enfant_key_1 = hashlib.md5("commande_enfant_checkbox".encode()).hexdigest()

agree_box = st.empty()
enfant_box = st.empty()
# État de la case à cocher pour l'email
agree = agree_box.checkbox('Je veux recevoir le récap de ma commande par mail🚀',key=agree_key_1)

# État de la case à cocher pour l'email
commande_enfant = enfant_box.checkbox("C'est pour un enfant 🧒👧",key=commande_enfant_key_1)
#commande_enfant = True
# Formulaire de commande
with placeholder.form("Commander un Sandwich"):
    container = st.container()
    container.title("Commander un Sandwich")

    # Saisie du prénom
    prenom = container.text_input("Prénom", key=prenom_key_1, value="")
    nom = container.selectbox("Nom de famile", noms_disponibles, key=nom_key_1, index=0)

    # Saisie de l'email si la case à cocher est sélectionnée
    email = ""
    if agree:
        email = container.text_input("Email", key=email_key_1, value="")

    # Sélection des ingrédients
    ingredients_selectionnes = container.multiselect("Sélectionnez les ingrédients", ingredients_disponibles, key=ingredients_key_1, default=[])

    # Sélection des sauces
    sauces_selectionnees = container.multiselect("Sélectionnez les sauces", sauces_disponibles, key=sauces_key_1, default=[])

    # Sélection des protéines
    proteines_selectionnees = container.selectbox("Sélectionnez les protéines", proteines_disponibles, key=proteines_key_1, index=0)

    # Bouton pour soumettre la commande
    commander_button = st.form_submit_button("Commander")

    if commander_button:
        # Vérification si les champs obligatoires sont remplis
        if not ingredients_selectionnes or not sauces_selectionnees:
            st.warning("Veuillez sélectionner au moins un ingrédient et une sauce.")
            st.stop()
        
        if not prenom:
            st.warning("Veuillez renseigner votre nom.")
            st.stop()

        if agree and not validate_email(email):
            st.error("Veuillez rentrer une adresse mail valide svp.")
            st.stop()

        # Création de l'objet Client
        client = Client(prenom, nom, email)

        # Création de l'objet Sandwich
        sandwich = Sandwich(proteines_selectionnees, sauces_selectionnees, ingredients_selectionnes)

        # Création de l'objet Commande avec le client et le sandwich
        commande = Commande(client, sandwich)

        # Insertion du client dans la base de données et récupération de son ID
        id_client = inserer_client(db, client.prenom, client.nom, client.email)

        # Construction de la liste d'ingrédients, de sauces et de protéines sous forme de chaînes de caractères séparées par des virgules
        sauces = ", ".join(commande.sandwichs.sauces)
        ingredients = ", ".join(commande.sandwichs.ingredients)

        # Insertion de la commande de sandwich avec l'ID du client associé
        inserer_commande_sandwich(db, id_client, commande.sandwichs.proteine, sauces, ingredients,commande_enfant)

        # Envoi de l'email de commande
        if agree:
            if email!="":
                try:
                    send_order_email(st.secrets.email_cred.address, st.secrets.email_cred.pwd, client, ingredients_selectionnes, sauces_selectionnees, [proteines_selectionnees])
                except:
                    print("couldn't send email")
        else:
            send_slack_notification(st.secrets.slack_cred.webhook,f"{client.nom} {client.prenom} a passé commande!:\n Avec ces ingrédients {ingredients}, \n Avec ces sauces:{sauces},\n \n Avec ces proteines {proteines_selectionnees}")
        success = True
        placeholder.empty()
        agree_box.empty()
        enfant_box.empty()

if success:
    no_more_to_show(agree,client)

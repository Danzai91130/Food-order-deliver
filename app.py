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

if not firebase_admin._apps:
    cred = credentials.Certificate(db_creds)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

success = False

def no_more_to_show(agree, client):
    email_message = f" Tu vas recevoir un email à l'adresse suivante: {client.email}" if agree else ""
    
    st.write(f"<h1 style='text-align: center;'>\
             Commande passée avec succès ! 🎉 {client.prenom} 🎉\
             L'équipe du pôle service de Jeevapathai te remercie pour ta commande.{email_message}</h1>", 
             unsafe_allow_html=True)

    rdm = random.randint(1, 5)
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image(f"data/gifs/gif{rdm}.gif", use_column_width=True)

    st.session_state.clear()

    if st.button('Commander à nouveau'):
        st.experimental_rerun()

ingredients_disponibles = ["Salade", "Tomate", "Oignons", "Fromage"]
sauces_disponibles = ["Mayonnaise", "Ketchup", "Algerienne", "Samourai", "Harissa", "BBQ"]
proteines_disponibles = ["Jambon", "Poulet"]
noms_disponibles = [
    "GAUTIER","SARAVANANE","PONNOU","RAYAPOULE","MOUTALOU","SHANMOUGAM(Simon)",
    "IROUDAYARAJ","JARDIN","XAVIERE","LIZY(Daniel Tonton)","GILOT(Marc tonton)",
    "ALLISTER(Guru tonton)","MOBIN(Bernard tonton)","MICHEL","AROUL(Jonathan)",
    "ANTOINE DASS","ANTOINERADJU(Remo)","LEPRINCE(Loki)","JEANPIERRE(Nicolas tonton)","SILENCE(Jeci tatie)"
]

nouveaute = st.empty()

placeholder = st.empty()

prenom_key_1 = hashlib.md5("Prénom".encode()).hexdigest()
nom_key_1 = hashlib.md5("Nom".encode()).hexdigest()
email_key_1 = hashlib.md5("Email".encode()).hexdigest()
ingredients_key_1 = hashlib.md5("ingredient_select".encode()).hexdigest()
sauces_key_1 = hashlib.md5("sauces_select".encode()).hexdigest()
proteines_key_1 = hashlib.md5("proteines_select".encode()).hexdigest()
agree_key_1 = hashlib.md5("agree_checkbox".encode()).hexdigest()
commande_enfant_key_1 = hashlib.md5("commande_enfant_checkbox".encode()).hexdigest()
thon_mayo_key_1 = hashlib.md5("thon_mayo_checkbox".encode()).hexdigest()
nouveaute_key_1 = hashlib.md5("nouveaute_holder".encode()).hexdigest()

thon_box =st.empty()
agree_box = st.empty()
enfant_box = st.empty()

new=nouveaute.markdown("### 🆕 Nouveauté : le Sandwich Thon Mayo 🐟 est maintenant disponible ! Coche la case en dessous du formulaire pour le gouter!", unsafe_allow_html=True)

thon_mayo_option = thon_box.checkbox("Sandwich Thon Mayo 🐟 + Mayo", key=thon_mayo_key_1)
agree = agree_box.checkbox('Je veux recevoir le récap de ma commande par mail🚀', key=agree_key_1)
commande_enfant = enfant_box.checkbox("C'est pour un enfant 🧒👧", key=commande_enfant_key_1)


with placeholder.form("Commander un Sandwich"):
    container = st.container()
    container.title("Commander un Sandwich")

    prenom = container.text_input("Prénom", key=prenom_key_1, value="")
    nom = container.selectbox("Nom de famile", noms_disponibles, key=nom_key_1, index=0)

    email = ""
    if agree:
        email = container.text_input("Email", key=email_key_1, value="")

    if thon_mayo_option:
        proteines_selectionnees = "Thon"
        sauces_selectionnees = ["Mayonnaise"]
        ingredients_selectionnes = []
        container.info("Tu as choisi un Sandwich **Thon Mayo** 🐟 avec uniquement de la Mayonnaise. Aucun autre choix requis.")
    else:
        ingredients_selectionnes = container.multiselect("Sélectionnez les ingrédients", ingredients_disponibles, key=ingredients_key_1, default=[])
        sauces_selectionnees = container.multiselect("Sélectionnez les sauces", sauces_disponibles, key=sauces_key_1, default=[])
        proteines_selectionnees = container.selectbox("Sélectionnez les protéines", proteines_disponibles, key=proteines_key_1, index=0)

    commander_button = st.form_submit_button("Commander")

    if commander_button:
        if not prenom:
            st.warning("Veuillez renseigner votre nom.")
            st.stop()

        if agree and not validate_email(email):
            st.error("Veuillez rentrer une adresse mail valide svp.")
            st.stop()

        if not thon_mayo_option and (not ingredients_selectionnes or not sauces_selectionnees):
            st.warning("Veuillez sélectionner au moins un ingrédient et une sauce.")
            st.stop()

        client = Client(prenom, nom, email)
        sandwich = Sandwich(proteines_selectionnees, sauces_selectionnees, ingredients_selectionnes)
        commande = Commande(client, sandwich)

        id_client = inserer_client(db, client.prenom, client.nom, client.email)

        sauces = ", ".join(commande.sandwichs.sauces)
        ingredients = ", ".join(commande.sandwichs.ingredients)

        inserer_commande_sandwich(db, id_client, commande.sandwichs.proteine, sauces, ingredients, commande_enfant)

        if agree and email:
            try:
                send_order_email(st.secrets.email_cred.address, st.secrets.email_cred.pwd, client, ingredients_selectionnes, sauces_selectionnees, [proteines_selectionnees])
            except:
                print("couldn't send email")
        else:
            send_slack_notification(st.secrets.slack_cred.webhook, f"{client.nom} {client.prenom} a passé commande!:\nAvec ces ingrédients {ingredients},\nAvec ces sauces: {sauces},\nAvec cette protéine: {proteines_selectionnees}")

        success = True
        placeholder.empty()
        agree_box.empty()
        enfant_box.empty()
        thon_box.empty()
        nouveaute.empty()

if success:
    no_more_to_show(agree, client)

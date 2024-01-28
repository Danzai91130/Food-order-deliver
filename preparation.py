import streamlit as st
import os

# Importe les fonctions de gestion des commandes que tu as déjà écrites
from src.classes.commande import recuperer_details_commande, marquer_commande_preparee

# Récupère la première commande non préparée depuis la base de données
commande = recuperer_details_commande(non_prepares_seulement=True)

# Si une commande a été trouvée, affiche ses détails
if commande:
    st.title("Préparation de Commandes de Sandwichs")

    # Affiche le titre de la commande
    st.header("Détails de la commande :")
    st.write(f"ID de la commande : {commande['id']}")
    st.write(f"Nom du client : {commande['nom_client']}")
    st.write(f"Email du client : {commande['email_client']}")
    
    # Affiche les ingrédients à gauche
    st.subheader("Ingrédients :")
    for ingredient in commande.ingredients:
        # Charge l'image correspondante depuis le dossier "data"
        image_path = os.path.join("data/streamlit_data", f"{ingredient}.jpg")
        st.image(image_path, caption=ingredient, width=100)

    # Affiche les sauces au milieu
    st.subheader("Sauces :")
    for sauce in commande.sauces:
        # Charge l'image correspondante depuis le dossier "data"
        image_path = os.path.join("data/streamlit_data", f"{sauce}.jpg")
        st.image(image_path, caption=sauce, width=100)

    # Affiche les protéines à droite
    st.subheader("Protéines :")
    for proteine in commande.proteines:
        # Charge l'image correspondante depuis le dossier "data"
        image_path = os.path.join("data/streamlit_data", f"{proteine}.jpg")
        st.image(image_path, caption=proteine, width=100)

    # Bouton pour passer à la commande suivante
    if st.button("Commande suivante"):
        # Marque la commande actuelle comme préparée dans la base de données
        marquer_commande_preparee(commande.id)
else:
    st.write("Aucune commande non préparée trouvée.")

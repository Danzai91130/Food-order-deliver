import streamlit as st
import os
from PIL import Image  # Import PIL for image resizing
from stockage import db, marquer_commande_preparee
from commandes import recuperer_details_commande

# Function to resize images
def resize_image(image_path, width=100, height=100):
    img = Image.open(image_path)
    img = img.resize((width, height), Image.ANTIALIAS)
    return img

# @st.cache(allow_output_mutation=True)
# def recuperer_details_commande_cached(db, non_prepares_seulement=False):
#     return recuperer_details_commande(db, non_prepares_seulement)

# @st.cache(allow_output_mutation=True)
# def marquer_commande_preparee_cached(db, id_commande):
#     return marquer_commande_preparee(db, id_commande)

st.set_page_config(layout="wide")

# Récupère la première commande non préparée depuis la base de données
commande = recuperer_details_commande(db, non_prepares_seulement=True)

# Si une commande a été trouvée, affiche ses détails
if commande:
    st.title("Préparation de Commandes de Sandwichs")

    # Affiche le titre de la commande
    st.header("Détails de la commande :")
    st.write(f"ID de la commande : {commande['id']}")
    st.write(f"Nom du client : {commande['nom_client']}")
    st.write(f"Email du client : {commande['email_client']}")
    print(commande)
    print(type(commande['ingredients']))
    col1, col2, col3 = st.columns(3)

    commande_ingredients_str = commande['ingredients']
    commande_ingredients = [item.strip() for item in commande_ingredients_str.split(',')]

    commande_sauces_str = commande['sauces']
    commande_sauces = [item.strip() for item in commande_sauces_str.split(',')]

    commande_proteines_str = commande['proteine']
    commande_proteines = [item.strip() for item in commande_proteines_str.split(',')]

    with col1:
        st.subheader("Ingrédients :")
        for ingredient in commande_ingredients:
            image_path = os.path.join("data/ingredients", f"{ingredient.lower()}.jpeg")
            resized_img = resize_image(image_path)
            st.image(resized_img, width=100, caption=ingredient)

    with col2:
        st.subheader("Sauces :")
        for sauce in commande_sauces:
            image_path = os.path.join("data/sauces", f"{sauce.lower()}.jpeg")
            resized_img = resize_image(image_path)
            st.image(resized_img, width=100, caption=sauce)

    with col3:
        st.subheader("Protéines :")
        for proteine in commande_proteines:
            image_path = os.path.join("data/proteines", f"{proteine.lower()}.jpeg")
            resized_img = resize_image(image_path)
            st.image(resized_img, width=100, caption=proteine)

    # Bouton pour passer à la commande suivante
    if st.button("Commande suivante"):
        # Marque la commande actuelle comme préparée dans la base de données
        marquer_commande_preparee(db, commande["id"])
else:
    # Centered text
    st.write("<h1 style='text-align: center;'>Aucune commande non préparée trouvée.</h1>", unsafe_allow_html=True)

    # Centered GIF
    col1, col2, col3 = st.columns([1, 3, 1])  # Adjust column widths as needed
    with col1:
        st.write("")  # Add space for better centering
    with col2:
        st.image("data/gifs/bien-joue.gif", use_column_width=True)
    with col3:
        st.write("")  # Add space for better centering


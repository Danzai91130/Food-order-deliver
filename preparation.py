import streamlit as st
import os
import ast
from PIL import Image
from analytics import *
from stockage import marquer_commande_preparee, set_all_preparee_false, set_completion_time
from commandes import recuperer_details_commande
import firebase_admin
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import datetime
from collections import Counter, defaultdict
from firebase_admin import credentials
from firebase_admin import firestore

# Function to get image paths for items
def get_image_paths(category):
    image_paths = {}
    data_folder = f"data/{category}"
    for item in os.listdir(data_folder):
        if item.endswith(".jpeg"):
            item_name = os.path.splitext(item)[0]
            image_paths[item_name] = os.path.join(data_folder, item)
    return image_paths

# Convert the string to a dictionary
db_creds = ast.literal_eval(st.secrets.db_credentials['json_credentials'])

# Check if Firebase app is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(db_creds)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Function to resize images
def resize_image(image_path, width=100, height=100):
    img = Image.open(image_path)
    img = img.resize((width, height), Image.ANTIALIAS)
    return img

st.set_page_config(layout="wide")

# Main page content
def main_page():
    # Récupère la première commande non préparée depuis la base de données
    commande = recuperer_details_commande(db, non_prepares_seulement=True)


    # Si une commande a été trouvée, affiche ses détails
    if commande:
        # Initialization
        if 'key' not in st.session_state:
            st.session_state['order-id'] = commande['id']
        st.title("Préparation de Commandes de Sandwichs")

        # Affiche le titre de la commande
        st.header("Détails de la commande :")
        st.write(f"ID de la commande : {commande['id']}")
        st.write(f"Nom du client : {commande['nom_client']}")
        st.write(f"Email du client : {commande['email_client']}")
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
        if st.button("Commande suivante",on_click=set_completion_time(db,st.session_state['order-id'])):
            # # Set completion time for the current order
            # set_completion_time(db, commande['id'])
            # Marque la commande actuelle comme préparée dans la base de données
            marquer_commande_preparee(db, commande["id"])
            # Bouton pour passer à la commande suivante
        if st.button("NON preparer tous"):
            # Marque la commande actuelle comme préparée dans la base de données
            set_all_preparee_false(db)
    else:
        # Centered text
        st.write("<h1 style='text-align: center;'>Aucune commande non préparée trouvée.</h1>", unsafe_allow_html=True)
        if st.button("NON preparer tous"):
            # Marque la commande actuelle comme préparée dans la base de données
            set_all_preparee_false(db)
        # Centered GIF
        col1, col2, col3 = st.columns([1, 3, 1])  # Adjust column widths as needed
        with col1:
            st.write("")  # Add space for better centering
        with col2:
            st.image("data/gifs/bien-joue.gif", use_column_width=True)
        with col3:
            st.write("")  # Add space for better centering

# Analytics page content
def analytics_page():
    # Retrieve all orders
    orders = get_all_orders(db)

    # Analyze orders
    most_used_ingredients, most_used_sauces, most_used_proteines, ingredient_count, sauces_count, protein_count = analyze_orders(orders)
    avg_ingredients_per_order, avg_sauces_per_order, avg_proteines_per_order = calculate_average_order_size(orders)
    most_common_ingredients, most_common_sauces, most_common_proteines = identify_most_common_combinations(orders)
    orders_per_day = analyze_order_trends_over_time(orders)
    customer_insights = analyze_customer_insights(orders)
    avg_preparation_time = calculate_average_preparation_time(orders)

    # Display Analytics
    st.title("Analytics")

    # Most Used Ingredients
    st.subheader("Most Used Ingredients:")
    for ingredient, count in most_used_ingredients:
        st.write(f"{ingredient}: {count} times")

    # Most Used Sauces
    st.subheader("Most Used Sauces:")
    for sauce, count in most_used_sauces:
        st.write(f"{sauce}: {count} times")

    # Most Used Proteines
    st.subheader("Most Used Proteines:")
    for proteine, count in most_used_proteines:
        st.write(f"{proteine}: {count} times")

    # Average Order Size
    st.subheader("Average Order Size:")
    st.write(f"Avg. Ingredients per Order: {avg_ingredients_per_order}")
    st.write(f"Avg. Sauces per Order: {avg_sauces_per_order}")
    st.write(f"Avg. Proteines per Order: {avg_proteines_per_order}")

    # Most Common Combinations
    st.subheader("Most Common Combinations:")

    st.write("Most Common Ingredients:")
    if most_common_ingredients:
        podium_ingredients = most_common_ingredients[:3]  # Get the top 3 most common ingredients
        podium_df = pd.DataFrame(podium_ingredients, columns=['Ingredient', 'Count'])
        st.write(podium_df)

        # Create a podium-like bar chart
        fig_ingredients = go.Figure()
        for i, (ingredient, count) in enumerate(podium_ingredients):
            fig_ingredients.add_trace(go.Bar(
                x=[ingredient],
                y=[count],
                name=ingredient,
                marker=dict(color=f'rgba(0, 0, 255, {1 - 0.1 * i})'),  # Decreasing opacity for higher ranks
            ))
        fig_ingredients.update_layout(title='Most Common Ingredients',
                                      xaxis_title='Ingredient',
                                      yaxis_title='Count',
                                      barmode='group')
        st.plotly_chart(fig_ingredients, use_container_width=True)

    st.write("Most Common Sauces:")
    if most_common_sauces:
        podium_sauces = most_common_sauces[:3]  # Get the top 3 most common sauces
        podium_df = pd.DataFrame(podium_sauces, columns=['Sauce', 'Count'])
        st.write(podium_df)

        # Create a podium-like bar chart
        fig_sauces = go.Figure()
        for i, (sauce, count) in enumerate(podium_sauces):
            fig_sauces.add_trace(go.Bar(
                x=[sauce],
                y=[count],
                name=sauce,
                marker=dict(color=f'rgba(0, 0, 255, {1 - 0.1 * i})'),  # Decreasing opacity for higher ranks
            ))
        fig_sauces.update_layout(title='Most Common Sauces',
                                  xaxis_title='Sauce',
                                  yaxis_title='Count',
                                  barmode='group')
        st.plotly_chart(fig_sauces, use_container_width=True)

    st.write("Most Common Proteins:")
    if most_common_proteines:
        podium_proteines = most_common_proteines[:3]  # Get the top 3 most common proteins
        podium_df = pd.DataFrame(podium_proteines, columns=['Protein', 'Count'])
        st.write(podium_df)

        # Create a podium-like bar chart
        fig_proteines = go.Figure()
        for i, (proteine, count) in enumerate(podium_proteines):
            fig_proteines.add_trace(go.Bar(
                x=[proteine],
                y=[count],
                name=proteine,
                marker=dict(color=f'rgba(0, 0, 255, {1 - 0.1 * i})'),  # Decreasing opacity for higher ranks
            ))
        fig_proteines.update_layout(title='Most Common Proteins',
                                     xaxis_title='Protein',
                                     yaxis_title='Count',
                                     barmode='group')
        st.plotly_chart(fig_proteines, use_container_width=True)

    # Order Trends Over Time
    st.subheader("Order Trends Over Time:")
    orders_per_day_df = pd.DataFrame.from_dict(orders_per_day, orient='index', columns=['Orders'])
    orders_per_day_df.index.name = 'Hour'
    fig_orders_per_day = px.line(orders_per_day_df, x=orders_per_day_df.index, y='Orders', title='Orders per Hour')
    st.plotly_chart(fig_orders_per_day, use_container_width=True)

    # Customer Insights
    st.subheader("Customer Insights:")
    customer_insights_df = pd.DataFrame(customer_insights, columns=['Customer ID', 'Order Count'])
    st.write(customer_insights_df)

    # Average Preparation Time
    st.subheader("Average Preparation Time:")
    st.write(f"{avg_preparation_time} seconds")

# Main function to display the "Courses" page
def courses_page():
    st.markdown("<h1 style='text-align: center; color: yellow;'>Courses</h1>", unsafe_allow_html=True)

    # Retrieve all orders from Firestore
    orders = get_all_orders(db)

    # Aggregate counts of ingredients, proteins, and sauces
    most_used_ingredients, most_used_sauces, most_used_proteines, ingredient_counts, proteines_counts, sauces_counts = analyze_orders(orders)
    # Get image paths for ingredients, proteins, and sauces
    ingredient_image_paths = get_image_paths("ingredients")
    proteines_image_paths = get_image_paths("proteines")
    sauces_image_paths = get_image_paths("sauces")
    col1, col2, col3 = st.columns(3)
    with col1:
        # Display ingredient counts
        st.subheader("Ingredients")
        for ingredient, count in ingredient_counts.items():
            caption = f"{ingredient}: {count}"
            if ingredient.lower() in ingredient_image_paths.keys():
                image = Image.open(ingredient_image_paths[ingredient.lower()])
                st.image(image, caption=caption, width=100)

    with col2:
        # Display ingredient counts
        st.subheader("Proteines")
        for proteine, count in proteines_counts.items():
            caption = f"{proteine}: {count}"
            if proteine.lower() in proteines_image_paths.keys():
                image = Image.open(proteines_image_paths[proteine.lower()])
                st.image(image, caption=caption, width=100)

    with col3:
        # Display ingredient counts
        st.subheader("Sauces")
        for sauce, count in sauces_counts.items():
            caption = f"{sauce}: {count}"
            if sauce.lower() in sauces_image_paths.keys():
                image = Image.open(sauces_image_paths[sauce.lower()])
                st.image(image, caption=caption, width=100)

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Main", "Analytics","Courses"])

if page == "Main":
    main_page()
elif page == "Analytics":
    analytics_page()
elif page == "Courses":
    courses_page()
from email.mime.image import MIMEImage
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import requests

from src.classes.client import Client

def send_slack_notification(webhook_url, message):
    payload = {
        "text": message
    }
    response = requests.post(webhook_url, json=payload)

    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print("Failed to send notification. Status code:", response.status_code)

sauces_equivalents = {
"Samourai": "🥷",
"Ketchup" : "🥫🍅",
"Harissa" : "🌶🥵",
"Mayonnaise" : "〽️",
"BBQ" : "🍖♨️🔥🥩🥓🍳",
"Algerienne" : "🇩🇿"
}


ingredients_equivalents = {
"Salade": "🥬",
"Tomate" : "🍅",
"Oignons" : "🧅",
"Fromage" : "🧀",
}

proteines_equivalents = {
    "Jambon" :"🐷",
    "Poulet" :"🐔"
}
def send_order_email(sender_email: str, sender_pwd: str, client: Client, ingredients: list, sauces: list, proteines: list):
    # Mapper les ingrédients, sauces et protéines avec les emojis correspondants
    emojis = {**ingredients_equivalents, **sauces_equivalents, **proteines_equivalents}

    # Générer une description humoristique du sandwich commandé
    description = ""
    
    # Gérer les ingrédients
    if ingredients:
        description += "🍱 On commence par ajouter une bonne dose d'ingrédients 'zélément choisis'.\n"
        for ingredient in ingredients:
            if ingredient == "Salade":
                description += "    • 🥬 La salade, pour une touche de fraîcheur et de croquant !\n"
            elif ingredient == "Tomate":
                description += "    • 🍅 Les tomates, juteuses et colorées, pour égayer votre sandwich !\n"
            elif ingredient == "Oignons":
                description += "    • 🧅 Les oignons, pour une petite touche de piquant et de saveur !\n"
            elif ingredient == "Fromage":
                description += "    • 🧀 Le fromage, fondant à souhait, pour rendre votre sandwich irrésistible !\n"
            else:
                description += f"{emojis.get(ingredient, ingredient)} "
        description += "\n"
    
    # Gérer les sauces
    if sauces:
        description += "🥫 Ensuite, on y ajoute une sauce qui va faire danser vos papilles !\n"
        for sauce in sauces:
            if sauce == "Ketchup":
                description += "    • 🥫🍅 Ah, le classique ketchup ! Parfait pour une touche de douceur.\n"
            elif sauce == "Harissa":
                description += "    • 🌶️🥵 Oh là là, la harissa ! Attention, ça va piquer ! 😜\n"
            elif sauce == "Mayonnaise":
                description += "    • 〽️ La mayonnaise, une touche de crémeux pour un sandwich irrésistible !\n"
            elif sauce == "BBQ":
                description += "    • 🍖♨️🔥🥩🥓🍳 La sauce BBQ, un festival de saveurs fumées et épicées ! Yeehaw ! 🤠\n"
            elif sauce == "Algerienne":
                description += "    • 🇩🇿 L'algérienne, une explosion de saveurs méditerranéennes ! Magnifique ! 🌊🌴\n"
            elif sauce == "Samourai":
                description += "    • 🥷 La sauce Samouraï, tout comme un ninja, elle passe partout et vous surprendra avec son coup percutant ! 💥🥋\n"

            else:
                description += f"{emojis.get(sauce, sauce)} "
        description += "\n"
    
    # Gérer les protéines
    if proteines:
        description += "🥩 Et pour finir en beauté, on garnit le tout avec une délicieuse protéine !\n"
        for proteine in proteines:
            if proteine == "Jambon":
                description += "    • 🐷 Le jambon, tendre et savoureux, pour une touche de gourmandise !\n"
            elif proteine == "Poulet":
                description += "    • 🐔 Le poulet, grillé à la perfection, pour un sandwich léger et délicieux !\n"
            else:
                description += f"{emojis.get(proteine, proteine)} "
        description += "\n"
    
    # Ajouter une touche finale joyeuse
    description += "🎉 Voilà, votre sandwich unique et délicieux est prêt à être dégusté ! Bon appétit ! 🎉"

    # Paramètres de l'e-mail
    receiver_email = client.email
    subject = f"🥪 {client.nom}, votre sandwich Jeevapathai est en route ! 😎"
    
    # Email body
    corps_email = f"""\
    <html>
    <body>
        <p>Cher {client.nom},</p>
        <p>Nous sommes ravis de vous annoncer que votre commande de sandwich est en cours de préparation avec soin et amour ! 🥪❤️</p>
        <p>Voici une description amusante de votre sandwich :<br>{description}</p>
        <p>Notre équipe chez Jeevapathai a hâte que vous savouriez chaque bouchée ! 😋</p>
        <p>Votre satisfaction est notre priorité absolue, et nous sommes toujours là pour nous assurer que vous avez une expérience délicieuse avec nous.</p>
        <p>Merci d'avoir choisi Jeevapathai pour vos envies de sandwich ! 🙏</p>
        <p>Cordialement,<br>L'équipe Pole service Jeevapathai</p>
        <img src="cid:bien_joue_gif" width="100" height="70"> <!-- Adjust width and height as needed -->
    </body>
    </html>
    """

    # Création du message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Ajout du corps du message
    message.attach(MIMEText(corps_email, "html"))
    # Open the image file
    with open('data/gifs/bien-joue.gif', 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID', '<bien_joue_gif>')
        message.attach(img)

    try:
        # Connexion au serveur SMTP
        with smtplib.SMTP("smtp-mail.outlook.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_pwd)
            
            # Envoi de l'e-mail
            server.send_message(message)
            send_slack_notification(st.secrets.slack_cred.webhook,f"{client.nom} {client.prenom} a passé commande!:\n Avec ces ingrédients {ingredients}, \n Avec ces sauces:{sauces},\n \n Avec ces proteines {proteines}")
        print("E-mail envoyé avec succès !")
    except smtplib.SMTPDataError as e:
        send_slack_notification(st.secrets.slack_cred.webhook,f"Erreur lors de l'envoi de l'e-mail:{e}, pour le client {client.nom} au mail {client.email})")
        print("Erreur lors de l'envoi de l'e-mail:", e)
        print("L'erreur a été ignorée.")


    print("E-mail envoyé avec succès !")

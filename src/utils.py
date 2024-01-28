import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def envoyer_email(destinataire, sujet, contenu):
    # Définir les détails du serveur SMTP
    smtp_server = "smtp.example.com"
    port = 587  # Port du serveur SMTP
    expediteur = "votre_adresse_email@example.com"
    mot_de_passe = "votre_mot_de_passe"

    # Créer un objet MIMEMultipart pour l'e-mail
    message = MIMEMultipart()
    message["From"] = expediteur
    message["To"] = destinataire
    message["Subject"] = sujet

    # Ajouter le contenu de l'e-mail
    message.attach(MIMEText(contenu, "plain"))

    # Se connecter au serveur SMTP
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(expediteur, mot_de_passe)

    # Envoyer l'e-mail
    server.sendmail(expediteur, destinataire, message.as_string())

    # Fermer la connexion SMTP
    server.quit()

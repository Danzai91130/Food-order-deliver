from stockage import *

# Test de la fonction de création de connexion
def test_creer_connexion():
    conn = creer_connexion()
    assert conn is not None
    conn.close()

# Test de la fonction de création de tables
def test_creer_tables():
    conn = creer_connexion()
    creer_tables(conn)
    # Vérifie si les tables ont été créées en vérifiant l'existence des tables
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clients'")
    assert cursor.fetchone() is not None
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='commandes_sandwichs'")
    assert cursor.fetchone() is not None
    conn.close()

# Test de la fonction d'insertion de client
def test_inserer_client():
    conn = creer_connexion()
    inserer_client(conn, "John Doe", "john@example.com")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE nom='John Doe'")
    assert cursor.fetchone() is not None
    conn.close()

# Test de la fonction d'insertion de commande de sandwich
def test_inserer_commande_sandwich():
    conn = creer_connexion()
    inserer_commande_sandwich(conn, 1, "Jambon-Fromage", "Jambon", "Mayonnaise", "Salade, Tomate")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM commandes_sandwichs WHERE nom_sandwich='Jambon-Fromage'")
    assert cursor.fetchone() is not None
    conn.close()

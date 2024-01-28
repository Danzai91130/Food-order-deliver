import sqlite3

def creer_connexion():
    """Crée et retourne une connexion à la base de données."""
    return sqlite3.connect('data/commands.db')

def creer_tables(conn):
    """Crée les tables de la base de données si elles n'existent pas déjà."""
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
                        id INTEGER PRIMARY KEY,
                        nom TEXT,
                        email TEXT
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS commandes_sandwichs (
                        id INTEGER PRIMARY KEY,
                        id_client INTEGER,
                        nom_sandwich TEXT,
                        proteine TEXT,
                        sauces TEXT,
                        ingredients TEXT,
                        preparee INTEGER DEFAULT 0,
                        FOREIGN KEY (id_client) REFERENCES clients (id)
                    )''')
    conn.commit()

def inserer_client(conn, nom, email):
    """Insère un client dans la base de données."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clients (nom, email) VALUES (?, ?)", (nom, email))
    conn.commit()
    # Récupère l'ID du client nouvellement inséré
    id_client = cursor.lastrowid
    return id_client

def inserer_commande_sandwich(conn, id_client, nom_sandwich, proteine, sauces, ingredients):
    """Insère une commande de sandwich dans la base de données."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO commandes_sandwichs (id_client, nom_sandwich, proteine, sauces, ingredients) VALUES (?, ?, ?, ?, ?)",
                   (id_client, nom_sandwich, proteine, sauces, ingredients))
    conn.commit()

def marquer_commande_preparee(conn, id_commande):
    """Marque une commande comme préparée dans la base de données."""

    cursor = conn.cursor()
    cursor.execute("UPDATE commandes_sandwichs SET preparee = 1 WHERE id = ?", (id_commande,))
    conn.commit()
    conn.close()

# Code de test pour vérifier le bon fonctionnement des fonctions
if __name__ == "__main__":
    conn = creer_connexion()
    creer_tables(conn)
    
    # Insertion d'un client
    inserer_client(conn, "John Doe", "john@example.com")

    # Insertion d'une commande de sandwich
    inserer_commande_sandwich(conn, 1, "Jambon-Fromage", "Jambon", "Mayonnaise", "Salade, Tomate")
    
    conn.close()

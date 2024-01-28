# src/classes/commande.py

class Commande:
    def __init__(self, client, sandwichs):
        self.client = client
        self.sandwichs = sandwichs

    def afficher_details(self):
        print("Commande de {} :".format(self.client.nom))
        for i, sandwich in enumerate(self.sandwichs, 1):
            print("  {}. {}".format(i, sandwich))

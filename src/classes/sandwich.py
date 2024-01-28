# src/classes/sandwich.py

class Sandwich:
    def __init__(self, nom, proteine, sauces=None, ingredients=None):
        self.nom = nom
        self.proteine = proteine
        self.sauces = sauces if sauces is not None else []
        self.ingredients = ingredients if ingredients is not None else []

    def ajouter_sauce(self, sauce):
        self.sauces.append(sauce)

    def ajouter_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def __str__(self):
        return self.nom

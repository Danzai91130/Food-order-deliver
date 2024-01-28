# test_sandwich.py
from src.classes.sandwich import Sandwich

def test_ajout_sauces_et_ingredients():
    # Création d'un sandwich
    sandwich = Sandwich("Poulet BBQ", "Poulet")

    # Ajout de sauces
    sandwich.ajouter_sauce("BBQ")
    sandwich.ajouter_sauce("Mayonnaise")

    # Ajout d'ingrédients
    sandwich.ajouter_ingredient("Salade")
    sandwich.ajouter_ingredient("Tomate")

    # Vérification des sauces et des ingrédients ajoutés
    assert sandwich.sauces == ["BBQ", "Mayonnaise"]
    assert sandwich.ingredients == ["Salade", "Tomate"]

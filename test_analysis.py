#import des bibliothèques nécessaires
import pytest
import pandas as pd
from functions.data_cleaner import clean_whitespace, handle_missing_values, fix_formats, remove_duplicates
from functions.analyzer import analyze_by_rating, get_global_statistics

# test_analysis.py

@pytest.fixture

#fonction qui fournit une liste de livres BRUTES (pour les tests de nettoyage)
def raw_books_list():
    df_raw = pd.DataFrame([
        # Livre 1 (Propre et Doublon)
        {'title': '  Book 1 ', 'price': '£10.50 ', 'rating': 'Three', 'available': 'In stock (2)'},
        # Livre 2 (OK)
        {'title': 'Book 2', 'price': '5.00', 'rating': 'One', 'available': 'Out of stock'},
        # Livre 3 (Valeurs manquantes/invalides)
        {'title': 'Book 3', 'price': None, 'rating': '', 'available': 1},
        # Livre 4 (Doublon de Livre 1)
        {'title': 'Book 1', 'price': '£10.50 ', 'rating': 'Three', 'available': 'In stock (2)'},
        # Livre 5 (Format spécial et Rating invalide)
        {'title': 'Book 5', 'price': '25.99$', 'rating': 'Six', 'available': '25'}, 
    ])
    return df_raw.to_dict('records')

@pytest.fixture

#fonction qui fournit une liste de livres PROPRES (pour les tests d'analyse)
def clean_books_list():
    return [
        {'title': 'High Price 5-Star', 'price': 50.00, 'rating': 5, 'available': 10},
        {'title': 'Low Price 5-Star', 'price': 10.00, 'rating': 5, 'available': 5},
        {'title': 'Avg Price 3-Star', 'price': 20.00, 'rating': 3, 'available': 20},
        {'title': 'Zero Rating/Error', 'price': 5.00, 'rating': 0, 'available': 1},
    ]

#test data_cleaner.py

#fonction de test pour clean_data.py
def test_clean_whitespace(raw_books_list):
    books_cleaned = clean_whitespace(raw_books_list)
    # On vérifie la première entrée
    assert books_cleaned[0]['title'] == 'Book 1'
    assert books_cleaned[0]['price'] == '£10.50'

#fonction de test pour handle_missing_values.py
def test_handle_missing_values(raw_books_list):
    books_handled = handle_missing_values(raw_books_list)
    
    # Vérification du Livre 3 (index 2: price=None, rating='')
    assert books_handled[2]['price'] == 0.0
    assert books_handled[2]['rating'] == 0
    assert books_handled[2]['available'] == 1

#fonction de test pour fix_formats.py
def test_fix_formats(raw_books_list):
    books_temp = handle_missing_values(raw_books_list)
    books_fixed = fix_formats(books_temp)
    
    assert books_fixed[0]['price'] == 10.50
    assert books_fixed[0]['rating'] == 3
    assert books_fixed[0]['available'] == 2
    
    assert books_fixed[4]['price'] == 25.99
    assert books_fixed[4]['rating'] == 0
    assert books_fixed[4]['available'] == 25

#fonction de test pour remove_duplicates.py
def test_remove_duplicates(raw_books_list):
    books_unique = remove_duplicates(raw_books_list)
    assert len(books_unique) == 4

#fonction de test pour analyze_by_rating.py
def test_analyze_by_rating(clean_books_list):
    results = analyze_by_rating(clean_books_list)
    
    rating_5 = results[5]
    
    # Livre Count : 2
    assert rating_5['Book_Count'] == 2
    # Prix Moyen : (50.00 + 10.00) / 2 = 30.00
    assert rating_5['Average_Price'] == 30.00
    # Valeur Totale : (50*10) + (10*5) = 550.00
    assert rating_5['Value'] == 550.00

#fonction de test pour get_global_statistics.py
def test_get_global_statistics(clean_books_list):
    stats = get_global_statistics(clean_books_list)
    
    assert stats['total_books'] == 4
    assert stats['average_price'] == 21.25
    assert stats['max_price'] == 50.00
    assert stats['total_value'] == 955.00
    
#fonction de test pour get_global_statistics avec liste vide
def test_global_statistics_empty_list():
    stats = get_global_statistics([])
    assert stats['total_books'] == 0
    assert stats['average_price'] == 0.0
#importation des modules nécessaires
import re
import pandas as pd

#fonction pour nettoyer les espaces blancs dans les données des livres
def clean_whitespace(books):
    if books is None:
        return []

    # retrait des espaces inutiles au début et fin des textes
    cleaned_books = []
    
    for book in books:
        try:
            # Utilisation d'une compréhension de dictionnaire pour appliquer strip() à toutes les valeurs de type str
            cleaned_book = {
                k: (v.strip() if isinstance(v, str) else v) 
                for k, v in book.items()
            }
            cleaned_books.append(cleaned_book)
        except Exception as e:
            print(f"Error during the cleaning : {e}")
            cleaned_books.append(book)
    
    return cleaned_books


#fonction pour gérer les valeurs manquantes dans les données des livres
def handle_missing_values(books):
    if books is None:
        return []

    #Gestion des valeurs manquantes avec protection d'erreurs
    cleaned_books = []
    
    for book in books:
        try:
            
            if 'price' not in book or book.get('price') is None:
                book['price'] = 0.0
            
            # Remplacer rating manquant par 0
            if not book.get('rating'):
                book['rating'] = 0
            
            # Remplacer disponibilité manquante par 0
            if 'available' not in book or book['available'] is None or book['available'] == '':
                book['available'] = 0
            
            cleaned_books.append(book)
            
        except KeyError as e:
            print(f"Key Error : {e}")
            cleaned_books.append(book)

        except Exception as e:
            print(f"unmissed values : {e}")
            cleaned_books.append(book)
    
    return cleaned_books


#fonction pour corriger les formats des données des livres
def fix_formats(books):
    if books is None:
        return []
    
    # Mapping pour les ratings en texte
    rating_map = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    
    
    for book in books:
        # nettoyage du prix
        try:
            price = book.get('price', 0)
            
            if isinstance(price, str):
                # retrait des £, €, $, espaces
                price = price.replace('£', '').replace('€', '').replace('$', '').strip()
                # formatage décimal avec virgule en point
                price = price.replace(',', '.')
                # Conversion en float
                book['price'] = float(price)
            elif not isinstance(price, (int, float)):
                book['price'] = 0.0
                
        except (ValueError, TypeError, AttributeError) as e:
            print(f"Error during the conversion of price '{book.get('price')}' : {e}")
            book['price'] = 0.0
        
        # nettoyage du rating 
        try:
            rating = book.get('rating', 0)
            
            if isinstance(rating, str):
                # retrait de ' stars' 
                cleaned_rating = rating.lower().replace(' stars', '').strip()
            
                if cleaned_rating.capitalize() in rating_map:
                    book['rating'] = rating_map[cleaned_rating.capitalize()]
                else:
                    book['rating'] = int(cleaned_rating)
            
            elif not isinstance(rating, int):
                book['rating'] = 0
                
        except (ValueError, TypeError) as e:
            print(f"Error during the conversion of rating '{book.get('rating')}' : {e}")
            book['rating'] = 0
        
        # nettoyage de la disponibilité
        try:
            available = book.get('available', 0)
            
            if isinstance(available, str):
                if 'In stock' in available:
                    # extraction du nombre entre parenthèses
                    match = re.search(r'\((\d+)', available)
                    if match:
                        book['available'] = int(match.group(1))
                    else:
                        book['available'] = 0
                elif 'Out of stock' in available:
                    book['available'] = 0
                else:
                    # essai de conversion directe
                    book['available'] = int(available)
            elif not isinstance(available, int):
                # Sécurité si le type n'est pas un int
                book['available'] = 0
                
        except (ValueError, TypeError, AttributeError) as e:
            print(f"error during the conversion '{book.get('available')}' : {e}")
            book['available'] = 0

    return books


#fonction pour supprimer les livres en double
def remove_duplicates(books):
    if books is None:
        return []
        
    #Suppression des livres en double basés sur le titre et le prix
    seen = set()
    unique_books = []
    
    for book in books:
        try:

            title_raw = book.get('title', '')
            title = title_raw.strip() if isinstance(title_raw, str) else title_raw
            
            price_raw = book.get('price', 0)
            price = price_raw.strip() if isinstance(price_raw, str) else price_raw
            
            key = (title, price)
            
            if key not in seen:
                seen.add(key)
                unique_books.append(book)
                
        except (TypeError, AttributeError) as e:
            print(f"Error : {e}")
            # On garde le livre quand même si la création de clé échoue
            unique_books.append(book)
    
    return unique_books


#fonction principale de nettoyage des données des livres
def clean_data(books):

    try:
        if not books:
            print("Books list is empty, nothing to clean.")
            return []
        
        books_initial = len(books)
        print(f"\n START CLEANING - {books_initial} books")
        
        # Étape 1 : nettoyer les espaces
        books = clean_whitespace(books)
        
        # Étape 2 : gerer les valeurs manquantes
        books = handle_missing_values(books)
        
        # Étape 3 : corriger les formats
        books = fix_formats(books)
        
        # Étape 4 : enlever les doublons
        books = remove_duplicates(books)
        
        # Étape finale : transformation en DataFrame pandas pour vérification
        df_books = pd.DataFrame(books)
        return df_books
        
    except Exception as e:
        print(f"\nError during the cleaning : {e}")
        return []
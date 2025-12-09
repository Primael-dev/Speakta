#importat des bibliothèques nécessaires
from data_cleaner import clean_data
from manage import load_books
import pandas as pd
import io 
import sys
from contextlib import redirect_stdout
from pathlib import Path
import traceback


#fonction pour analyser les livres par rating
def analyze_by_rating(books):
    
    stats_by_rating = {}
    
    for rating in range(0, 6):  
        stats_by_rating[rating] = {
            'books': [],           
            'total_price': 0.0,    
            'total_stock': 0,      
            'total_value': 0.0,    
            'book_count': 0        
        }
    
    # parcours de tous les livres
    for book in books:
        try:

            rating = int(book.get('rating', 0))
            price = book.get('price', 0.0)
            stock = book.get('available', 0)
            
            # Gestion des ratings hors-limites
            if rating < 0 or rating > 5:
                rating = 0
            
            # Ajout du livre à la catégorie correspondante
            stats_by_rating[rating]['books'].append(book)
            stats_by_rating[rating]['total_price'] += price
            stats_by_rating[rating]['total_stock'] += stock
            stats_by_rating[rating]['total_value'] += (price * stock)
            stats_by_rating[rating]['book_count'] += 1
            
        except Exception as e:
            stats_by_rating[0]['book_count'] += 1
            continue 
    
    # Calcul des moyennes
    results = {}
    for rating, stats in stats_by_rating.items():
        book_count = stats['book_count']
        
        if book_count > 0:
            avg_price = stats['total_price'] / book_count
        else:
            avg_price = 0.0
        
        results[rating] = {
            'Rating': rating,
            'Average_Price': round(avg_price, 2),
            'Total_Stock': stats['total_stock'],
            'Value': round(stats['total_value'], 2),
            'Book_Count': book_count
        }
    
    return results

#fonction pour afficher les résultats de l'analyse sous forme de tableau
def print_analysis_table(results):
    
    print("\n" + "="*80)
    print("ANALYSE DES LIVRES PAR RATING")
    print("="*80)
    
    # En-tête du tableau
    print(f"{'Rating':<10} {'Average_Price':<15} {'Total_Stock':<15} {'Value':<15} {'Book_Count':<15}")
    print("-" * 80)
    
    # Lignes du tableau
    for rating in sorted(results.keys()):
        data = results[rating]
        
        # affichage spécial pour rating 0 (erreurs)
        if rating == 0:
            rating_display = "0 (Erreur)"
        else:
            rating_display = str(rating)
        
        print(f"{rating_display:<10} "
              f"{data['Average_Price']:<15.2f} "
              f"{data['Total_Stock']:<15} "
              f"{data['Value']:<15.2f} "
              f"{data['Book_Count']:<15}")
    
    print("="*80 + "\n")

#fonction pour obtenir les statistiques globales
def get_global_statistics(books):
    
    try:
        total_books = len(books)
        
        if total_books == 0:
            return {
                'total_books': 0,
                'average_price': 0.0,
                'total_stock': 0,
                'total_value': 0.0,
                'min_price': 0.0,
                'max_price': 0.0
            }
        
        # Extraction des données
        prices = [book.get('price', 0.0) for book in books]
        stocks = [book.get('available', 0) for book in books]
        
        # Calcul des statistiques
        total_price = sum(prices)
        total_stock = sum(stocks)
        total_value = sum(book.get('price', 0) * book.get('available', 0) for book in books)
        
        stats = {
            'total_books': total_books,
            'average_price': round(total_price / total_books, 2),
            'total_stock': total_stock,
            'total_value': round(total_value, 2),
            'min_price': round(min(p for p in prices if p > 0) if any(p > 0 for p in prices) else 0.0, 2),
            'max_price': round(max(prices) if prices else 0.0, 2)
        }
        
        return stats
        
    except Exception as e:
        print(f"Error during the treatment : {e}")
        return {}

#fonction pour afficher les statistiques globales
def print_global_statistics(stats):

    print("\n" + "="*60)
    print("📈 STATISTIQUES GLOBALES")
    print("="*60)
    print(f"Nombre total de livres     : {stats.get('total_books', 0)}")
    print(f"Prix moyen                   : {stats.get('average_price', 0):.2f} £")
    print(f"Prix minimum                 : {stats.get('min_price', 0):.2f} £")
    print(f"Prix maximum                 : {stats.get('max_price', 0):.2f} £")
    print(f"Stock total                  : {stats.get('total_stock', 0)} livres")
    print(f"Valeur totale du stock       : {stats.get('total_value', 0):.2f} £")
    print("="*60 + "\n")


#fonction pour sauvegarder le rapport d'analyse dans un fichier texte
def save_analysis_to_file(analysis_output, directory="output", filename="analysis_report.txt"):
    try:

        output_dir = Path(directory)
        output_dir.mkdir(parents=True, exist_ok=True)
        filepath = output_dir / filename
        content_to_write = (
            "Rapport d'Analyse des Livres\n"
            + "=" * 35 
            + "\n\n"
            + analysis_output
        )
        filepath.write_text(content_to_write, encoding='utf-8')
        
        print(f"\nFiles save in : **{filepath}**")
        
    except Exception as e:
        print(f"Error during the saving : {e}")


#fonction principale pour analyser les données des livres
def analyze_data(books):
    
    try:
        #Gestion DataFrame ou liste vide
        if isinstance(books, pd.DataFrame):
            if books.empty:
                print("data not found (DataFrame empty)")
                return {}
            # Conversio de la DataFrame en liste de dictionnaires
            books = books.to_dict('records')
            print(f"DataFrame converti en liste de {len(books)} livres")
        elif isinstance(books, list):
            if len(books) == 0:
                print("data not found (list empty)")
                return {}
        else:
            print(f"Bad format of data : {type(books)}")
            return {}
        
        print(f"\nDÉBUT DE L'ANALYSE - {len(books)} livres")
        
        # Utilisation d'un buffer pour capturer tout impression
        f = io.StringIO()
        with redirect_stdout(f):
            results_by_rating = analyze_by_rating(books)
            print_analysis_table(results_by_rating)
            
            # Statistiques globales 
            global_stats = get_global_statistics(books)
            print_global_statistics(global_stats)
            
        # Récupération du contenu du buffer
        analysis_output = f.getvalue()
        
        # Impression du contenu capturé sur la console
        sys.stdout.write(analysis_output)
        
        # Sauvegarde le contenu capturé dans le fichier TXT, dans le dossier 'output'
        save_analysis_to_file(analysis_output, directory="output") 
        
        return {
            'by_rating': results_by_rating,
            'global_stats': global_stats,
            'books_list': books  
        }
        
    except Exception as e:
        print(f"Error : {e}")
        traceback.print_exc() 
        return {}


# Test de la fonction si le fichier est exécuté directement
if __name__ == "__main__":
    # Charger et nettoyer les données
    print("Chargement des données...")
    books = load_books()
    
    print("\nNettoyage des données...")
    books_cleaned = clean_data(books)
    
    # Analyser
    print("\nAnalyse des données...")
    results = analyze_data(books_cleaned)
    
    if results:
        print("\nAnalyse terminée avec succès !")
    else:
        print("\nÉchec de l'analyse")
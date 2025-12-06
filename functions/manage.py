#importer les librairies nécessaires
import pandas as pd
from pathlib import Path
import os


#indication du chemin du fichier csv 'books.csv'
csv_filename = os.environ.get('BOOKS_CSV_FILE', 'input/books.csv')
csv_file=Path(__file__).parent.parent/csv_filename


#fonction de lecture du fichier 'books.csv'
def load_books():

    if not csv_file.exists():
        print(f"File : {csv_file} not found.")
        return pd.DataFrame()
    
    try:
        #lecture du contenu du fichier 'books.csv'
        data_csv=pd.read_csv(csv_file,encoding='utf-8')

        return data_csv
    
    #capture des erreurs fichier introuvable et erreurs de decodage
    except (FileNotFoundError,pd.errors.EmptyDataError,IOError) as e:
        print(f"Erreur lors de la lecture du fichier CSV: {e}")
        return pd.DataFrame()
    
    #autres erreurs inattendues
    except Exception as e:
        print(f"Une erreur inattendue s'est produite: {e}")
        return pd.DataFrame()
    

    

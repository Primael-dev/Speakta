#imortations des bibliothèques nécessaires
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from .analyzer import analyze_data, load_books, clean_data 

# répertoire de sortie pour les images
OUTPUT_DIR = Path("output/visuals")

# Fonctions de création de graphiques

def create_distribution_plot(books_list):

    df = pd.DataFrame(books_list)
    
    # Exclusion des prix très faibles ou nuls 
    prices = df['price'][df['price'] > 1.0] 
    plt.figure(figsize=(10, 6))
    plt.hist(prices, bins=30, color='teal', edgecolor='black', alpha=0.7)
    
    plt.title('Distribution des Prix des Livres')
    plt.xlabel('Prix (£)')
    plt.ylabel('Fréquence (Nombre de Livres)')
    plt.grid(axis='y', alpha=0.5)
    
    # Sauvegarde
    plt.savefig(OUTPUT_DIR / '01_distribution_prix.png')
    plt.close()
    print(f"Généré : {OUTPUT_DIR / '01_distribution_prix.png'}")


def create_comparison_plot(results_by_rating):

    ratings_data = {
        r: results_by_rating[r] for r in sorted(results_by_rating.keys()) if r != 0
    }
    
    ratings = list(ratings_data.keys())
    avg_prices = [data['Average_Price'] for data in ratings_data.values()]
    
    plt.figure(figsize=(9, 6))
    
    bars = plt.bar(ratings, avg_prices, color='skyblue')
    
    plt.title('Prix Moyen des Livres par Note (Rating)')
    plt.xlabel('Note Étoile')
    plt.ylabel('Prix Moyen (£)')
    plt.xticks(ratings)
    plt.grid(axis='y', alpha=0.5)
    
    # Affichage de la valeur sur chaque barre
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, 
                 f'{yval:.2f}', ha='center', va='bottom', fontsize=9)

    # Sauvegarde
    plt.savefig(OUTPUT_DIR / '02_prix_moyen_par_note.png')
    plt.close()
    print(f"Généré : {OUTPUT_DIR / '02_prix_moyen_par_note.png'}")


def create_relationship_plot(books_list):

    df = pd.DataFrame(books_list)
    df_filtered = df[(df['available'] > 0) & (df['price'] > 0.0)]
    
    plt.figure(figsize=(10, 6))
    
    # Utilisation du Rating pour colorer les points (meilleure information visuelle)
    scatter = plt.scatter(
        df_filtered['price'], 
        df_filtered['available'], 
        c=df_filtered['rating'], 
        cmap='viridis', 
        alpha=0.6,
        s=30 
    )
    
    plt.title('Relation entre Prix et Stock (coloré par Note)')
    plt.xlabel('Prix (£)')
    plt.ylabel('Stock Disponible')
    plt.grid(True, linestyle='--', alpha=0.3)
    cbar = plt.colorbar(scatter)
    cbar.set_label('Note (Rating)')

    # Sauvegarde
    plt.savefig(OUTPUT_DIR / '03_prix_vs_stock.png')
    plt.close()
    print(f"Généré : {OUTPUT_DIR / '03_prix_vs_stock.png'}")


# --- Fonction principale de visualisation  et de l'analyse ---

def run_visualizer():
    
    # Chargement et nettoyage des données
    print("\n--- Préparation des données pour la visualisation ---")
    try:
        books_cleaned = clean_data(load_books()) 
        analysis_results = analyze_data(books_cleaned) 
    except Exception as e:
        print(f"Error during the treamtment: {e}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("\nGénération des graphiques")
    
    if analysis_results:
        books_list = analysis_results['books_list']
        results_by_rating = analysis_results['by_rating']
        create_distribution_plot(books_list)
        create_comparison_plot(results_by_rating)
        create_relationship_plot(books_list)
        
        print(f"\nToutes les visualisations ont été sauvegardées dans : **{OUTPUT_DIR.resolve()}**")
    else:
        print("\nImpossible de générer les graphiques : Aucune donnée d'analyse disponible.")

if __name__ == "__main__":
    run_visualizer()
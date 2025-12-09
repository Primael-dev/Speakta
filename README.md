# API_Flask

Auteur 

BANKOLE Primael M. William

Licence 

Ce projet est sous licence MIT.

---

## Description

Ce projet est un projet qui a pour but l'analyse des livres du projet_2(Webscrapping) afin d'en tirer des infos et de realiser des visualisations faciles à comprendre

---

## Installation

0.  Clonez le projet :
    ```bash
    git clone https://github.com/Primael-dev/Speakta.git
    ```
1.  Ouvrez votre terminal et naviguez vers le dossier du projet **`Speakta`**.

2.  Créez un environnement virtuel pour le projet :
    ```bash
    python -m venv env
    ```

3.  Activez cet environnement :
    * **Sur Windows :**
        ```bash
        env\Scripts\activate
        ```
    * **Sur macOS ou Linux :**
        ```bash
        source env/bin/activate
        ```

4.  Installez les modules nécessaires à l'exécution du programme à l'aide du fichier `requirements.txt` :
    ```bash
    pip install -r requirements.txt
    ```

---

## Utilisation

Une fois l'installation terminée et l'environnement activé, lancez le script en exécutant la commande suivante dans le terminal :

```bash
python app.py 
``` 
pour le test de l'Api avec Postman (recommandé)

```bash
pytest 
``` 
(non operationnel)

---

## Fonctionnement

L'exécution effectue les étapes suivantes :

    Chargement des données via functions/manage.py:load_books().

    Nettoyage des données via functions/data_cleaner.py:clean_data().

    Analyse et affichage des statistiques dans la console.

    Génération des rapports et graphiques.
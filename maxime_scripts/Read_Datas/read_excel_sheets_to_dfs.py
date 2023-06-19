import pandas as pd

import sys
import os

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


def read_excel_sheets_to_dfs(excel_file_path):
    # Utilisation de pandas pour lire le fichier Excel
    xls = pd.ExcelFile(excel_file_path)
    
    # Obtention des noms de toutes les feuilles du fichier
    sheet_names = xls.sheet_names
     
    # Création d'un dictionnaire pour stocker les dataframes
    dfs = {}
     
    # Lecture de chaque feuille et stockage dans le dictionnaire
    for sheet_name in sheet_names:
        df = xls.parse(sheet_name)
        dfs[sheet_name] = df
        print(df)
        print("---------------------------------------------------------")
    return dfs


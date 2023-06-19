import pandas as pd
import warnings
import sys
import os

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

def read_excel_sheets_xlsx(excel_file, Display = False, start_sheet=2, skip_rows=1):
    # Lire le nom de toutes les feuilles
    sheet_names = pd.ExcelFile(excel_file).sheet_names
 
    # Initialiser un dictionnaire pour stocker les dataframes
    dfs = {}

    # Lire chaque feuille, en commençant par 'start_sheet'
    for name in sheet_names[start_sheet:]:
        dfs[name] = pd.read_excel(excel_file, sheet_name=name, skiprows=skip_rows)
        if Display :
            print(dfs[name])

    return dfs

def read_excel_sheets_csv(excel_file, Display = False, start_sheet=2, skip_rows=1):
    # Lire le nom de toutes les feuilles
    sheet_names = pd.ExcelFile(excel_file).sheet_names

    # Initialiser un dictionnaire pour stocker les dataframes
    dfs = {}

    # Lire chaque feuille, en commençant par 'start_sheet'
    for name in sheet_names[start_sheet:]:
        dfs[name] = pd.read_csv(excel_file, sheet_name=name, skiprows=skip_rows)
        if Display :
            print(dfs[name])

    return dfs
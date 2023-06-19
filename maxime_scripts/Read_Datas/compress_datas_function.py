import pandas as pd
import parameters as parameters
import warnings
import sys
import os
import gzip
import shutil


from read_datas_sheet_to_dfs_only import read_excel_sheets
 
# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

excel_file_path = parameters.excel_file_path
filename_without_ext = parameters.filename_without_ext
excel_file_path_gzip = parameters.excel_file_path_gzip

def decompress_gzip(file_path):
    with gzip.open(file_path, 'rb') as f_in:
        with open(file_path[:-3], 'wb') as f_out:  # supprime l'extension '.gz'
            shutil.copyfileobj(f_in, f_out)

def excel_to_csv_gz(file_path, file_name):
    # Lire le fichier Excel
    xls = pd.read_excel(file_path, sheet_name=None)

    # Concaténer tous les DataFrames en un seul
    df = pd.concat(xls.values(), ignore_index=True)

    # Créer le chemin complet du fichier, y compris le nom du fichier et l'extension
    full_file_path = os.path.join(file_path, f"{file_name}.csv.gz")

    # Sauvegarder le DataFrame en tant que fichier csv.gz
    df.to_csv(full_file_path, index=False, compression='gzip')


def read_gzip_excel_sheets(excel_file, Display = True, start_sheet=2, skip_rows=1):
    # Décompresse le fichier gzip
    decompress_gzip(excel_file)
    
    # supprime l'extension '.gz' du nom du fichier
    excel_file = excel_file[:-3]
    
    # Lire le nom de toutes les feuilles
    sheet_names = pd.ExcelFile(excel_file).sheet_names

    # Initialiser un dictionnaire pour stocker les dataframes
    dfs = {}

    # Lire chaque feuille, en commençant par 'start_sheet'
    for name in sheet_names[start_sheet:]:
        dfs[name] = pd.read_excel(excel_file, sheet_name=name, skiprows=skip_rows)
        if Display:
            print(dfs[name])

    return dfs

#dfs = read_excel_sheets(excel_file_path)
#excel_to_csv_gz(excel_file_path, filename_without_ext)
#dfs_gzip = read_gzip_excel_sheets(excel_file_path_gzip)

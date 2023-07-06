import sys
import os
import pandas as pd
import dolfyn as dlfn
import re
from io import StringIO

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


def read_semicolon_separated_csv(file_path, display=True):
    # Lire le fichier comme un texte
    with open(file_path, 'r') as f:
        data = f.read()

 

    # Supprimer les virgules au début et à la fin de chaque ligne
    cleaned_data = re.sub(r'^;|;;;$', '', data, flags=re.MULTILINE)

 

    # Lire les données nettoyées comme un DataFrame
    df = pd.read_csv(StringIO(cleaned_data), skiprows=1, sep=',', parse_dates={'Datetime':['Year', 'Month', 'Day']}, keep_date_col=True)
    df = df.dropna(axis=1, how='all')

    return df
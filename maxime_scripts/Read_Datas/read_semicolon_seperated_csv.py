import pandas as pd
import warnings
import sys
import os
from datetime import timedelta

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


def read_semicolon_separated_csv(file_path, display=True):
    # Lire le fichier csv
    df = pd.read_csv(file_path, sep=';')
    if 'DateTime' in df.columns:
        df['DateTime'] = pd.to_datetime(df['DateTime'], format='%m/%d/%Y %H:%M:%S')

    # Afficher le DataFrame si demandé
    if display:
        print(df)

    return df 
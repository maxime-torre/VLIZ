import pandas as pd

import sys
import os

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


def read_pickle_to_df(file_path, Display = True):
    try:
        df = pd.read_pickle(file_path)
        if Display :
            print(df.head())
        return df
    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture du fichier pickle : {e}")
        return None
 
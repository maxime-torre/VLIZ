import pandas as pd

import sys
import os

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


def read_pickle_to_df(excel_file_path, Display = False):
    # Séparer le chemin de base et l'extension

    df = pd.read_pickle(excel_file_path)
    df = df.reset_index(drop=True)
    
    if Display :
        print(df)
        
    return df
 
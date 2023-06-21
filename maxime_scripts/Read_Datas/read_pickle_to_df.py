import pandas as pd

import sys
import os

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


def read_pickle_to_df(excel_file_path, Display = True):
    # Séparer le chemin de base et l'extension
    base_path, extension = os.path.splitext(excel_file_path)

    # Ajouter "_process_data" au chemin de base, puis ajouter l'extension .pkl
    new_path = base_path + "_process_data.pkl"
    df = pd.read_pickle(new_path)
    
    if Display :
        print(df)
        
    return df
 
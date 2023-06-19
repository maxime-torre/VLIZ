import pandas as pd
import sys
import os

from optimize_dataframe.compare_dataframe import compare_dataframes

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grand_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, grand_parent_dir)
 
def downcast_float(df):
    float_cols = [c for c in df if df[c].dtype == "float64"]
    df[float_cols] = df[float_cols].astype('float32')
    return df
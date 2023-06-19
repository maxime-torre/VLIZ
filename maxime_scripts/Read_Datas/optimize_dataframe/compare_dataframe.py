import pandas as pd
import parameters
import warnings
import sys
import os

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grand_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, grand_parent_dir)
 
excel_file = parameters.excel_file_path

def compare_dataframes(df1, df2):
    numeric_cols = [c for c in df1 if pd.api.types.is_numeric_dtype(df1[c])]
    error = ((df1[numeric_cols] - df2[numeric_cols]).abs() / df1[numeric_cols].abs()).mean()
    print(f"Error between df 64 bits and 32 bits for Pressure value is : {error}")
    return error
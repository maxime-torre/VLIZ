# main.py

import sys
import os
import pandas as pd
from datetime import timedelta

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Read_Datas.read_datas_sheet_to_dfs_only import read_excel_sheets_xlsx

def dict_pressure_dataframe_to_organize_dataframe(excel_file_path, columns_to_drop, Display = False):
    dfs = read_excel_sheets_xlsx(excel_file_path)
    df = pd.concat(dfs.values())
    df['Time'] = df['Time'] + timedelta(hours = 2)
    
    df = df.drop(columns_to_drop, axis=1) # suppression des colonnes inutiles
    
    if Display :
        print(df)
    
    return df
        
    
    

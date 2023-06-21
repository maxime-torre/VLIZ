# main.py

import sys
import os
import pandas as pd

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from constance_scripts.open_and_save_ad2cp_data import read_ad2cp_to_dataframe
from constance_scripts import parameters

ad2cp_file_path = parameters.ad2cp_file_path

df = pd.read_pickle(ad2cp_file_path)

df = df.vel

# Convertir le DataArray en un Dataset
ds = df.to_dataset()

# Convertir le Dataset en un DataFrame
df = ds.to_dataframe()

# Supprimer les colonnes inutiles
df = df.reset_index().drop(columns=['dir', 'range'])
print(df.info())
print("------------")
print(df)
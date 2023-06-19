import sys
import os
import pandas as pd
from scipy.signal import butter,filtfilt

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def add_surface_column(df):
    df["surface"] = df["Sea pressure"] - df["tide"]
    return df
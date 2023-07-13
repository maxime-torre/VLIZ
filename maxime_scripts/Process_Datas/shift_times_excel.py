import sys
import os
import pandas as pd
from scipy.signal import butter,filtfilt
from datetime import timedelta
import pickle

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def shift_times_excel(excel_path, date_debut, date_fin):
    return 0
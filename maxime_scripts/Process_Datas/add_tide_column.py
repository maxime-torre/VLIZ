import sys
import os
import pandas as pd
from scipy.signal import butter,filtfilt

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Process_Datas.butter_lowpass_filter import butter_lowpass_filter

def add_tide_column(df, cutoff, fs, order):
    df["tide"] = butter_lowpass_filter(df["Sea pressure"], cutoff, fs, order)
    return df

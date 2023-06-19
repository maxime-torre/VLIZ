import sys
import os
import pandas as pd
from scipy.signal import butter,filtfilt

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def butter_lowpass_filter(dataset, cutoff, fs, order):
    nyq = fs * 0.5
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients 
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, dataset)
    
    return y
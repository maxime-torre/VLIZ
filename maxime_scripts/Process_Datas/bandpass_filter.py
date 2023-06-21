import sys
import os
import pandas as pd
from scipy.signal import butter,filtfilt

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import numpy as np
from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=5):
    """ 
    Construit un filtre passe-bande Butterworth.
    lowcut : Fréquence de coupure basse
    highcut : Fréquence de coupure haute
    fs : Fréquence d'échantillonnage
    order : Ordre du filtre
    """
    nyq = 0.5 * fs  # Fréquence de Nyquist
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def apply_bandpass_filter(data, lowcut, highcut, fs, order=5):
    """
    Applique un filtre passe-bande à un signal.
    data : Signal à filtrer
    lowcut : Fréquence de coupure basse
    highcut : Fréquence de coupure haute
    fs : Fréquence d'échantillonnage
    order : Ordre du filtre
    """
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y
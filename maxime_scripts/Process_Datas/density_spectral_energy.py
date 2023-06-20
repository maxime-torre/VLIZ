import sys
import os
import pandas as pd
from scipy.signal import butter,filtfilt

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from scipy.signal import butter, lfilter, welch
from scipy.fftpack import fft, fftfreq

def bandpass_filter_and_spectrum(signal, fe, fmin, fmax):
    # Filtre passe-bande
    def butter_bandpass(lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
        b, a = butter_bandpass(lowcut, highcut, fs, order=order)
        y = lfilter(b, a, data)
        return y

    # Appliquer le filtre passe-bande
    signal_filt = butter_bandpass_filter(signal, fmin, fmax, fe)

    # Calculer la densité spectrale d'énergie (PSD) à l'aide de la méthode de Welch
    freqs, psd = welch(signal_filt, fe)
    freqs = pd.Series(freqs, name='Fréquency')
    psd = pd.Series(psd, name='Density Spectral Energy')

    return freqs, psd

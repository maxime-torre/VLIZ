import sys
import os
import pandas as pd
from scipy.signal import butter,filtfilt
from scipy import signal 
from numpy.fft import fft 
import inspect


# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import numpy as np

def compute_spectrum(signal, signal_name, fe, n_segments=100):
    # Assurez-vous que le signal est numérique
    if not np.issubdtype(signal.dtypes, np.number):
        raise ValueError("Signal should be numeric.")
    
    # Assurez-vous que le signal est divisible par n_segments
    divisible_length = len(signal) - len(signal) % n_segments
    signal = signal[:divisible_length]

    # Divise le signal en segments pour le moyennage spectral
    segments = np.array_split(signal, n_segments)
    
    amplitude_db_avg = []
    freqs_list = []

    for segment in segments:
        window = np.hamming(len(segment))
        segment = np.array(segment)
        segment = segment - segment.mean()
        
        segment = segment * window

        # Echantillonnage du signal
        t = np.arange(0, len(segment)/fe, 1/fe)

        # Calcul de la FFT
        fft_result = np.fft.fft(segment)

        # Calcul des fréquences correspondant aux valeurs de la FFT
        freqs = np.fft.fftfreq(len(segment), 1/fe)

        # On ne garde que la moitié des valeurs (partie positive du spectre)
        fft_result = fft_result[0:len(fft_result)//2]
        freqs = freqs[0:len(freqs)//2]

        # Conversion en dB
        amplitude_db = 20 * np.log10(np.abs(fft_result))
        
        amplitude_db_avg.append(amplitude_db)
        freqs_list.append(freqs)
    
    # Calcul du spectre moyen
    amplitude_db_avg = np.mean(np.array(amplitude_db_avg), axis=0)
    freqs = np.mean(np.array(freqs_list), axis=0)

    amplitude_db_avg = pd.Series(amplitude_db_avg, name=signal_name)
    freqs = pd.Series(freqs, name='Frequency (Hz)')

    return amplitude_db_avg, freqs



def compute_2D_spectrum(signal, time, depth):
    # Assurez-vous que le signal est numérique
    if not np.issubdtype(signal.dtypes, np.number):
        raise ValueError("Signal should be numeric.")

    # Remodeler le signal en 2D pour correspondre au temps et à la profondeur
    # Note: Cela suppose que signal est un tableau 1D plat et qu'il peut être redimensionné
    # aux mêmes dimensions que le temps et la profondeur.
    # Soustraire la moyenne
    signal = signal - np.mean(signal)

    # Appliquer une fenêtre de Hamming en 2D
    window = np.hamming(len(signal))
    signal = signal * window

    # Calcul de la FFT en 2D
    fft_result = np.fft.fft(signal)

    # Calcul des fréquences correspondant aux valeurs de la FFT
    freqs_time = np.fft.fftfreq(len(time))
    freqs_depth = np.fft.fftfreq(len(depth))

    # On ne garde que la moitié des valeurs (partie positive du spectre)
    fft_result = fft_result[0:len(fft_result)//2]
    freqs_time = freqs_time[0:len(freqs_time)//2]
    freqs_depth = freqs_depth[0:len(freqs_depth)//2]

    # Conversion en dB
    amplitude_db = 20 * np.log10(np.abs(fft_result))

    return amplitude_db, freqs_time, freqs_depth




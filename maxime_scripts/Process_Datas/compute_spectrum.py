import sys
import os
import pandas as pd
from scipy.signal import butter,filtfilt
from scipy import signal 
from numpy.fft import fft 

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import numpy as np

def compute_spectrum(df, signal_column_name, fe, n_segments=100):
    signal = df[signal_column_name]
    # Assurez-vous que le signal est divisible par n_segments
    divisible_length = len(signal) - len(signal) % n_segments
    signal = signal[:divisible_length]

    # Divise le signal en segments pour le moyennage spectral
    segments = np.array_split(signal, n_segments)
    
    amplitude_db_avg = []
    freqs_list = []

    for segment in segments:
        window = np.hamming(len(segment))
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

    amplitude_db_avg = pd.Series(amplitude_db_avg, name='amplitude dB')
    freqs = pd.Series(freqs, name='Frequency')

    return amplitude_db_avg, freqs



def calculerSpectre(echantillons,fe,fenetre,nz=2,db=False):
    N = echantillons.size
    p = int(np.log(nz*N)/np.log(2))
    NN = 2**p
    zeros=np.zeros(NN-N)
    echantillons = np.concatenate((echantillons*signal.get_window(fenetre,N),zeros))
    spectre = np.absolute(fft(echantillons))
    spectre = spectre / spectre.max()
    if db:
        spectre = 20*np.log10(spectre)
    freq = np.arange(NN)*fe/NN
    return [freq,spectre]

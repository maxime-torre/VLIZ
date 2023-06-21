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

def butter_highpass_filter(dataset, cutoff, fs, order):
    nyq = fs * 0.5
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients 
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    y = filtfilt(b, a, dataset)
    
    return y


def butter_bandpass_filter(dataset, lowcut, highcut, fs, order=3):
    # Filtre passe-haut
    y = butter_highpass_filter(dataset, lowcut, fs, order)
    
    # Filtre passe-bas
    y = butter_lowpass_filter(y, highcut, fs, order)
    
    return y

import scipy.signal

def low_pass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs  # Fréquence de Nyquist
    normal_cutoff = cutoff / nyq
    b, a = scipy.signal.butter(order, normal_cutoff, btype='low', analog=False)
    y = scipy.signal.lfilter(b, a, data)
    return y

def high_pass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs  # Fréquence de Nyquist
    normal_cutoff = cutoff / nyq
    b, a = scipy.signal.butter(order, normal_cutoff, btype='high', analog=False)
    y = scipy.signal.lfilter(b, a, data)
    return y

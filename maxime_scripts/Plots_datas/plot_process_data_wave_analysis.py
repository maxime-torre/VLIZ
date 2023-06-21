import sys
import os
import pandas as pd

from matplotlib.pyplot import *

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Plots_datas.plots_dataframe import plot_dataframe
from Process_Datas.compute_spectrum import compute_spectrum
from Process_Datas.butter_lowpass_filter import butter_bandpass_filter
from Read_Datas.read_pickle_to_df import read_pickle_to_df




def plot_process_data_wave_analysis(excel_file_path, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fs_data, fe, N):
    base_path, extension = os.path.splitext(excel_file_path)

    # Ajouter "_process_data" au chemin de base, puis ajouter l'extension de retour
    new_path = base_path + "_process_data" + ".pkl"
    print(new_path)
    df = read_pickle_to_df(new_path)

    bandpass_filtred_signal_ig = butter_bandpass_filter(df['Sea pressure'], fmin_ig, fmax_ig, fs_data)
    bandpass_filtred_signal_ig = bandpass_filtred_signal_ig - bandpass_filtred_signal_ig.mean()
    print(bandpass_filtred_signal_ig)
    bandpass_filtred_signal_ig = pd.Series(bandpass_filtred_signal_ig, name=f'IG bandpass filtred')

    bandpass_filtred_signal_ss = butter_bandpass_filter(df['Sea pressure'], fmin_ss, fmax_ss, fs_data)
    bandpass_filtred_signal_ss = bandpass_filtred_signal_ss - bandpass_filtred_signal_ss.mean()
    print(bandpass_filtred_signal_ss)
    bandpass_filtred_signal_ss = pd.Series(bandpass_filtred_signal_ss, name=f'SS bandpass filtred')
    
    Temperature = df['Temperature']
    Time = df['Time']
    Sea_pressure = df['Sea pressure']

    """mean_tide = df['tide'].mean()
    print(f"mean_tide : {mean_tide} m")
    Depth = df['Depth']
    Surface = df['surface']
    Tide = df['tide']
    k0 = df['k0 (deep water number)']"""

    spectre_dB, freqs = compute_spectrum(Sea_pressure, fe)

    plot_dataframe(df, N, (Time, Temperature), (Time, Sea_pressure),
                   #(Time, Depth), 
                   #(Time, Tide), 
                   #(Time, k0), 
                   #(Time, Surface), 
                #(Time, Energy_IG), (Time, Energy_SS),
                (freqs, spectre_dB, fmin_ig, fmax_ig ),
                (freqs, spectre_dB, fmin_ss, fmax_ss ),
                (Time, bandpass_filtred_signal_ig**2),
                (Time, bandpass_filtred_signal_ss**2))
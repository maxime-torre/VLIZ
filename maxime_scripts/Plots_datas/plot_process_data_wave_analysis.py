import sys
import os
import pandas as pd

from matplotlib.pyplot import *
from datetime import timedelta

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Plots_datas.plots_dataframe import plot_dataframe
from Process_Datas.compute_spectrum import compute_spectrum
from Process_Datas.butter_lowpass_filter import butter_bandpass_filter
from Read_Datas.read_pickle_to_df import read_pickle_to_df
from Process_Datas.add_waves_description_columns import fourier_windows


def plot_process_data_wave_analysis(excel_file_path, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fs_data, fe, N, seconds, fe_ig, fe_ss):
    """base_path, extension = os.path.splitext(excel_file_path)

    # Ajouter "_process_data" au chemin de base, puis ajouter l'extension de retour
    new_path = base_path + "_process_data" + ".pkl"
    print(new_path)"""
    df = read_pickle_to_df(excel_file_path)
    df = df.head(N)
    print(df)

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
    AltimeterDistanceAST = df['AltimeterDistanceAST']

    """mean_tide = df['tide'].mean()
    print(f"mean_tide : {mean_tide} m")
    Depth = df['Depth']
    Surface = df['surface']
    Tide = df['tide']
    k0 = df['k0 (deep water number)']"""

    df = fourier_windows(df, seconds, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fe_ig, fe_ss)
    print(df)
    spectre_dB, freqs = compute_spectrum(Sea_pressure, fe)

    Hm0_IG = df['Hm0,IG']
    Hm0_SS = df['Hm0,SS']
    frequency_IG = df['frequency,IG']
    frequency_SS = df['frequency,SS']
    energy_IG = df['energy,IG']
    energy_SS = df['energy,SS']
    Hm0_total = df['Hm0,total']
    
    plot_dataframe(df, N, 
                   [(Time,Temperature,Sea_pressure),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])
    
    plot_dataframe(df, N, 
                   [(Time,Hm0_IG,Hm0_SS,Hm0_total),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5)), 
                    (Time.min()+timedelta(minutes=15),Time.max()-timedelta(minutes=15), 'ig waves'), (Time.min()+timedelta(minutes=10),Time.max()-timedelta(minutes=10), 'sea swell waves')])

    
"""    plot_dataframe(df, N, (Time, Temperature), (Time, Sea_pressure),
                   #(Time, Depth), 
                   #(Time, Tide), 
                   #(Time, k0), 
                   #(Time, Surface), 
                #(Time, Energy_IG), (Time, Energy_SS),
                (freqs, spectre_dB),
                (freqs, spectre_dB, fmin_ig, fmax_ig ),
                (freqs, spectre_dB, fmin_ss, fmax_ss ),
                (Time, bandpass_filtred_signal_ig**2, Time.min() + timedelta( minutes = 5), Time.max() - timedelta( minutes = 5) ),
                (Time, bandpass_filtred_signal_ss**2, Time.min() + timedelta( minutes = 5), Time.max() - timedelta( minutes = 5) ),
                (Time, Hm0_IG, Time.min() + timedelta( minutes = 5), Time.max() - timedelta( minutes = 5)),
                (Time, Hm0_SS, Time.min() + timedelta( minutes = 5), Time.max() - timedelta( minutes = 5)),
                (Time, Hm0_total, Time.min() + timedelta( minutes = 5), Time.max() - timedelta( minutes = 5)),
                (frequency_IG, energy_IG),
                (frequency_SS, energy_SS))"""
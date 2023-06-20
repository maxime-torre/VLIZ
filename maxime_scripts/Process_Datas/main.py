# main.py

import sys
import os
import pandas as pd
import math
import numpy as np
from matplotlib.pyplot import *
from numpy.fft import fft 
from datetime import timedelta

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Process_Datas import parameters
from Process_Datas.dict_dataframe_to_organize_data import dict_pressure_dataframe_to_organize_dataframe
from Process_Datas.add_tide_column import add_tide_column
from Process_Datas.add_surface_column import add_surface_column
from Plots_datas.plots_dataframe import plot_dataframe
from Process_Datas.add_surface_correlation_column import add_surface_correlation_column_and_cte_evaluation, check_complex_values
from Process_Datas.add_waves_description_columns import fourier, fourier_windows
from Process_Datas.compute_spectrum import compute_spectrum
from Process_Datas.remove_jump_rows import remove_jump_rows
from Process_Datas.density_spectral_energy import bandpass_filter_and_spectrum
from Plots_datas.plot_spectrogram import compute_spectrogram

N = parameters.N
excel_file_path = parameters.excel_file_path
columns_to_drop = parameters.columns_to_drop

fs = parameters.fs
dt = parameters.dt
cutoff = parameters.cutoff
order = parameters.order

hbed = parameters.hbed

fmin_ig = parameters.fmin_ig
fmax_ig = parameters.fmax_ig
fmin_ss = parameters.fmin_ss
fmax_ss = parameters.fmax_ss
fe_ig = parameters.fe_ig
fe_ss = parameters.fe_ss
hour = parameters.hour
minutes = parameters.minutes
seconds = parameters.seconds
fe=parameters.fe
cutoff_low_pass = parameters.cutoff_low_pass
fs_data = parameters.fs_data


df = dict_pressure_dataframe_to_organize_dataframe(excel_file_path, columns_to_drop)
df['Time'] = df['Time'] + timedelta(hours = 2)
print(df.info())
print(df)
#df = df.iloc[N:6*N]
add_tide_column(df, cutoff, fs, order)
add_surface_column(df)
cte_evaluation_wave = add_surface_correlation_column_and_cte_evaluation(df, fs, hbed)
print(f"kp(pressure response factor): {cte_evaluation_wave[0]} | h(mean water depth in m) : {cte_evaluation_wave[1]} | k(wave number) : {cte_evaluation_wave[2]}")
df = remove_jump_rows(df, "Sea pressure", 0.11, fs_data)
print(df)
#fourier_result = fourier(df['Sea pressure'],fmin,fmax, fsep)
#print(fourier_result)
#fourier_windows(df, seconds, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fe_ig, fe_ss)

"""wave_result = fourier_windows(df, hour, fmin, fsep, fmax, fsep)
print(wave_result)"""
Temperature = df['Temperature']
Time = df['Time']
# Prenez la valeur minimale de 'Time' comme référence
reference_time = df['Time'].min()
# Convertissez la colonne 'Time' en secondes depuis la date de référence
Time_in_seconds = (df['Time'] - reference_time) // pd.Timedelta('1s')

Sea_pressure = df['Sea pressure']
Depth = df['Depth']
Surface = df['surface']
Tide = df['tide']
k0 = df['k0 (deep water number)']
#Energy_IG = df['energy,IG']
#Energy_SS = df['energy,SS']

spectre_dB, freqs = compute_spectrum(Sea_pressure, fe)

#Frequency_DSE_IG, DSE_IG = bandpass_filter_and_spectrum(df['Sea pressure'], fe_ig, fmin_ig, fmax_ig)

mean_tide = df['tide'].mean()
print(f"mean_tide : {mean_tide} m")

plot_dataframe(df, N, (Time, Temperature), (Time, Sea_pressure), (Time, Depth), (Time, Tide), (Time, k0), (Time, Surface), 
               #(Time, Energy_IG), (Time, Energy_SS),
               (freqs, spectre_dB, fmin_ig, fmax_ig ),
               (freqs, spectre_dB, fmin_ss, fmax_ss ),
               (Time, Sea_pressure**2))

#compute_spectrogram(df['Sea pressure'], fe, fmin_ig,fmax_ig)


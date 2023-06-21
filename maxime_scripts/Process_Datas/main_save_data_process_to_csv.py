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
from Process_Datas.bandpass_filter import bandpass_filter
from Plots_datas.plot_spectrogram import compute_spectrogram
from Process_Datas.process_concatenate_save_dataframe import process_concatenate_save_dataframe

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


df = process_concatenate_save_dataframe(excel_file_path, columns_to_drop, cutoff, fs, order, hbed, fs_data, fe)
print(df)
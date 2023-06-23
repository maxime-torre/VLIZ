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
from Plots_datas.plot_process_data_wave_analysis import plot_process_data_wave_analysis


N = parameters.N
excel_pressure_file_path = parameters.excel_file_path
excel_adcp_file_path = parameters.adcp_file_path
columns_to_drop = parameters.columns_to_drop

pickle_all_adcp_data_path = parameters.pickle_all_adcp_data_path

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
fs_data_adcp_all = parameters.fs_data_adcp_all

pickle_path_file_ADCP = parameters.pickle_path_file_ADCP
pickle_path_file_Pressure_sensor = parameters.pickle_path_file_Pressure_sensor


plot_process_data_wave_analysis(pickle_path_file_ADCP, pickle_path_file_Pressure_sensor, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fs_data_adcp_all, fe, N,  seconds, fe_ig, fe_ss)


# main_trapergeer.py

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

import parameters
from Plots_datas.plot_pressure_data_comparaison import plot_pressure_data_comparaison


pickle_path_file_ADCP_trapergeer_2023  = parameters.pickle_path_file_ADCP_trapergeer_2023
pickle_path_file_Pressure_sensor_trapergeer_2023  = parameters.pickle_path_file_Pressure_sensor_trapergeer_2023

pickle_path_file_ADCP_test_september_2022 = parameters.pickle_path_file_ADCP_test_september_2022
pickle_path_file_Pressure_sensor_test_september_2022= parameters.pickle_path_file_Pressure_sensor_test_september_2022

N = parameters.N
cutoff = parameters.cutoff
fe_ADCP = parameters.fe_ADCP
fe_PS = parameters.fe_PS
samples_cutoff_filter = parameters.samples_cutoff_filter
fmin_ig = parameters.fmin_ig
fmax_ig = parameters.fmax_ig
fmin_ss = parameters.fmin_ss
fmax_ss = parameters.fmax_ss
hour = parameters.hour
seconds = parameters.seconds
hbed = parameters.hbed

plot_pressure_data_comparaison(pickle_path_file_ADCP_trapergeer_2023, pickle_path_file_Pressure_sensor_trapergeer_2023, N, cutoff, fe_ADCP, fe_PS, samples_cutoff_filter, fmin_ig, fmax_ig, fmin_ss, fmax_ss)
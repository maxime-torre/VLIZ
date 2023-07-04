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
from Read_Datas.read_pickle_to_df import read_pickle_to_df
from Process_Datas.add_waves_description_columns import fourier_windows
from Plots_datas.plots_dataframe import plot_dataframe
from Process_Datas.sub_sampling_dataframe import resample_dataframe, compare_time_columns
from Process_Datas.butter_lowpass_filter import butter_lowpass_filter


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
save_data_ADCP_path = parameters.save_data_ADCP_path
pickle_path_file_buoys = parameters.pickle_path_file_buoys

#test = "C:\\Users\\maxixme.torre\\Documents\\20220901-PS2201_test_RBR\\Datas\\ADCP\\S102377A024_Test_RBR_Q3B0_1_process_data.pkl"

#plot_process_data_wave_analysis(pickle_path_file_ADCP, pickle_path_file_Pressure_sensor, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fs_data_adcp_all, fe, N,  seconds, fe_ig, fe_ss, cutoff)
pickle_path_file_ADCP_init = read_pickle_to_df(pickle_path_file_ADCP)
pickle_path_file_ADCP_init  =pickle_path_file_ADCP_init.head(N)
pickle_path_file_ADCP_init['Time'] = pickle_path_file_ADCP_init['Time'].dt.floor('S')
print(pickle_path_file_ADCP_init)




"""plot_dataframe(N, "ADCP : Sea pressure vs Altimeter pressure", 
               [(pickle_path_file_ADCP_init['Time'], pickle_path_file_ADCP_init['Hm0,IG'], pickle_path_file_ADCP_init['Hm0,SS']),
                    (pickle_path_file_ADCP_init['Time'].min(),pickle_path_file_ADCP_init['Time'].max()) ])"""


"""pickle_path_file_ADCP_init_resample, pickle_path_file_buoys_init = compare_time_columns(pickle_path_file_ADCP_init_resample, pickle_path_file_buoys_init)

print('pickle_path_file_buoys_init')
print(pickle_path_file_buoys_init)
print("pickle_path_file_ADCP_init_resample")
print(pickle_path_file_ADCP_init_resample)"""
pickle_path_file_ADCP_init['AltimeterPressure'] = pickle_path_file_ADCP_init['AltimeterPressure']*10
print(pickle_path_file_ADCP_init)
pickle_path_file_ADCP_init['AltimeterPressure'] =  pickle_path_file_ADCP_init['AltimeterPressure'] - butter_lowpass_filter(pickle_path_file_ADCP_init['AltimeterPressure'], cutoff, fs, order)
print(pickle_path_file_ADCP_init)


pickle_path_file_ADCP_init = fourier_windows(pickle_path_file_ADCP_init, 'AltimeterPressure', seconds, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fe_ig, fe_ss, save_data_ADCP_path)
print(pickle_path_file_ADCP_init)



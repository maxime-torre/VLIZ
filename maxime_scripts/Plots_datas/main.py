# main.py
import sys
import os
import pandas as pd
from datetime import timedelta
from scipy import stats
import numpy as np

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import parameters
from Plots_datas.plots_dataframe import plot_dataframe_dict, plot_dataframe, plot_dataframe_columns, plot_with_linear_regression
from Read_Datas.read_excel_sheets_to_dfs import read_excel_sheets_to_dfs
from Read_Datas.read_pickle_to_df import read_pickle_to_df
from Read_Datas.read_datas_sheet_to_dfs_only import read_excel_sheets_xlsx, read_excel_sheets_csv
from Read_Datas.read_semicolon_seperated_csv import read_semicolon_separated_csv
from Plots_datas.plot_pressure_data_comparaison import plot_pressure_data_comparaison
from Process_Datas.add_waves_description_columns import depth_to_pressure, pressure_from_depth_hydraustatique_and_dynamique, pressure_to_depth
from Process_Datas.butter_lowpass_filter import low_pass_filter
from Plots_datas.plot_ADCP_PressurevsAltimeter_comparaison import plot_ADCP_PressurevsAltimeter_comparaison
  
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
latitude = parameters.latitude



plot_ADCP_PressurevsAltimeter_comparaison(N,
                                          pickle_path_file_ADCP_test_september_2022,
                                          cutoff,
                                          fe_ADCP,
                                          fmin_ig,
                                          fmax_ig,
                                          fmin_ss,
                                          fmax_ss,
                                          latitude)



# main_test_t_tide.py
import sys
import os
import pandas as pd
from datetime import timedelta

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import parameters
from Plots_datas.plots_dataframe import plot_dataframe_dict, plot_dataframe, plot_dataframe_columns
from Read_Datas.read_excel_sheets_to_dfs import read_excel_sheets_to_dfs
from Read_Datas.read_pickle_to_df import read_pickle_to_df
from Read_Datas.read_datas_sheet_to_dfs_only import read_excel_sheets_xlsx, read_excel_sheets_csv
from Read_Datas.read_semicolon_seperated_csv import read_semicolon_separated_csv
from Plots_datas.plot_pressure_data_comparaison import plot_pressure_data_comparaison
from Process_Datas.butter_lowpass_filter import high_pass_filter
from Plots_datas.u_tide_estimation import u_tide_estimation

"""sys.path.insert(0, 'C:\\Users\\maxixme.torre\\Documents\\20220901-PS2201_test_RBR\\ttide_py-master')
import ttide as tt"""

from utide import solve
from utide import reconstruct

N = parameters.N
cutoff = parameters.cutoff
fe_ADCP = parameters.fe_ADCP
latitude = parameters.latitude

pickle_path_file_ADCP_trapergeer_2023  = parameters.pickle_path_file_ADCP_trapergeer_2023
pickle_path_file_Pressure_sensor_trapergeer_2023  = parameters.pickle_path_file_Pressure_sensor_trapergeer_2023

pickle_path_file_ADCP_test_september_2022 = parameters.pickle_path_file_ADCP_test_september_2022
pickle_path_file_Pressure_sensor_test_september_2022= parameters.pickle_path_file_Pressure_sensor_test_september_2022

df_ADCP= read_pickle_to_df(pickle_path_file_ADCP_test_september_2022)
df_ADCP = df_ADCP.head(N)
Time = df_ADCP.Time
print(df_ADCP)

distance = df_ADCP['AltimeterDistanceAST']

u_tide_estimation_m, distance_without_tide = u_tide_estimation(distance,Time, latitude)

pressure_without_tide_HighPass = high_pass_filter(distance, "AltimeterDistanceAST", cutoff, fe_ADCP)
pressure_without_tide_HighPass = pd.Series(pressure_without_tide_HighPass, name="Distance_without_tide_HighPass")

plot_dataframe(N, "Distance (m)" ,
                [(Time,distance,distance_without_tide, pressure_without_tide_HighPass, u_tide_estimation_m),
                (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])

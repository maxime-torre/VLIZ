# main.py
import sys
import os
import pandas as pd

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Plots_datas import parameters
from Plots_datas.plots_dataframe import plot_dataframe_dict, plot_dataframe, plot_dataframe_columns
from Read_Datas.read_excel_sheets_to_dfs import read_excel_sheets_to_dfs
from Read_Datas.read_datas_sheet_to_dfs_only import read_excel_sheets_xlsx, read_excel_sheets_csv
from Read_Datas.read_semicolon_seperated_csv import read_semicolon_separated_csv
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

plot_pressure_data_comparaison(pickle_path_file_ADCP_test_september_2022, 
                               pickle_path_file_Pressure_sensor_test_september_2022, 
                               N, 
                               cutoff, 
                               fe_ADCP, 
                               fe_PS, 
                               samples_cutoff_filter,
                               fmin_ig,
                               fmax_ig,
                               fmin_ss,
                               fmax_ss)

"""df = read_semicolon_separated_csv(adcp_B)
df = df.loc[:, ['DateTime', 'Temperature', 'Pressure', 'AltimeterPressure', 'AltimeterDistanceAST']]
df = df.rename(columns={'DateTime': 'Time'})
df = df.rename(columns={'Pressure': 'Sea pressure'})
base_path, extension = os.path.splitext(adcp_B)

# Ajouter "_process_data" au chemin de base, puis ajouter l'extension de retour
new_path = base_path + "_process_data" + ".pkl"
print(df.info())
print(df)

df.to_pickle(new_path)"""


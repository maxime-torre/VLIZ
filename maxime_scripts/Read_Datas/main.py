import pandas as pd
import parameters
import warnings
import sys
import os
import numpy as np

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from read_semicolon_seperated_csv import read_semicolon_separated_csv
from Plots_datas.plots_dataframe import plot_dataframe
from Read_Datas.read_pickle_to_df import read_pickle_to_df
from Read_Datas.read_datas_sheet_to_dfs_only import read_excel_sheets_xlsx
from Process_Datas.save_adcp_data_process_to_pickle import process_adcp_excel_files, concatenate_dataframes
from Process_Datas.sub_sampling_dataframe import resample_dataframe
from Process_Datas.save_buoys_data_to_pickle import merge_data

excel_file = parameters.excel_file_path
ADCP_path_file = parameters.adcp_path_file
N = parameters.N

"""df = read_semicolon_separated_csv(ADCP_path_file)
plot_dataframe(df, N)"""

pickle_path_file_ADCP = parameters.pickle_path_file_ADCP
pickle_path_file_Pressure_sensor = parameters.pickle_path_file_Pressure_sensor
all_pickle_path_file_ADCP = parameters.all_pickle_path_file_ADCP
all_csv_path_file_PS = parameters.all_csv_path_file_PS
all_pickle_path_file_PS = parameters.all_pickle_path_file_PS
pickle_dict_of_data_path = parameters.pickle_dict_of_data_path
pickle_all_adcp_data_path = parameters.pickle_all_adcp_data_path
fs = parameters.fs 
threshold = parameters.threshold

Trapergeer_wave_height_text_file = parameters.Trapergeer_wave_height_text_file
Trapergeer_wave_period_text_file = parameters.Trapergeer_wave_period_text_file

"""df_buoy = merge_data(Trapergeer_wave_height_text_file,Trapergeer_wave_period_text_file, "All_BUOYS_processed_data_8Feb_10Apr",'2023-02-08', '2023-04-11')
print(df_buoy)"""

test = "C:\\Users\\maxixme.torre\\Documents\\Infra_gravity_waves_datas\\Trapegeer_8Feb_10Apr_2023_ADCP_PS_BUOYS\\ADCP\\All_ADCP_processed_data_8Feb_10Apr.pkl"
df = read_pickle_to_df(test)
print(df)
df = df.head(N)
print(df)

# Calcule le coefficient de corrélation de Pearson
correlation_coefficient = np.corrcoef(df['AltimeterPressure'], df['Sea pressure'])[0, 1]
print(f"correlation_coefficient : {correlation_coefficient}")

plot_dataframe(N, "ADCP : Sea pressure vs Altimeter pressure", 
               [(df['Time'], df['AltimeterPressure'], df['Sea pressure']),
                    (df['Time'].min(),df['Time'].max()),
                    (df['Time'].min(), pd.to_datetime("2023 02 15 12:45:00"), 'Pressure before singularity'), 
                    (pd.to_datetime("2023 02 15 12:45:00"),df['Time'].max(), 'Pressure after singularity')])


# Enregistrer le DataFrame global en fichier pickle
#df.to_pickle(pickle_all_adcp_data_path)

"""plot_dataframe(N, "Pitch and Roll for ADCP sensor", 
               [(df['Time'],df['Pitch'], df['Roll']),
                    (df['Time'].min(),df['Time'].max())])"""

"""print("---------------------all_pickle_path_file_PS---------------------")
df = read_pickle_to_df(all_pickle_path_file_PS)
print(df)
print(df.info())
"""
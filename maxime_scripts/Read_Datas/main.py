import pandas as pd
import parameters
import warnings
import sys
import os

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from read_semicolon_seperated_csv import read_semicolon_separated_csv
from Plots_datas.plots_dataframe import plot_dataframe
from Read_Datas.read_pickle_to_df import read_pickle_to_df

excel_file = parameters.excel_file_path
ADCP_path_file = parameters.adcp_path_file
N = parameters.N

"""df = read_semicolon_separated_csv(ADCP_path_file)
plot_dataframe(df, N)"""

pickle_path_file_ADCP = parameters.pickle_path_file_ADCP
pickle_path_file_Pressure_sensor = parameters.pickle_path_file_Pressure_sensor

print("---------------------pickle_path_file_ADCP---------------------")
df = read_pickle_to_df(pickle_path_file_ADCP)
print(df.info())
print("---------------------pickle_path_file_Pressure_sensor---------------------")
df2 = read_pickle_to_df(pickle_path_file_Pressure_sensor)
print(df2.info())

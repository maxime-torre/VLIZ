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

excel_file_path = parameters.excel_file_path
adcp_A = parameters.adcp_A
adcp_B = parameters.adcp_B

N = parameters.N


df = read_semicolon_separated_csv(adcp_B)
df = df.loc[:, ['DateTime', 'Temperature', 'Pressure', 'AltimeterPressure', 'AltimeterDistanceAST']]
df = df.rename(columns={'DateTime': 'Time'})
df = df.rename(columns={'Pressure': 'Sea pressure'})
base_path, extension = os.path.splitext(adcp_B)

# Ajouter "_process_data" au chemin de base, puis ajouter l'extension de retour
new_path = base_path + "_process_data" + ".pkl"
print(df.info())
print(df)

df.to_pickle(new_path)


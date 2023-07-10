# main_test_t_tide.py
import sys
import os
import pandas as pd
from datetime import timedelta

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Plots_datas import parameters
from Plots_datas.plots_dataframe import plot_dataframe_dict, plot_dataframe, plot_dataframe_columns
from Read_Datas.read_excel_sheets_to_dfs import read_excel_sheets_to_dfs
from Read_Datas.read_pickle_to_df import read_pickle_to_df
from Read_Datas.read_datas_sheet_to_dfs_only import read_excel_sheets_xlsx, read_excel_sheets_csv
from Read_Datas.read_semicolon_seperated_csv import read_semicolon_separated_csv
from Plots_datas.plot_pressure_data_comparaison import plot_pressure_data_comparaison
from Process_Datas.add_waves_description_columns import pressure_factor, pressure_from_depth_hydraustatique_and_dynamique
from Process_Datas.butter_lowpass_filter import high_pass_filter

"""sys.path.insert(0, 'C:\\Users\\maxixme.torre\\Documents\\20220901-PS2201_test_RBR\\ttide_py-master')
import ttide as tt"""

from utide import solve
from utide import reconstruct

N = parameters.N
cutoff = parameters.cutoff
fe_ADCP = parameters.fe_ADCP
latitude = parameters.latitude

pickle_path_file_ADCP_test_september_2022 = parameters.pickle_path_file_ADCP_test_september_2022
pickle_path_file_Pressure_sensor_test_september_2022= parameters.pickle_path_file_Pressure_sensor_test_september_2022

df_PS= read_pickle_to_df(pickle_path_file_Pressure_sensor_test_september_2022)
df_PS = df_PS.head(N)
Time = df_PS.Time
print(df_PS)

pressure = df_PS['Sea pressure']

# Présumons que 'time' est un tableau numpy de temps en heures depuis un certain moment, et 'pressure' est votre mesure de pression.
coef = solve(Time, pressure, lat=latitude)  # Remplacez 'your_latitude' par la latitude de votre site de mesure

# Une fois que vous avez ces coefficients, vous pouvez utiliser 'reconstruct' pour reconstruire le signal de marée :

tide = reconstruct(Time, coef)

# Et enfin, vous pouvez soustraire ce signal de marée de vos données originales pour obtenir une série de pression sans marée :
pressure_without_tide = pressure - tide['h']
pressure_without_tide = pd.Series(pressure_without_tide, name="pressure_without_tide_Utide")
print(pressure_without_tide)

pressure_without_tide_HighPass = high_pass_filter(pressure, "Sea pressure", cutoff, fe_ADCP)
pressure_without_tide_HighPass = pd.Series(pressure_without_tide_HighPass, name="pressure_without_tide_HighPass")

plot_dataframe(N, "Pressure sensor (dBar)" ,
                [(Time,pressure,pressure_without_tide, pressure_without_tide_HighPass),
                (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])

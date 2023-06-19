# main.py

import sys
import os
import pandas as pd

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Process_Datas import parameters
from Process_Datas.dict_dataframe_to_organize_data import dict_pressure_dataframe_to_organize_dataframe
from Process_Datas.add_tide_column import add_tide_column
from Process_Datas.add_surface_column import add_surface_column
from Plots_datas.plots_dataframe import plot_dataframe
from Process_Datas.add_surface_correlation_column import add_surface_correlation_column_and_cte_evaluation, check_complex_values
from Process_Datas.add_waves_description_columns import fourier, fourier_windows

N = parameters.N
excel_file_path = parameters.excel_file_path
columns_to_drop = parameters.columns_to_drop

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


df = dict_pressure_dataframe_to_organize_dataframe(excel_file_path, columns_to_drop)
df = df.head(N)

add_tide_column(df, cutoff, fs, order)
add_surface_column(df)
cte_evaluation_wave = add_surface_correlation_column_and_cte_evaluation(df, fs, hbed)
print(df)
print(f"kp(pressure response factor): {cte_evaluation_wave[0]} | h(mean water depth in m) : {cte_evaluation_wave[1]} | k(wave number) : {cte_evaluation_wave[2]}")

#fourier_result = fourier(df['Sea pressure'],fmin,fmax, fsep)
#print(fourier_result)
fourier_windows(df, seconds, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fe_ig, fe_ss)

"""wave_result = fourier_windows(df, hour, fmin, fsep, fmax, fsep)
print(wave_result)"""

print(df)
plot_dataframe(df, N)
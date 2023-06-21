import sys
import os
import pandas as pd
from datetime import timedelta
import numpy as np

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Process_Datas.dict_dataframe_to_organize_data import dict_pressure_dataframe_to_organize_dataframe
from Process_Datas.add_tide_column import add_tide_column
from Process_Datas.add_surface_column import add_surface_column
from Process_Datas.add_surface_correlation_column import add_surface_correlation_column_and_cte_evaluation
from Process_Datas.compute_spectrum import compute_spectrum
from Process_Datas.remove_jump_rows import remove_jump_rows


def process_concatenate_save_dataframe(excel_file_path, columns_to_drop, cutoff, fs, order, hbed, fs_data, fe) :
    df = dict_pressure_dataframe_to_organize_dataframe(excel_file_path, columns_to_drop)
    #df = df.iloc[N:6*N]
    add_tide_column(df, cutoff, fs, order)
    add_surface_column(df)
    cte_evaluation_wave = add_surface_correlation_column_and_cte_evaluation(df, fs, hbed)
    print(f"kp(pressure response factor): {cte_evaluation_wave[0]} | h(mean water depth in m) : {cte_evaluation_wave[1]} | k(wave number) : {cte_evaluation_wave[2]}")
    df = remove_jump_rows(df, "Sea pressure", 0.11, fs_data)
    df = df.reset_index(drop=True)
    
    # Séparer le chemin de base et l'extension
    base_path, extension = os.path.splitext(excel_file_path)

    # Ajouter "_process_data" au chemin de base, puis ajouter l'extension de retour
    new_path = base_path + "_process_data" + ".pkl"
    #fourier_result = fourier(df['Sea pressure'],fmin,fmax, fsep)
    #print(fourier_result)
    #fourier_windows(df, seconds, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fe_ig, fe_ss)

    """wave_result = fourier_windows(df, hour, fmin, fsep, fmax, fsep)
    print(wave_result)"""
    """Temperature = df['Temperature']
    Time = df['Time']
    # Prenez la valeur minimale de 'Time' comme référence
    reference_time = df['Time'].min()
    # Convertissez la colonne 'Time' en secondes depuis la date de référence
    Time_in_seconds = (df['Time'] - reference_time) // pd.Timedelta('1s')

    
    Depth = df['Depth']
    Surface = df['surface']
    Tide = df['tide']
    k0 = df['k0 (deep water number)']

    #Energy_IG = df['energy,IG']
    #Energy_SS = df['energy,SS']"""
    
    df.to_pickle(new_path)
        
    
import sys
import os
import pandas as pd
from scipy.signal import butter,filtfilt
from datetime import timedelta

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Read_Datas.read_semicolon_seperated_csv import read_semicolon_separated_csv
from Process_Datas.remove_jump_rows import remove_jump_rows

def save_adcp_data_process_to_pickle(adcp_file_path, threshold, fs):
    df = read_semicolon_separated_csv(adcp_file_path)
    df = df.loc[:, ['DateTime', 'Temperature', 'Pressure', 'AltimeterPressure', 'AltimeterDistanceAST']]
    df = df.rename(columns={'DateTime': 'Time'})
    df = df.rename(columns={'Pressure': 'Sea pressure'})
    base_path, extension = os.path.splitext(adcp_file_path)
    df['Time'] = df['Time'] - timedelta(hours = 2)
    print(df)
    df = remove_jump_rows(df, df['Sea pressure'], threshold, fs)

    # Ajouter "_process_data" au chemin de base, puis ajouter l'extension de retour
    new_path = base_path + "_process_data" + ".pkl"
    print(df.info())
    print(df)

    df.to_pickle(new_path)
    
    return df
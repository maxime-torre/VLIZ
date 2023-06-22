import sys
import os
import pandas as pd
from scipy.signal import butter,filtfilt
from datetime import timedelta
import pickle

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
    print(df)
    #df = remove_jump_rows(df, df['Sea pressure'], threshold, fs)

    # Ajouter "_process_data" au chemin de base, puis ajouter l'extension de retour
    new_path = base_path + "_process_data" + ".pkl"
    print(df.info())
    print(df)

    df.to_pickle(new_path)
    
    return df

def process_adcp_excel_files(directory_path, threshold, fs, display = True):
    # Initialiser un dictionnaire pour stocker les DataFrame
    dfs = {}

    # Parcourir tous les fichiers dans le répertoire
    for filename in os.listdir(directory_path):
        # Si le fichier est un fichier Excel
        if filename.endswith(".csv"):
            # Construire le chemin complet du fichier
            file_path = os.path.join(directory_path, filename)
            
            # Lire le fichier Excel en DataFrame
            df = read_semicolon_separated_csv(file_path)

            df = df.loc[:, ['DateTime', 'Temperature', 'Pressure', 'AltimeterPressure', 'AltimeterDistanceAST']]
            df = df.rename(columns={'DateTime': 'Time'})
            df = df.rename(columns={'Pressure': 'Sea pressure'})            
            if display :
                print("--------------------------")
                print(f"filename : {filename}")
                print(df)
            #df = remove_jump_rows(df, df['Sea pressure'], threshold, fs)

            # Ajouter le DataFrame au dictionnaire
            dfs[filename] = df

    # Enregistrer le dictionnaire de DataFrame en fichier pickle
    with open(os.path.join(directory_path, "processed_dict_of_data.pkl"), "wb") as f:
        pickle.dump(dfs, f)

    return dfs

def concatenate_dataframes(pickle_path, threshold, fs):
    # Ouvrir le fichier pickle et charger le dictionnaire de DataFrame
    with open(pickle_path, "rb") as f:
        dfs = pickle.load(f)

    # Obtenir une liste des clés du dictionnaire (noms des fichiers) triées
    keys = sorted(dfs.keys())

    # Initialiser une liste pour stocker les DataFrame
    df_list = []

    # Parcourir les clés
    for key in keys:
        # Ajouter le DataFrame à la liste
        df_list.append(dfs[key])

    # Concaténer les DataFrame
    df = pd.concat(df_list)
    df_reset  = df.reset_index(drop=True)
    print(df_reset)
    df_reset = remove_jump_rows(df_reset, df_reset['Sea pressure'], threshold, fs)
    df_reset  = df_reset.reset_index(drop=True)
    print(df_reset)

    # Assurer qu'il n'y a pas de recouvrement ou de perte de données
    # en ré-échantillonnant les données pour qu'elles correspondent à la fréquence d'échantillonnage spécifiée
    #df = df.resample(f'{1/fe}S', on='Time').mean().reset_index()

    # Construire le chemin du nouveau fichier pickle
    base_path, extension = os.path.splitext(pickle_path)
    new_path = base_path + "_all" + extension

    # Enregistrer le DataFrame global en fichier pickle
    df_reset.to_pickle(new_path)

    return df_reset
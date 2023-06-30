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

def merge_data(wave_file, period_file, pickle_name, data_debut, date_end):
    # Chargement des données
    wave_data = pd.read_csv(wave_file, sep="\t")
    period_data = pd.read_csv(period_file, sep="\t")
    
    base_path, extension = os.path.splitext(wave_file)
    new_path = base_path + pickle_name + ".pkl"

    # Renommage des colonnes
    wave_data.columns = ['Time', 'Wave Height']
    period_data.columns = ['Time', 'Average Period']

    # Fusion des deux dataframes
    merged_data = pd.merge(wave_data, period_data, on='Time', how='outer')
    merged_data['Time'] = pd.to_datetime(merged_data['Time'])
    merged_data = merged_data.loc[(merged_data['Time'] >= data_debut)]
    merged_data = merged_data.loc[(merged_data['Time'] < date_end)]
    
    merged_data.to_pickle(new_path)

    return merged_data
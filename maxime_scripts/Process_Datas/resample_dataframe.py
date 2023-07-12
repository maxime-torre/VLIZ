import sys
import os
# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import pandas as pd

def resample_dataframes(df1, df2, freq_df1, freq_df2):
    # Assurer que 'Time' est au format datetime
    df1['Time'] = pd.to_datetime(df1['Time'])
    df2['Time'] = pd.to_datetime(df2['Time'])

    # Convertir les fréquences d'échantillonnage en périodes de temps
    period_df1 = pd.to_timedelta((1/freq_df1)*1000, unit='ms')
    period_df2 = pd.to_timedelta((1/freq_df2)*1000, unit='ms')

    # Déterminer le dataframe avec la plus grande fréquence d'échantillonnage (plus petite période)
    if period_df1 > period_df2:
        df_to_resample = df2.copy()
        target_frequency = str(int(freq_df1)) + 'S'  # convert Hz to string format for resampling
    else:
        df_to_resample = df1.copy()
        target_frequency = str(int(freq_df2)) + 'S'  # convert Hz to string format for resampling

    # Rééchantillonner le dataframe
    df_to_resample.set_index('Time', inplace=True)
    df_resampled = df_to_resample.resample(target_frequency).mean()

    # Réinitialiser l'index
    df_resampled.reset_index(inplace=True)

    # Retourner les dataframes avec la même fréquence d'échantillonnage
    if period_df1 < period_df2:
        return df1, df_resampled
    else:
        return df_resampled, df2
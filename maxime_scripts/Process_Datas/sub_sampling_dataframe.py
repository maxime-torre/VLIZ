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

def resample_dataframe(path, freq='30T'):
    """
    This function reads a dataframe from a pickle file, resamples it with a given frequency, and rearranges the columns so 'Time' is first.

    Parameters:
    path (str): The path to the pickle file.
    freq (str): The frequency for resampling the dataframe. Default is '30T' (30 minutes).

    Returns:
    df (pandas.DataFrame): The resampled dataframe.
    """
    # Read the dataframe
    df = pd.read_pickle(path)
    print(df)

    # Make a copy of the 'Time' column and convert it to datetime
    df['Time'] = pd.to_datetime(df['Time'])
    df['TimeCopy'] = df['Time']

    # Set 'Time' as the dataframe index
    df.set_index('Time', inplace=True)

    # Create a new 'Time' column from the 'TimeCopy' and drop 'TimeCopy'
    df['Time'] = df['TimeCopy']
    df.drop('TimeCopy', axis=1, inplace=True)

    # Resample the dataframe
    df = df.resample(freq).first()

    # Reset the index
    df.reset_index(drop=True, inplace=True)

    # Move 'Time' column to the first position
    cols = list(df.columns)
    cols = ['Time'] + [col for col in cols if col != 'Time']
    df = df[cols]

    return df

def compare_time_columns(df1, df2, time_column='Time'):
    # Assurez-vous que les colonnes sont de type datetime
    df1[time_column] = pd.to_datetime(df1[time_column])
    df2[time_column] = pd.to_datetime(df2[time_column])
    
    # Fusionnez les deux dataframes sur la colonne 'Time'
    merged_df = pd.merge(df1, df2, on=time_column, how='outer')
    
    # Triez le dataframe fusionné par 'Time'
    merged_df.sort_values(by=time_column, inplace=True)
    
    # Utilisez l'interpolation pour remplir les valeurs manquantes
    merged_df.interpolate(inplace=True)
    
    # Séparez les dataframes
    df1_filled = merged_df[df1.columns]
    df2_filled = merged_df[df2.columns]
    
    return df1_filled, df2_filled

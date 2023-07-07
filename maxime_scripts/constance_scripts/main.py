# main.py

import sys
import os
import pandas as pd
import numpy as np

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from read_semicolon_separated_csv import read_semicolon_separated_csv
from Read_Datas.read_pickle_to_df import read_pickle_to_df
from Plots_datas.plots_dataframe import plot_dataframe
from constance_scripts import parameters

csv_file = parameters.csv_file
pickle_file = parameters.pickle_file
pickle_file_mean_daily = parameters.pickle_file_mean_daily

df = read_pickle_to_df(pickle_file)
print("df without daily mean")
# Assurez-vous que 'Datetime' et 'Date' sont dans le bon format datetime
"""df['Datetime'] = pd.to_datetime(df['Datetime'])
df['Date'] = pd.to_datetime(df['Date'])

# Mettez à jour les valeurs NaT dans 'Datetime' avec la valeur correspondante de 'Date'
df.loc[df['Datetime'].isna(), 'Datetime'] = df['Date']

# Si vous voulez que les dates sans heure aient 00:00:00 comme heure, vous pouvez le faire comme ça :
df.loc[df['Datetime'].dt.time == pd.to_datetime('00:00:00').time(), 'Datetime'] = df['Datetime'].dt.date.astype(str) + ' 00:00:00'
df['Datetime'] = pd.to_datetime(df['Datetime'])"""
print(df)

df_pressure = df['Pressure, db']
df_pressure = pd.Series(df_pressure, name="df_pressure")



plot_dataframe(len(df), "Pressure dBar", 
               [(df['Datetime'],df_pressure),
                    (df['Datetime'].min(),df['Datetime'].max())])

#-----------------------------------------


na_rows = df[df['Datetime'].isna()]
print(na_rows)


daily_means = read_pickle_to_df(pickle_file_mean_daily)
# Convert 'Date' to datetime if not already
daily_means['Date'] = daily_means['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
print("df with daily mean")
print(daily_means)


"""df_pressure = df['Pressure, db']
df_pressure = pd.Series(df_pressure, name="df_pressure")
df_mean_daily_pressure = daily_means['Pressure, db']
df_mean_daily_pressure = pd.Series(df_mean_daily_pressure, name="df_mean_daily_pressure")"""


"""plot_dataframe(len(df), "Pressure dBar", 
               [(df['Datetime'],df_pressure, df_mean_daily_pressure),
                    (df['Datetime'].min(),df['Datetime'].max())])"""

"""df = read_semicolon_separated_csv(csv_file)
print(df)
# Convert 'Datetime' to string type
df['Datetime'] = df['Datetime'].astype(str)

# Combining 'Datetime' and 'Time' for rows where 'Time' is not NaN
mask = ~df['Time'].isna()
df.loc[mask, 'Datetime'] = pd.to_datetime(df[mask]['Datetime'] + ' ' + df[mask]['Time'])

# Converting 'Datetime' to datetime format for the rest
df.loc[~mask, 'Datetime'] = pd.to_datetime(df[~mask]['Datetime'])

# Replace "00:00:00" with np.nan
df['Datetime'] = df['Datetime'].apply(lambda x: np.nan if x.time() == pd.Timestamp("00:00:00").time() else x)
df.to_pickle(pickle_file)
print(df)
"""
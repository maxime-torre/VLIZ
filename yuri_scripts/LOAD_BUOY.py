# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 09:47:56 2023

@author: yuri.pepi
"""
import pandas as pd
from datetime import datetime

folder_path = "C:/Users/yuri.pepi/Desktop/Yuri/IG WAVES/SCRIPT/vlaamse_banken/"

# A function to resample the data to a 3-hour interval
def resampling(buoy):
    buoy_3hrs = buoy.resample('3H', on='time', closed='right').mean().reset_index()
    return buoy_3hrs

# A function to process the buoy data
def process_data(file_Hm, file_dirlow=None, file_dirhigh=None):
    # Load the Hm data
    Hm = pd.read_table(folder_path + file_Hm)
    data = Hm.copy()
    headers = ["time", "Hm"]
    data.columns = headers

    # Convert datetime to Python datetime format
    for idx, row in data.iterrows():
        data.loc[idx, "time"] = datetime.fromisoformat(row["time"][0:-6])

    # Unify dataset
    data["Hm"] = Hm.iloc[:, 1] / 100  # convert in meter
 
    # If direction data is provided, add it to the dataset
    if file_dirlow is not None and file_dirhigh is not None:
        dirlow = pd.read_table(folder_path + file_dirlow)
        dirhigh = pd.read_table(folder_path + file_dirhigh)

        data["dirlow"] = dirlow.iloc[:, 1]
        data["dirhigh"] = dirhigh.iloc[:, 1]

    # Resample the data to a 3-hour interval
    data = resampling(data)
    return data

# Process data for four buoys: Trapegeer, Nieuwport, Westhinder, Kwintebank
trap = process_data('TRG.GHA_001_TRGDG0HM0030.txt')
nieu = process_data('NPB.GHA_001_NPTDG0HM0030.txt')
west = process_data("WHI.GHA_001_WHIDW0HM0030.txt", 'WHI.RLF_001_WHIDW0RLF030.txt', 'WHI.RHF_001_WHIDW0RHF030.txt')
kwin = process_data("KWI.GHA_001_KWIDW0HM0030.txt", 'KWI.RLF_001_KWIDW0RLF030.txt', 'KWI.RHF_001_KWIDW0RHF030.txt')
rave1 = process_data("RA1.GHA_001_RA1DW0HM0030.txt", 'RA1.RLF_001_RA1DW0RLF030.txt', 'RA1.RHF_001_RA1DW0RHF030.txt')
rave2 = process_data("RA2.GHA_001_RA2DW0HM0030.txt", 'RA2.RLF_001_RA2DW0RLF030.txt', 'RA2.RHF_001_RA2DW0RHF030.txt')

# Save the processed data as a list of objects using Pickle 
f = open('BUOY_ALL.pckl', 'wb')
pickle.dump([trap, nieu, west, kwin, rave1, rave2], f)
f.close()


















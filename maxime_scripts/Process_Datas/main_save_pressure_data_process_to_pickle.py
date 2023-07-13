import sys
import os
import pandas as pd
import math
import numpy as np
from matplotlib.pyplot import *
from numpy.fft import fft 
from datetime import timedelta

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import parameters
from Process_Datas.process_concatenate_save_dataframe import process_concatenate_save_dataframe

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
seconds = parameters.seconds
fe=parameters.fe
cutoff_low_pass = parameters.cutoff_low_pass
fs_data = parameters.fs_data
date_debut = parameters.date_debut
date_end_exclu = parameters.date_end_exclu


df = process_concatenate_save_dataframe(excel_file_path, columns_to_drop, cutoff, fs, order, hbed, fs_data, fe, date_debut, date_end_exclu)
print(df)
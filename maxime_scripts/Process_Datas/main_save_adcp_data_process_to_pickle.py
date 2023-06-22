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

from Process_Datas.save_adcp_data_process_to_pickle import save_adcp_data_process_to_pickle, process_adcp_excel_files, concatenate_dataframes
from Process_Datas import parameters
from Plots_datas.plots_dataframe import plot_dataframe_columns
from Read_Datas.read_semicolon_seperated_csv import read_semicolon_separated_csv

adcp_file_path = parameters.adcp_file_path
threshold = parameters.threshold
fs = parameters.fs
directory_path = parameters.directory_path
N = parameters.N
pickle_dict_of_data_path = parameters.pickle_dict_of_data_path
fs_data_adcp_all = parameters.fs_data_adcp_all

#df = save_adcp_data_process_to_pickle(adcp_file_path, threshold, fs)

#dfs = process_adcp_excel_files(directory_path,threshold, fs)

concatenate_dataframes(pickle_dict_of_data_path, threshold, fs_data_adcp_all)


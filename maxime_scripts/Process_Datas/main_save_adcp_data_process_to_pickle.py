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

from Process_Datas.save_adcp_data_process_to_pickle import save_adcp_data_process_to_pickle
from Process_Datas import parameters

adcp_file_path = parameters.adcp_file_path
threshold = parameters.threshold
fs = parameters.fs

df = save_adcp_data_process_to_pickle(adcp_file_path, threshold, fs)


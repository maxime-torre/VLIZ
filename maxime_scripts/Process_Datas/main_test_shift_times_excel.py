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

from Process_Datas.shift_times_excel import shift_times_excel

excel_PS_before_time_shift = parameters.excel_PS_before_time_shift
date_debut = parameters.date_debut
date_end_exclu = parameters;date_end_exclu

df = shift_times_excel(excel_PS_before_time_shift, date_debut, date_end_exclu)
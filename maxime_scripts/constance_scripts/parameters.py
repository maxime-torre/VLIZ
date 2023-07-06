# parameters.py

import sys
import os
import pandas as pd

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

csv_file = "C:\\Users\\maxixme.torre\\Documents\\20220901-PS2201_test_RBR\\maxime_scripts\\constance_scripts\\Greenland_mooring.csv"
pickle_file = "C:\\Users\maxixme.torre\\Documents\\20220901-PS2201_test_RBR\\maxime_scripts\\constance_scripts\\Greenland_mooring.pickle"
pickle_file_mean_daily = "C:\\Users\maxixme.torre\\Documents\\20220901-PS2201_test_RBR\\maxime_scripts\\constance_scripts\\Greenland_mooring_mean_daily.pickle"
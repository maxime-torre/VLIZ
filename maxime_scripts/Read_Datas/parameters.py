# parameters.py

import sys
import os

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

excel_file_path = 'C:\\Users\\maxixme.torre\\Documents\\20220901-PS2201_test_RBR\\Datas\\PRESSURE SENSOR\\210961_20220902_1748.xlsx'
adcp_path_file = "C:\\Users\\maxixme.torre\\Documents\\20220901-PS2201_test_RBR\\Datas\\ADCP\\S102377A024_Test_RBR_Q3B0_1.csv"

pickle_path_file_ADCP = "C:\\Users\\maxixme.torre\\Documents\\20220901-PS2201_test_RBR\\Datas\\ADCP\\S102377A024_Test_RBR_Q3B0_1_process_data.pkl"
pickle_path_file_Pressure_sensor = "C:\\Users\\maxixme.torre\\Documents\\20220901-PS2201_test_RBR\\Datas\\PRESSURE SENSOR\\210961_20220902_1748_process_data.pkl"

N = 1000 
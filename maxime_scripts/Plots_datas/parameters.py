# parameters.py

import sys
import os

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

excel_file_path = 'C:\\Users\\maxixme.torre\\Documents\\20220901-PS2201_test_RBR\\Datas\\PRESSURE SENSOR\\210961_20220902_1748.xlsx'
adcp_A = "C:\\Users\\maxixme.torre\\Documents\\20220901-PS2201_test_RBR\\Datas\\ADCP\\S102377A024_Test_RBR_Q3A0_1.csv"
adcp_B = "C:\\Users\\maxixme.torre\\Documents\\20220901-PS2201_test_RBR\\Datas\\ADCP\\S102377A024_Test_RBR_Q3B0_1.csv"

pickle_path_file_ADCP_trapergeer_2023 = "C:\\Users\\maxixme.torre\\Documents\\Infra_gravity_waves_datas\\Trapegeer_8Feb_10Apr_2023_ADCP_PS_BUOYS\\ADCP\\All_ADCP_processed_data_8Feb_10Apr.pkl"
pickle_path_file_Pressure_sensor_trapergeer_2023 = "C:\\Users\\maxixme.torre\\Documents\\Infra_gravity_waves_datas\\Trapegeer_8Feb_10Apr_2023_ADCP_PS_BUOYS\\PS\\All_PS_processed_data_8Feb_10Apr.pkl"

pickle_path_file_ADCP_test_september_2022 = "C:\\Users\\maxixme.torre\\Documents\\20220901-PS2201_test_RBR\\Datas\\ADCP\\S102377A024_Test_RBR_Q3B0_1_process_data.pkl"
pickle_path_file_Pressure_sensor_test_september_2022 = "C:\\Users\\maxixme.torre\\Documents\\20220901-PS2201_test_RBR\\Datas\\PRESSURE SENSOR\\210961_20220902_1748_process_data.pkl"
N = 1200000

cutoff = 1/(60*10)
fe_ADCP = 2
fe_PS = 4
samples_cutoff_filter = fe_ADCP*60*60*4 #suppression des échantillons des 2 premieres heures
fmin_ig = 1/(5*60)
fmax_ig = 1/16.87 # Minimum frequency
fmin_ss = fmax_ig
fmax_ss = 1
hour = 28
seconds = 20
hbed = 0.3
latitude = 52.115950
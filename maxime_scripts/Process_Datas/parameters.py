# parameters.py

import sys
import os

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

excel_file_path = 'C:\\Users\\maxixme.torre\\Documents\\20220901-PS2201_test_RBR\\Datas\\PRESSURE SENSOR\\210961_20220902_1748.xlsx' 
columns_to_drop = ['BPR temperature', 'BPR pressure', 'Period', 'Period.1']
adcp_file_path = "C:\\Users\\maxixme.torre\\Documents\\20220901-PS2201_test_RBR\\Datas\\ADCP\\S102377A024_Test_RBR_Q3B0_1.csv"
directory_path = "C:\\Users\\maxixme.torre\\Documents\\Infra_gravity_waves_datas\\Adcp_sensor\\Trapegeer"
pickle_dict_of_data_path = "C:\\Users\\maxixme.torre\\Documents\\Infra_gravity_waves_datas\\Adcp_sensor\\Trapegeer\\processed_dict_of_data.pkl"
pickle_all_adcp_data_path = "C:\\Users\\maxixme.torre\\Documents\\Infra_gravity_waves_datas\\Adcp_sensor\\Trapegeer\\processed_dict_of_data_all.pkl"

N = 10000

#-------------- butter_lowpass_filter | parameters --------------#
fs = 2
dt = 1/fs
cutoff = 1/300
order = 2

hbed = 0.3 # Sensor height from bed (m)

#-------------- bfourier transform | parameters --------------#
#fsep = 1/16.87 
# fsep = 1/500
fmin_ig = 1/(5*60)
fmax_ig = 1/30 # Minimum frequency
fe_ig = 1/10
fmin_ss = 1/30
fmax_ss = 1
fe_ss = 3
fsep = 1/30 # Separation frequency
hour = 3 # Window size in hours
minutes = 2
seconds = 60
fe = 1/10
fs_data = 2
fs_data_adcp_all = 4
cutoff_low_pass = 0.1

threshold = 0.1
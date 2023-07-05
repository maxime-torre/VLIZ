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

all_pickle_path_file_ADCP = "C:\\Users\\maxixme.torre\\Documents\\Infra_gravity_waves_datas\\Pressure_sensor\\210961_20230417_0929_v2_process_data.pkl"
all_csv_path_file_PS = "C:\\Users\\maxixme.torre\\Documents\\Infra_gravity_waves_datas\\Pressure_sensor\\210961_20230417_0929_v2.xlsx"
all_pickle_path_file_PS = "C:\\Users\\maxixme.torre\\Documents\\Infra_gravity_waves_datas\\Pressure_sensor\\210961_20230417_0929_v2_process_data.pkl"

pickle_dict_of_data_path = "C:\\Users\\maxixme.torre\\Documents\\Infra_gravity_waves_datas\\Adcp_sensor\\Trapegeer\\processed_dict_of_data.pkl"
pickle_all_adcp_data_path = "C:\\Users\\maxixme.torre\\Documents\\Infra_gravity_waves_datas\\Adcp_sensor\\Trapegeer\\processed_dict_of_data_all.pkl"

Trapergeer_wave_height_text_file = "C:\\Users\\maxixme.torre\\Documents\\Infra_gravity_waves_datas\\Trapegeer_8Feb_10Apr_2023_ADCP_PS_BUOYS\\BUOYS\\TRG.GHA_001_TRGDG0HM0030.txt"
Trapergeer_wave_period_text_file = "C:\\Users\\maxixme.torre\\Documents\\Infra_gravity_waves_datas\\Trapegeer_8Feb_10Apr_2023_ADCP_PS_BUOYS\\BUOYS\\TRG.GTZ_001_TRGDG0GTZ030.txt"

save_data_ADCP_path = "C:\\Users\\maxixme.torre\\Documents\\Infra_gravity_waves_datas\\Trapegeer_8Feb_10Apr_2023_ADCP_PS_BUOYS\\ADCP\\All_ADCP_processed_daata_wave_informations.pkl"


N = 2000000
fs = 2
threshold = 0.1
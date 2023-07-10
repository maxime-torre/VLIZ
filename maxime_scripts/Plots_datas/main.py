# main.py
import sys
import os
import pandas as pd
from datetime import timedelta
from scipy import stats

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Plots_datas import parameters
from Plots_datas.plots_dataframe import plot_dataframe_dict, plot_dataframe, plot_dataframe_columns, plot_with_linear_regression
from Read_Datas.read_excel_sheets_to_dfs import read_excel_sheets_to_dfs
from Read_Datas.read_pickle_to_df import read_pickle_to_df
from Read_Datas.read_datas_sheet_to_dfs_only import read_excel_sheets_xlsx, read_excel_sheets_csv
from Read_Datas.read_semicolon_seperated_csv import read_semicolon_separated_csv
from Plots_datas.plot_pressure_data_comparaison import plot_pressure_data_comparaison
from Process_Datas.add_waves_description_columns import depth_to_pressure, pressure_from_depth_hydraustatique_and_dynamique, pressure_to_depth
from Process_Datas.butter_lowpass_filter import low_pass_filter
  
pickle_path_file_ADCP_trapergeer_2023  = parameters.pickle_path_file_ADCP_trapergeer_2023
pickle_path_file_Pressure_sensor_trapergeer_2023  = parameters.pickle_path_file_Pressure_sensor_trapergeer_2023

pickle_path_file_ADCP_test_september_2022 = parameters.pickle_path_file_ADCP_test_september_2022
pickle_path_file_Pressure_sensor_test_september_2022= parameters.pickle_path_file_Pressure_sensor_test_september_2022

N = parameters.N
cutoff = parameters.cutoff
fe_ADCP = parameters.fe_ADCP
fe_PS = parameters.fe_PS
samples_cutoff_filter = parameters.samples_cutoff_filter
fmin_ig = parameters.fmin_ig
fmax_ig = parameters.fmax_ig
fmin_ss = parameters.fmin_ss
fmax_ss = parameters.fmax_ss
hour = parameters.hour
seconds = parameters.seconds
hbed = parameters.hbed

df_ADCP = read_pickle_to_df(pickle_path_file_ADCP_test_september_2022)
df_ADCP = df_ADCP.head(N)
df_tide_ADCP = low_pass_filter(df_ADCP['AltimeterDistanceAST'], "AltimeterDistanceAST", cutoff, fe_ADCP)
Time_ADCP = df_ADCP.Time

df_PS= read_pickle_to_df(pickle_path_file_Pressure_sensor_test_september_2022)
df_PS = df_PS.head(N)
Time_PS = df_PS.Time

if Time_ADCP.equals(Time_PS):
    print("Time_ADCP et Time_PS are equals")
else:
    print(f"Time_ADCP et Time_PS are not equals")

    # Find the common time interval
    common_start = max(Time_ADCP.min(), Time_PS.min())
    common_end = min(Time_ADCP.max(), Time_PS.max())

    # Slice the time series to the common interval
    Time_ADCP = Time_ADCP[(Time_ADCP >= common_start) & (Time_ADCP <= common_end)]
    Time_PS = Time_PS[(Time_PS >= common_start) & (Time_PS <= common_end)]
    
    # Remove the rows of df_ADCP that are not in the common interval and reindex
    df_ADCP = df_ADCP[(df_ADCP['Time'] >= common_start) & (df_ADCP['Time'] <= common_end)]
    df_ADCP = df_ADCP.reset_index(drop=True)
    
    # Remove the rows of df_PS that are not in the common interval and reindex
    df_PS = df_PS[(df_PS['Time'] >= common_start) & (df_PS['Time'] <= common_end)]
    df_PS = df_PS.reset_index(drop=True)
    
    Time = Time_PS
    
print(df_ADCP)
print(df_PS)

"""plot_pressure_data_comparaison(pickle_path_file_ADCP_test_september_2022, 
                            pickle_path_file_Pressure_sensor_test_september_2022, 
                            N, 
                            cutoff, 
                            fe_ADCP, 
                            fe_PS, 
                            samples_cutoff_filter,
                            fmin_ig,
                            fmax_ig,
                            fmin_ss,
                            fmax_ss)"""

P_linear_theory = depth_to_pressure(df_ADCP['AltimeterDistanceAST'], df_tide_ADCP, fe_ADCP)
P_linear_theory = pd.Series(P_linear_theory, name="P_linear_theory_from_ADCP")
print(f"len(Eta) : {len(P_linear_theory)}")
print(f"len(Time) : {len(Time)}")
print(P_linear_theory)
Sea_pressure_PS = df_PS['Sea pressure']
Sea_pressure_PS = pd.Series(Sea_pressure_PS, name="Sea_Pressure_from_PS")

rolling_P_linear_theory = P_linear_theory.rolling(window=10).mean()
rolling_P_linear_theory = pd.Series(rolling_P_linear_theory, name="Rolling_P_linear_theory_from_ADCP")


"""P_total = pressure_from_depth_hydraustatique_and_dynamique(df_ADCP['AltimeterPressure'], df_tide_ADCP, fe_ADCP, hbed)
P_total = pd.Series(P_total, name="P_total")"""

#Sea Pressure PS centred shifted vs AST pressure from ADCP (signal)
plot_dataframe(N, "AltimeterPressure (dBar) vs DistanceAST (m)" ,
                [(Time,df_ADCP['AltimeterPressure'], df_ADCP['AltimeterDistanceAST']),
                (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])

Estimation_depth_ADCP = pressure_to_depth(df_ADCP['AltimeterPressure'],df_tide_ADCP, fe_ADCP )
Estimation_depth_ADCP = pd.Series(Estimation_depth_ADCP, name="Estimation_depth_ADCP")
slope, intercept, r_value, p_value, std_err = stats.linregress(Estimation_depth_ADCP, df_ADCP['AltimeterDistanceAST'])
line = slope*Estimation_depth_ADCP+intercept

#Sea Pressure PS centred shifted vs AST pressure from ADCP (signal)
"""plot_dataframe(N, "Surface elevation (m) before correction" ,
                [(Time, df_ADCP['AltimeterDistanceAST'],Estimation_depth_ADCP),
                (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])

plot_with_linear_regression(Estimation_depth_ADCP,df_ADCP['AltimeterDistanceAST'], "AltimeterDistanceAST (ADCP) vs Elevation estimation from AltimeterPressure (ADCP)")

plot_dataframe(N, "Surface elevation (m) after correction" ,
                [(Time, df_ADCP['AltimeterDistanceAST'], Estimation_depth_ADCP*slope + intercept),
                (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])
"""

Amplitude_difference = df_ADCP['AltimeterDistanceAST'] -(Estimation_depth_ADCP*slope + intercept)
Amplitude_difference = pd.Series(Amplitude_difference, name="Amplitude_difference")

plot_dataframe(N, "Surface elevation (m) after correction" ,
                [(Amplitude_difference, Estimation_depth_ADCP),
                (Amplitude_difference.min(),Amplitude_difference.max())])
"""plot_dataframe(N, "Pressure (dBar)" ,
                [(Time,P_linear_theory,df_ADCP['AltimeterPressure'], rolling_P_linear_theory),
                (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])"""

"""df = read_semicolon_separated_csv(adcp_B)
df = df.loc[:, ['DateTime', 'Temperature', 'Pressure', 'AltimeterPressure', 'AltimeterDistanceAST']]
df = df.rename(columns={'DateTime': 'Time'})
df = df.rename(columns={'Pressure': 'Sea pressure'})
base_path, extension = os.path.splitext(adcp_B)

# Ajouter "_process_data" au chemin de base, puis ajouter l'extension de retour
new_path = base_path + "_process_data" + ".pkl"
print(df.info())
print(df)

df.to_pickle(new_path)"""


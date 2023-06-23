import sys
import os
import pandas as pd

from matplotlib.pyplot import *
from datetime import timedelta

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Plots_datas.plots_dataframe import plot_dataframe
from Process_Datas.compute_spectrum import compute_spectrum
from Process_Datas.butter_lowpass_filter import butter_bandpass_filter
from Read_Datas.read_pickle_to_df import read_pickle_to_df
from Process_Datas.add_waves_description_columns import fourier_windows
from tqdm import tqdm


def plot_process_data_wave_analysis(pickle_path_file_ADCP, pickle_path_file_Pressure_sensor, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fs_data, fe, N, seconds, fe_ig, fe_ss):
    """base_path, extension = os.path.splitext(excel_file_path)

    # Ajouter "_process_data" au chemin de base, puis ajouter l'extension de retour
    new_path = base_path + "_process_data" + ".pkl"
    print(new_path)"""
    df_ADCP = read_pickle_to_df(pickle_path_file_ADCP)
    df_ADCP = df_ADCP.head(N)
    df_ADCP['Time'] = df_ADCP['Time'].dt.floor('S')
    df_ADCP_init = df_ADCP.copy()
    #subset_ADCP = df_ADCP.iloc[8991:9011]
    #print(subset_ADCP)
    
    df_PS = read_pickle_to_df(pickle_path_file_Pressure_sensor) #PS for Pressure Sensor (RBR file)
    df_PS = df_PS.head(N)
    df_PS['Time'] = df_PS['Time'].dt.floor('S')
    df_PS_init = df_PS.copy()
    #subset_PS = df_PS.iloc[8991:9011]
    #print(subset_PS)
    
    Time_ADCP = df_ADCP['Time']
    Time_PS = df_PS['Time']
    Time = Time_ADCP
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
        
        #try to fix the bound of time
        """start_time = '2022-09-01 10:48:26'
        end_time = '2022-09-01 10:48:28'
        subset_df = df_ADCP_init[(df_ADCP_init['Time'] >= start_time) & (df_ADCP_init['Time'] <= end_time)]
        print(subset_df)
        subset_PS = df_PS_init.iloc[8991:9011]
        print(subset_PS)"""

        # Now you can use Time_ADCP or Time_PS for Time, they have the same interval
        Time = Time_ADCP

    #ADCP Sea pressure : IG signal and SS signal
    ADCP_sea_pressure_bandpass_filtred_signal_ig = butter_bandpass_filter(df_ADCP['Sea pressure'], fmin_ig, fmax_ig, fs_data)
    ADCP_sea_pressure_bandpass_filtred_signal_ig = ADCP_sea_pressure_bandpass_filtred_signal_ig - ADCP_sea_pressure_bandpass_filtred_signal_ig.mean()
    ADCP_sea_pressure_bandpass_filtred_signal_ig = pd.Series(ADCP_sea_pressure_bandpass_filtred_signal_ig, name=f'ADCP Sea pressure - IG bandpass filtred')

    ADCP_sea_pressure_bandpass_filtred_signal_ss = butter_bandpass_filter(df_ADCP['Sea pressure'], fmin_ss, fmax_ss, fs_data)
    ADCP_sea_pressure_bandpass_filtred_signal_ss = ADCP_sea_pressure_bandpass_filtred_signal_ss - ADCP_sea_pressure_bandpass_filtred_signal_ss.mean()
    ADCP_sea_pressure_bandpass_filtred_signal_ss = pd.Series(ADCP_sea_pressure_bandpass_filtred_signal_ss, name=f'ADCP Sea pressure - SS bandpass filtred')
    
    #ADCP AltimeterPressure : IG signal and SS signal
    ADCP_altimeter_pressure_bandpass_filtred_signal_ig = butter_bandpass_filter(df_ADCP['AltimeterPressure'], fmin_ig, fmax_ig, fs_data)
    ADCP_altimeter_pressure_bandpass_filtred_signal_ig = ADCP_altimeter_pressure_bandpass_filtred_signal_ig - ADCP_altimeter_pressure_bandpass_filtred_signal_ig.mean()
    ADCP_altimeter_pressure_bandpass_filtred_signal_ig = pd.Series(ADCP_altimeter_pressure_bandpass_filtred_signal_ig, name=f'ADCP Altimeter pressure - IG bandpass filtred')

    ADCP_altimeter_pressure_bandpass_filtred_signal_ss = butter_bandpass_filter(df_ADCP['AltimeterPressure'], fmin_ss, fmax_ss, fs_data)
    ADCP_altimeter_pressure_bandpass_filtred_signal_ss = ADCP_altimeter_pressure_bandpass_filtred_signal_ss - ADCP_altimeter_pressure_bandpass_filtred_signal_ss.mean()
    ADCP_altimeter_pressure_bandpass_filtred_signal_ss = pd.Series(ADCP_altimeter_pressure_bandpass_filtred_signal_ss, name=f'ADCP Altimeter pressure - SS bandpass filtred')
    
    #Pressure sensor : IG signal and SS signal
    ADCP_pressure_sensor_bandpass_filtred_signal_ig = butter_bandpass_filter(df_PS['Sea pressure'], fmin_ig, fmax_ig, fs_data)
    ADCP_pressure_sensor_bandpass_filtred_signal_ig = ADCP_pressure_sensor_bandpass_filtred_signal_ig - ADCP_pressure_sensor_bandpass_filtred_signal_ig.mean()
    ADCP_pressure_sensor_bandpass_filtred_signal_ig = pd.Series(ADCP_pressure_sensor_bandpass_filtred_signal_ig, name=f'Pressure sensor - IG bandpass filtred')

    ADCP_pressure_sensor_bandpass_filtred_signal_ss = butter_bandpass_filter(df_PS['Sea pressure'], fmin_ss, fmax_ss, fs_data)
    ADCP_pressure_sensor_bandpass_filtred_signal_ss = ADCP_pressure_sensor_bandpass_filtred_signal_ss - ADCP_pressure_sensor_bandpass_filtred_signal_ss.mean()
    ADCP_pressure_sensor_bandpass_filtred_signal_ss = pd.Series(ADCP_pressure_sensor_bandpass_filtred_signal_ss, name=f'Pressure sensor - SS bandpass filtred')
    
    
    Temperature_ADCP = df_ADCP['Temperature']
    Temperature_ADCP = pd.Series(Temperature_ADCP, name="Temperature_ADCP")
    Temperature_PS = df_PS['Temperature']
    Temperature_PS = pd.Series(Temperature_PS, name="Temperature_PS")

    Sea_pressure_ADCP = df_ADCP['Sea pressure']
    Sea_pressure_ADCP = pd.Series(Sea_pressure_ADCP, name="Sea_pressure_ADCP")
    Altimeter_pressure = df_ADCP['AltimeterPressure']
    Altimeter_pressure = pd.Series(Altimeter_pressure, name="Altimeter_pressure")
    Sea_pressure_PS = df_PS['Sea pressure']
    Sea_pressure_PS = pd.Series(Sea_pressure_PS, name="Sea_pressure_PS")
    
    Depth_ADCP = df_ADCP['AltimeterDistanceAST']
    Depth_ADCP = pd.Series(Depth_ADCP, name="Depth_ADCP")
    Depth_PS = df_PS['Depth']
    Depth_PS = pd.Series(Depth_PS, name="Depth_PS")
    
    df_signal_ADCP_Sea_pressure_name = "Sea pressure"
    df_signal_ADCP_Altimeter_pressure_name = "Sea pressure"
    df_signal_PS_Sea_pressure_name = "Sea pressure"

    """mean_tide = df['tide'].mean()
    print(f"mean_tide : {mean_tide} m")
    Depth = df['Depth']
    Surface = df['surface']
    Tide = df['tide']
    k0 = df['k0 (deep water number)']"""

    df_signal_ADCP_Sea_pressure = fourier_windows(df_ADCP, df_signal_ADCP_Sea_pressure_name, seconds, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fe_ig, fe_ss)
    print("--------------------df_signal_ADCP_Sea_pressure-------------------------")
    print(df_signal_ADCP_Sea_pressure)
    df_signal_ADCP_Altimeter_pressure = fourier_windows(df_ADCP, df_signal_ADCP_Altimeter_pressure_name, seconds, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fe_ig, fe_ss)
    print("---------------------df_signal_ADCP_Sea_pressure------------------------")
    print(df_signal_ADCP_Altimeter_pressure)
    df_signal_PS_Sea_pressure = fourier_windows(df_PS, df_signal_PS_Sea_pressure_name, seconds, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fe_ig, fe_ss)
    print("-------------------df_signal_PS_Sea_pressure--------------------------")
    print(df_signal_PS_Sea_pressure)
    
    spectre_dB_ADCP_Sea_pressure, freqs = compute_spectrum(df_ADCP, df_signal_ADCP_Sea_pressure_name, fe)
    spectre_dB_ADCP_Sea_pressure = pd.Series(spectre_dB_ADCP_Sea_pressure, name="spectre_dB_ADCP_Sea_pressure")
    spectre_dB_ADCP_Altimeter_pressure, freqs = compute_spectrum(df_ADCP, df_signal_ADCP_Altimeter_pressure_name, fe)
    spectre_dB_ADCP_Altimeter_pressure = pd.Series(spectre_dB_ADCP_Altimeter_pressure, name="spectre_dB_ADCP_Altimeter_pressure")
    spectre_dB_PS_Sea_pressure, freqs = compute_spectrum(df_PS, df_signal_PS_Sea_pressure_name, fe)
    spectre_dB_PS_Sea_pressure = pd.Series(spectre_dB_PS_Sea_pressure, name="spectre_dB_PS_Sea_pressure")

    Hm0_IG_Sea_pressure = df_signal_ADCP_Sea_pressure['Hm0,IG']
    Hm0_IG_Sea_pressure = pd.Series(Hm0_IG_Sea_pressure, name="Hm0_IG_Sea_pressure")
    Hm0_SS_Sea_pressure  = df_signal_ADCP_Sea_pressure['Hm0,SS']
    Hm0_SS_Sea_pressure = pd.Series(Hm0_SS_Sea_pressure, name="Hm0_SS_Sea_pressure")
    Hm0_total_Sea_pressure  = df_signal_ADCP_Sea_pressure['Hm0,total']
    Hm0_total_Sea_pressure = pd.Series(Hm0_total_Sea_pressure, name="Hm0_total_Sea_pressure")
    
    Hm0_IG_Altimeter_pressure = df_signal_ADCP_Altimeter_pressure['Hm0,IG']
    Hm0_IG_Altimeter_pressure = pd.Series(Hm0_IG_Altimeter_pressure, name="Hm0_IG_Altimeter_pressure")
    Hm0_SS_Altimeter_pressure = df_signal_ADCP_Altimeter_pressure['Hm0,SS']
    Hm0_SS_Altimeter_pressure = pd.Series(Hm0_SS_Altimeter_pressure, name="Hm0_SS_Altimeter_pressure")
    Hm0_total_Altimeter_pressure = df_signal_ADCP_Altimeter_pressure['Hm0,total']
    Hm0_total_Altimeter_pressure = pd.Series(Hm0_total_Altimeter_pressure, name="Hm0_total_Altimeter_pressure")
    
    Hm0_IG_PS_Sea_pressure = df_signal_PS_Sea_pressure['Hm0,IG']
    Hm0_IG_PS_Sea_pressure = pd.Series(Hm0_IG_PS_Sea_pressure, name="Hm0_IG_PS_Sea_pressure")
    Hm0_SS_PS_Sea_pressure = df_signal_PS_Sea_pressure['Hm0,SS']
    Hm0_SS_PS_Sea_pressure = pd.Series(Hm0_SS_PS_Sea_pressure, name="Hm0_SS_PS_Sea_pressure")
    Hm0_total_PS_Sea_pressure = df_signal_PS_Sea_pressure['Hm0,total']
    Hm0_total_PS_Sea_pressure = pd.Series(Hm0_total_PS_Sea_pressure, name="Hm0_total_PS_Sea_pressure")
    
    """frequency_IG = df['frequency,IG']
    frequency_SS = df['frequency,SS']
    energy_IG = df['energy,IG']
    energy_SS = df['energy,SS']"""
    
    #Temperature
    plot_dataframe(N, 
                   [(Time,Temperature_ADCP,Temperature_PS),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])
    
    #Pressure (signal)
    plot_dataframe(N, 
                   [(Time,Sea_pressure_ADCP,Altimeter_pressure,Sea_pressure_PS),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])
    
    #Depth
    plot_dataframe(N, 
                   [(Time,Depth_ADCP,Depth_PS),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])
    
    #Spetre (Amplitude in dB)
    plot_dataframe(N, 
                   [(freqs,spectre_dB_ADCP_Sea_pressure,spectre_dB_ADCP_Altimeter_pressure, spectre_dB_PS_Sea_pressure),
                    (freqs.min(),freqs.max()),
                    (fmin_ig, fmax_ig, 'Infra gravity waves interval'), 
                    (fmin_ss,fmax_ss, 'Sea swell waves interval')])
    #All Hm0
    plot_dataframe(N, 
                   [(Time,Hm0_IG_Sea_pressure,Hm0_IG_Altimeter_pressure, Hm0_IG_PS_Sea_pressure, 
                     Hm0_SS_Sea_pressure,Hm0_SS_Altimeter_pressure, Hm0_SS_PS_Sea_pressure,
                     Hm0_total_Sea_pressure,Hm0_total_Altimeter_pressure, Hm0_total_PS_Sea_pressure),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])
    
    #-------------------------------------------------------------------------------------------------------------------
    """plot_dataframe(df, N, 
                   [(Time,Hm0_IG,Hm0_SS,Hm0_total),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5)), 
                    (Time.min()+timedelta(minutes=15),Time.min()+timedelta(minutes=30), 'ig waves interval'), 
                    (Time.max()-timedelta(minutes=30),Time.max()-timedelta(minutes=15), 'sea swell waves interval')])
                    
        
    #Hm0 IG waves (wwaves mesure in m)
    plot_dataframe(N, 
                   [(Time,Hm0_IG_Sea_pressure,Hm0_IG_Altimeter_pressure, Hm0_IG_PS_Sea_pressure),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])
    
    #Hm0 SS waves (wwaves mesure in m)
    plot_dataframe(N, 
                   [(Time,Hm0_SS_Sea_pressure,Hm0_SS_Altimeter_pressure, Hm0_SS_PS_Sea_pressure),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])
    
    #Hm0 total waves (wwaves mesure in m)
    plot_dataframe(N, 
                   [(Time,Hm0_total_Sea_pressure,Hm0_total_Altimeter_pressure, Hm0_total_PS_Sea_pressure),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])"""


import sys
import os
import pandas as pd

from matplotlib.pyplot import *
from datetime import timedelta

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Plots_datas.plots_dataframe import plot_dataframe,plot_envelopes, plot_3d_spectrum
from Process_Datas.compute_spectrum import compute_spectrum, compute_2D_spectrum
from Process_Datas.butter_lowpass_filter import butter_bandpass_filter, high_pass_filter
from Read_Datas.read_pickle_to_df import read_pickle_to_df
from Process_Datas.add_waves_description_columns import fourier_windows
from tqdm import tqdm
import numpy as np


def plot_process_data_wave_analysis(pickle_path_file_ADCP, pickle_path_file_Pressure_sensor, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fs_data, fe, N, seconds, fe_ig, fe_ss, cutoff):
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
    print(f"len(Time_ADCP) : {len(Time_ADCP)}")
    Time_PS = df_PS['Time']
    print(f"len(Time_PS) : {len(Time_PS)}")
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
        
        Time = Time_ADCP
    
    print(f"len(Time) : {len(Time)}")

    print("df_ADCP")
    print(df_ADCP)
    print()
    print("df_PS")
    print(df_PS)
    
    Temperature_ADCP = df_ADCP['Temperature']
    Temperature_ADCP = pd.Series(Temperature_ADCP, name="Temperature_ADCP")
    Temperature_PS = df_PS['Temperature']
    Temperature_PS = pd.Series(Temperature_PS, name="Temperature_PS")

    Sea_pressure_ADCP = df_ADCP['Sea pressure']
    Sea_pressure_ADCP = pd.Series(Sea_pressure_ADCP, name="Sea_pressure_ADCP")
    AST_pressure_ADCP = df_ADCP['AltimeterPressure']
    AST_pressure_ADCP = pd.Series(AST_pressure_ADCP, name="AST_pressure_ADCP")
    Sea_pressure_PS = df_PS['Sea pressure']
    Sea_pressure_PS = pd.Series(Sea_pressure_PS, name="Sea_pressure_PS")
    
    Sea_pressure_PS_centred = Sea_pressure_PS - abs(AST_pressure_ADCP.mean() -Sea_pressure_PS.mean())
    Sea_pressure_PS_centred = pd.Series(Sea_pressure_PS_centred, name="Sea_pressure_PS_centred")
    
    Depth_ADCP = df_ADCP['AltimeterDistanceAST']
    Depth_ADCP = pd.Series(Depth_ADCP, name="Depth_ADCP")
    Depth_PS = df_PS['Depth']
    Depth_PS = pd.Series(Depth_PS, name="Depth_PS")
    print(f"Epsilon L = {abs(Depth_ADCP.mean() -Depth_PS.mean() )}")
    
    print(f"Epsilon Pressue between ADCP and PS = {abs(AST_pressure_ADCP.mean() -Sea_pressure_PS.mean() )}")
    
    
    df_PS['Sea_pressure_PS_centred'] = np.nan
    df_PS['Sea_pressure_PS_centred'] = Sea_pressure_PS_centred
    
    df_PS_shift = df_PS.copy()
    df_PS_shift.set_index('Time', inplace=True)
    df_PS_shift['Sea_pressure_PS_centred'] = df_PS_shift['Sea_pressure_PS_centred'].shift(+22)
    df_PS_shift.reset_index(inplace=True)
    
    #df_ADCP['Sea pressure']
    
    # Calcule le coefficient de corrélation de Pearson
    correlation_coefficient = np.corrcoef(AST_pressure_ADCP, Sea_pressure_PS)[0, 1]
    print(f"correlation_coefficient : {correlation_coefficient}")
    
        # Créer une copie de AST_pressure_ADCP et df_PS_shift['Sea_pressure_PS_centred']
    AST_pressure_ADCP_copy = AST_pressure_ADCP.copy()
    Sea_pressure_PS_centred_copy = df_PS_shift['Sea_pressure_PS_centred'].copy()

    # Supprimer les NaN des deux séries
    AST_pressure_ADCP_copy = AST_pressure_ADCP_copy.dropna()
    Sea_pressure_PS_centred_copy = Sea_pressure_PS_centred_copy.dropna()

    # Gardez uniquement les valeurs où les deux séries ont des données
    common_index = AST_pressure_ADCP_copy.index.intersection(Sea_pressure_PS_centred_copy.index)
    AST_pressure_ADCP_copy = AST_pressure_ADCP_copy.loc[common_index]
    Sea_pressure_PS_centred_copy = Sea_pressure_PS_centred_copy.loc[common_index]

    # Maintenant, calculez la corrélation
    correlation_coefficient_df_PS_shift = np.corrcoef(AST_pressure_ADCP_copy, Sea_pressure_PS_centred_copy)[0, 1]
    print(f"correlation_coefficient_df_PS_shift : {correlation_coefficient_df_PS_shift}")
    
    #Eliminate the Tide :
    print("----------------------------------------------")
    AST_pressure_ADCP_copy_without_tide = high_pass_filter(AST_pressure_ADCP_copy, "AST_pressure_ADCP_copy", cutoff, fe)
    Sea_pressure_PS_centred_copy_without_tide = high_pass_filter(Sea_pressure_PS_centred_copy, "Sea_pressure_PS_centred_copy", cutoff, fe)
    
    AST_pressure_ADCP_copy_without_tide = AST_pressure_ADCP_copy_without_tide.iloc[4800:]
    Sea_pressure_PS_centred_copy_without_tide = Sea_pressure_PS_centred_copy_without_tide.iloc[4800:]
    Time_without_tide = Time.iloc[4800:]
    Time_without_tide = Time_without_tide.iloc[:-22]
    condition_ADCP = df_ADCP['Time'].isin(Time_without_tide)
    condition_PS = df_PS['Time'].isin(Time_without_tide)
    AST_depth_ADCP_copy_without_tide = df_ADCP.loc[condition_ADCP, 'AltimeterPressure']
    AST_depth_ADCP_copy_without_tide = AST_depth_ADCP_copy_without_tide.iloc[:-2]
    depth_PS_copy_without_tide = df_PS.loc[condition_PS, 'Depth']
    depth_PS_copy_without_tide = depth_PS_copy_without_tide.iloc[:-2]
    
    
    print("*****AST_pressure_ADCP_copy_without_tide******")
    print(AST_pressure_ADCP_copy_without_tide)
    print("******Sea_pressure_PS_centred_copy_without_tide******")
    print(Sea_pressure_PS_centred_copy_without_tide)
    print("********Time_without_tide*******")
    print(Time_without_tide)
    print("********AST_depth_ADCP_copy_without_tide********")
    print(AST_depth_ADCP_copy_without_tide)
    print("********depth_PS_copy_without_tide********")
    print("serie pandas")
    print(depth_PS_copy_without_tide)
    
    AST_pressure_ADCP_copy_without_tide_spectrum, freqs_spectrum = compute_spectrum(AST_pressure_ADCP_copy_without_tide,"AST_pressure_ADCP_copy_without_tide", fe)
    Sea_pressure_PS_centred_copy_without_tide_spectrum, freqs_spectrum = compute_spectrum(Sea_pressure_PS_centred_copy_without_tide, "Sea_pressure_PS_centred_copy_without_tide", fe)


    """plot_envelopes(AST_pressure_ADCP_copy,  Sea_pressure_PS_centred_copy, fe, fe)
    
    #Sea Pressure PS vs AST pressure from ADCP (signal)
    plot_dataframe(N, "Sea Pressure (dBar)" ,
                   [(Time,AST_pressure_ADCP,Sea_pressure_PS),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])
    
    #Sea Pressure PS centred vs AST pressure from ADCP with tide
    plot_dataframe(N, "Sea Pressure centred with tide (dBar)" ,
                   [(Time,AST_pressure_ADCP_copy,Sea_pressure_PS_centred_copy),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])
    
    #Sea Pressure PS centred vs AST pressure from ADCP without tide
    plot_dataframe(N, "Sea Pressure centred without tide (dBar)" ,
                   [(Time_without_tide,AST_pressure_ADCP_copy_without_tide,Sea_pressure_PS_centred_copy_without_tide),
                    (Time_without_tide.min()+timedelta(minutes=5),Time_without_tide.max()-timedelta(minutes=5))])"""
                    
    #ADCP --> 3D plot : Amplitude (dB) , Freqs (Hz), Depth (m)
    

    #Spetre (Amplitude in dB)
    plot_dataframe(N, "FFT Amplitude of pressure signal (dB)",
                   [(freqs_spectrum,AST_pressure_ADCP_copy_without_tide_spectrum, Sea_pressure_PS_centred_copy_without_tide_spectrum),
                    (freqs_spectrum.min(),1),
                    (fmin_ig, fmax_ig, 'Infra gravity waves interval'), 
                    (fmin_ss,fmax_ss, 'Sea swell waves interval')])
    
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------
    
    """Energy_SS_ADCP_Hm0 = Hm0_SS_Sea_pressure**2
    Energy_SS_ADCP_Hm0 = pd.Series(Energy_SS_ADCP_Hm0, name="Energy_SS_ADCP_Hm0")
    Energy_IG_PS_Hm0 = Hm0_IG_PS_Sea_pressure**2
    Energy_IG_PS_Hm0 = pd.Series(Energy_IG_PS_Hm0, name="Energy_IG_PS_Hm0")
    Energy_SS_PS_Hm0 = Hm0_SS_PS_Sea_pressure**2
    Energy_SS_PS_Hm0 = pd.Series(Energy_SS_PS_Hm0, name="Energy_SS_PS_Hm0")"""
    
    """frequency_IG = df['frequency,IG']
    frequency_SS = df['frequency,SS']
    energy_IG = df['energy,IG']
    energy_SS = df['energy,SS']"""
    
    """
    # Energie of the Waves (IG and SS)
        plot_dataframe(N,  "Energy of the wave",
                    [(Time,Energy_IG_ADCP_Hm0, Energy_IG_ADCP_Hm0_mooving_average_1min30,Energy_IG_ADCP_Hm0_mooving_average_3min, Energy_IG_ADCP_Hm0_mooving_average_1min30_twice ),
                        (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])

    #Temperature
    plot_dataframe(N, 
                   [(Time,Temperature_ADCP,Temperature_PS),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])
    
    # waves detection
    plot_dataframe(N, 
                   [(Time,Energy_IG_ADCP_Hm0_mooving_average_1min30_twice, Energy_IG_ADCP_Hm0_mooving_average_5min_twice),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])
    
    #Depth
    plot_dataframe(N, 
                   [(Time,Depth_ADCP,Depth_PS),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])
    
    
    #All Hm0
    plot_dataframe(N, 
                   [(Time,Hm0_IG_Sea_pressure, Hm0_IG_PS_Sea_pressure, 
                     Hm0_SS_Sea_pressure, Hm0_SS_PS_Sea_pressure),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])
    
    #Hm0 précision entre ADCP et PS : IG 
    plot_dataframe(N, 
                   [(Time,Hm0_IG_Sea_pressure, Hm0_IG_PS_Sea_pressure),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])
    print(f"taux d'erreur entre ADCP et PS par rapport à ADCP pour IG waves : {(abs(Hm0_IG_PS_Sea_pressure.mean() - Hm0_IG_Sea_pressure.mean())/Hm0_IG_Sea_pressure.mean())*100} %")
    print(f"taux d'erreur entre ADCP et PS par rapport à ADCP pour IG waves : {(abs(Hm0_IG_PS_Sea_pressure.mean() - Hm0_IG_Sea_pressure.mean())/Hm0_IG_PS_Sea_pressure.mean())*100} %")
    #Hm0 précision entre ADCP et PS : SS
    plot_dataframe(N, 
                   [(Time, 
                     Hm0_SS_Sea_pressure, Hm0_SS_PS_Sea_pressure),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])
    print(f"taux d'erreur entre ADCP et PS par rapport à ADCP pour SS waves : {(abs(Hm0_SS_PS_Sea_pressure.mean() - Hm0_SS_Sea_pressure.mean())/Hm0_SS_Sea_pressure.mean())*100} %")
    print(f"taux d'erreur entre ADCP et PS par rapport à PS pour SS waves : {(abs(Hm0_SS_PS_Sea_pressure.mean() - Hm0_SS_Sea_pressure.mean())/Hm0_SS_PS_Sea_pressure.mean())*100} %")
    df_signal_ADCP_Sea_pressure_name = "Sea pressure"
    #df_signal_ADCP_Altimeter_pressure_name = "Sea pressure"
    df_signal_PS_Sea_pressure_name = "Sea pressure"

    
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
    
    mean_tide = df['tide'].mean()
    print(f"mean_tide : {mean_tide} m")
    Depth = df['Depth']
    Surface = df['surface']
    Tide = df['tide']
    k0 = df['k0 (deep water number)']

    #df_signal_ADCP_Sea_pressure = fourier_windows(df_ADCP, df_signal_ADCP_Sea_pressure_name, seconds, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fe_ig, fe_ss)
    #print("--------------------df_signal_ADCP_Sea_pressure-------------------------")
    #print(df_signal_ADCP_Sea_pressure)
    df_signal_ADCP_Altimeter_pressure = fourier_windows(df_ADCP, df_signal_ADCP_Altimeter_pressure_name, seconds, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fe_ig, fe_ss)
    print("---------------------df_signal_ADCP_Sea_pressure------------------------")
    print(df_signal_ADCP_Altimeter_pressure)
    df_signal_PS_Sea_pressure = fourier_windows(df_PS, df_signal_PS_Sea_pressure_name, seconds, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fe_ig, fe_ss)
    print("-------------------df_signal_PS_Sea_pressure--------------------------")
    print(df_signal_PS_Sea_pressure)
    #spectre_dB_ADCP_Sea_pressure, freqs = compute_spectrum(df_ADCP, df_signal_ADCP_Sea_pressure_name, fe)
    #spectre_dB_ADCP_Sea_pressure = pd.Series(spectre_dB_ADCP_Sea_pressure, name="spectre_dB_ADCP_Sea_pressure")
    #spectre_dB_ADCP_Altimeter_pressure, freqs = compute_spectrum(df_ADCP, df_signal_ADCP_Altimeter_pressure_name, fe)
    #spectre_dB_ADCP_Altimeter_pressure = pd.Series(spectre_dB_ADCP_Altimeter_pressure, name="spectre_dB_ADCP_Altimeter_pressure")
    #spectre_dB_PS_Sea_pressure, freqs = compute_spectrum(df_PS, df_signal_PS_Sea_pressure_name, fe)
    #spectre_dB_PS_Sea_pressure = pd.Series(spectre_dB_PS_Sea_pressure, name="spectre_dB_PS_Sea_pressure")

    Hm0_IG_Sea_pressure = df_signal_ADCP_Sea_pressure['Hm0,IG']
    Hm0_IG_Sea_pressure = pd.Series(Hm0_IG_Sea_pressure, name="Hm0_IG_ADCP_Sea_pressure")
    Hm0_SS_Sea_pressure  = df_signal_ADCP_Sea_pressure['Hm0,SS']
    Hm0_SS_Sea_pressure = pd.Series(Hm0_SS_Sea_pressure, name="Hm0_SS_ADCP_Sea_pressure")
    Hm0_total_Sea_pressure  = df_signal_ADCP_Sea_pressure['Hm0,total']
    Hm0_total_Sea_pressure = pd.Series(Hm0_total_Sea_pressure, name="Hm0_total_ADCP_Sea_pressure")
    
    #print(f"IG and SS waves on ADCP delta in m : {abs(Hm0_IG_Sea_pressure.mean() - Hm0_SS_Sea_pressure.mean())} m")

    
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
    Hm0_total_PS_Sea_pressure = df_signal_PS_Sea_pressure['Hm0,total']""
    Hm0_total_PS_Sea_pressure = pd.Series(Hm0_total_PS_Sea_pressure, name="Hm0_total_PS_Sea_pressure")
    
    print(f"IG and SS waves on PS delta in m : {abs(Hm0_IG_PS_Sea_pressure.mean() - Hm0_SS_PS_Sea_pressure.mean())} m")

    Energy_IG_ADCP_Hm0 = Hm0_IG_Sea_pressure**2
    Energy_IG_ADCP_Hm0 = pd.Series(Energy_IG_ADCP_Hm0, name="Energy_IG_ADCP_Hm0")
    time_min_IG = 90 #1min30 
    time_max_IG = 300 #5min
    time_mean = int((time_min_IG + time_max_IG)/2)
    
    windows_min = time_min_IG * fe
    windows_max = time_max_IG * fe
    windows_mean = time_mean * fe
    
    #df_signal_ADCP_Sea_pressure['Energy_IG_ADCP_Hm0_mooving_average_1min30_twice'] = None
    
    Energy_IG_ADCP_Hm0_mooving_average_1min30 = Energy_IG_ADCP_Hm0.rolling(window=windows_min, center=True).mean()
    Energy_IG_ADCP_Hm0_mooving_average_1min30 = pd.Series(Energy_IG_ADCP_Hm0_mooving_average_1min30, name="Energy_IG_ADCP_Hm0_mooving_average_1min30")
    
    Energy_IG_ADCP_Hm0_mooving_average_1min30_twice = Energy_IG_ADCP_Hm0_mooving_average_1min30.rolling(window=windows_min, center=True).mean()
    Energy_IG_ADCP_Hm0_mooving_average_1min30_twice = pd.Series(Energy_IG_ADCP_Hm0_mooving_average_1min30_twice, name="Energy_IG_ADCP_Hm0_mooving_average_1min30_twice")
    df_signal_ADCP_Sea_pressure['Energy_IG_ADCP_Hm0_mooving_average_1min30_twice'] = Energy_IG_ADCP_Hm0_mooving_average_1min30_twice
    
    Energy_IG_ADCP_Hm0_mooving_average_3min = Energy_IG_ADCP_Hm0.rolling(window=windows_mean, center=True).mean()
    Energy_IG_ADCP_Hm0_mooving_average_3min = pd.Series(Energy_IG_ADCP_Hm0_mooving_average_3min, name="Energy_IG_ADCP_Hm0_mooving_average_3min")
    
    Energy_IG_ADCP_Hm0_mooving_average_5min = Energy_IG_ADCP_Hm0.rolling(window=windows_max, center=True).mean()
    Energy_IG_ADCP_Hm0_mooving_average_5min = pd.Series(Energy_IG_ADCP_Hm0_mooving_average_5min, name="Energy_IG_ADCP_Hm0_mooving_average_5min")
    
    Energy_IG_ADCP_Hm0_mooving_average_5min_twice = Energy_IG_ADCP_Hm0_mooving_average_5min.rolling(window=windows_mean, center=True).mean()
    Energy_IG_ADCP_Hm0_mooving_average_5min_twice = pd.Series(Energy_IG_ADCP_Hm0_mooving_average_5min_twice, name="Energy_IG_ADCP_Hm0_mooving_average_5min_twice")
    
    #df_signal_ADCP_Sea_pressure = df_signal_ADCP_Sea_pressure.iloc[1200:-1200]
    """
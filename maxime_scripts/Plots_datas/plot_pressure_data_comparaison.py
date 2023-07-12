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
from Process_Datas.compute_spectrum import compute_spectrum_energy, compute_2D_spectrum
from Process_Datas.butter_lowpass_filter import butter_bandpass_filter, high_pass_filter
from Read_Datas.read_pickle_to_df import read_pickle_to_df
from Process_Datas.add_waves_description_columns import fourier_windows
from tqdm import tqdm
import numpy as np
from Process_Datas.resample_dataframe import resample_dataframes

def plot_pressure_data_comparaison(pickle_path_file_ADCP, pickle_path_file_Pressure_sensor, N, cutoff, fe_ADCP, fe_PS, samples_cutoff_filter, fmin_ig, fmax_ig, fmin_ss, fmax_ss):
    fe_ratio = int(fe_PS/fe_ADCP)
    df_ADCP = read_pickle_to_df(pickle_path_file_ADCP)
    df_ADCP = df_ADCP.head(N)
    df_ADCP['Time'] = df_ADCP['Time'].dt.floor('S')

    df_PS = read_pickle_to_df(pickle_path_file_Pressure_sensor) #PS for Pressure Sensor (RBR file)
    df_PS = df_PS.head(fe_ratio*N)
    df_PS['Time'] = df_PS['Time'].dt.floor('S')
    
    """print("before resample df_ADCP")
    print(df_ADCP)
    print()
    print("before resample df_PS")
    print(df_PS)"""
    df_PS = df_PS[::fe_ratio]
    
    """print("after resampled f_ADCP")
    print(df_ADCP)
    print()
    print("after resampled df_PS")
    print(df_PS)"""
    
    # Pour df_ADCP, vous voulez ajouter 000 ms à la première entrée de chaque seconde et 500 ms à la seconde.

    print("df_PS['Time']")
    print(df_PS['Time'])   
    
    print("df_ADCP['Time']")
    print(df_ADCP['Time'])  
    
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
    print("df_PS['Time']")
    print(df_PS['Time'])   
    
    print("df_ADCP['Time']")
    print(df_ADCP['Time'])   

    print("df_ADCP")
    print(df_ADCP)
    print()
    print("df_PS")
    print(df_PS)
    print("Time")
    print(Time)
    
    Temperature_ADCP = df_ADCP['Temperature']
    Temperature_ADCP = pd.Series(Temperature_ADCP, name="Temperature_ADCP")
    Temperature_PS = df_PS['Temperature']
    Temperature_PS = pd.Series(Temperature_PS, name="Temperature_PS")

    Altimeter_pressure_ADCP = df_ADCP['AltimeterPressure']
    Altimeter_pressure_ADCP = pd.Series(Altimeter_pressure_ADCP, name="AltimeterPressure")
    AST_distance_ADCP = df_ADCP['AltimeterDistanceAST']
    AST_distance_ADCP = pd.Series(AST_distance_ADCP, name="AltimeterDistanceAST")
    Sea_pressure_PS = df_PS['Sea pressure']
    Sea_pressure_PS = pd.Series(Sea_pressure_PS, name="Sea_pressure_PS")
    
    """correlation_coefficient_init = np.corrcoef(Altimeter_pressure_ADCP, Sea_pressure_PS)[0, 1]
    print(f"correlation_coefficient before vertical and horizontal shifts: {correlation_coefficient_init}")"""
    
    Sea_pressure_PS_centred = Sea_pressure_PS - abs(Altimeter_pressure_ADCP.mean() -Sea_pressure_PS.mean())
    Sea_pressure_PS_centred = pd.Series(Sea_pressure_PS_centred, name="Sea_pressure_PS_centred")
    
    """correlation_coefficient_after_vertical_shift = np.corrcoef(Altimeter_pressure_ADCP, Sea_pressure_PS_centred)[0, 1]
    print(f"correlation_coefficient before horizontal shifts: {correlation_coefficient_after_vertical_shift}")"""
    
    df_PS['Sea_pressure_PS_centred'] = np.nan
    df_PS['Sea_pressure_PS_centred'] = Sea_pressure_PS_centred
    
    df_PS_shift = df_PS.copy()
    df_PS_shift.set_index('Time', inplace=True)
    df_PS_shift['Sea_pressure_PS_centred'] = df_PS_shift['Sea_pressure_PS_centred'].shift(+22) # décalage de 5.5 secondes
    df_PS_shift.reset_index(inplace=True)
    
    # Créer une copie de AST_pressure_ADCP et df_PS_shift['Sea_pressure_PS_centred']
    Altimeter_pressure_ADCP_copy = Altimeter_pressure_ADCP.copy()
    Sea_pressure_PS_centred_copy = df_PS_shift['Sea_pressure_PS_centred'].copy()
    Sea_pressure_PS_centred_copy = pd.Series(Sea_pressure_PS_centred_copy, name="Sea_pressure_PS_centred_phasing")
    AST_distance_ADCP_copy = AST_distance_ADCP.copy()

    # Supprimer les NaN des deux séries
    Altimeter_pressure_ADCP_copy = Altimeter_pressure_ADCP_copy.dropna()
    Sea_pressure_PS_centred_copy = Sea_pressure_PS_centred_copy.dropna()
    AST_distance_ADCP_copy = AST_distance_ADCP_copy.dropna()

    # Gardez uniquement les valeurs où les deux séries ont des données
    common_index = Altimeter_pressure_ADCP_copy.index.intersection(Sea_pressure_PS_centred_copy.index)
    Altimeter_pressure_ADCP_copy = Altimeter_pressure_ADCP_copy.loc[common_index]
    Sea_pressure_PS_centred_copy = Sea_pressure_PS_centred_copy.loc[common_index]
    AST_distance_ADCP_copy = AST_distance_ADCP_copy.loc[common_index]
    
    """correlation_coefficient_df_PS_shift = np.corrcoef(Altimeter_pressure_ADCP_copy, Sea_pressure_PS_centred_copy)[0, 1]
    print(f"correlation_coefficient_df_PS_shift : {correlation_coefficient_df_PS_shift}")"""
           
    
    #Sea Pressure PS vs AST pressure from ADCP (signal)
    plot_dataframe(N, "AltimeterPressure (dBar) vs AltimeterDistanceAST (m)" ,
                   [(Time,df_ADCP['AltimeterDistanceAST'], df_ADCP['AltimeterPressure']),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])
    
    """#Sea Pressure PS centred vs AST pressure from ADCP (signal)
    plot_dataframe(N, "ADCP vs PS Pressure (dBar)" ,
                   [(Time,AST_distance_ADCP,Altimeter_pressure_ADCP,Sea_pressure_PS_centred),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])
    
    #Sea Pressure PS centred shifted vs AST pressure from ADCP (signal)
    plot_dataframe(N, "ADCP vs PS Pressure (dBar)" ,
                   [(Time,AST_distance_ADCP_copy,Altimeter_pressure_ADCP_copy,Sea_pressure_PS_centred_copy),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])"""
    
    
    #Eliminate the Tide :
    print("----------------------------------------------")
    Altimeter_pressure_ADCP_copy_without_tide = high_pass_filter(Altimeter_pressure_ADCP_copy, "Altimeter_pressure_ADCP_copy", cutoff, fe_ADCP)
    Sea_pressure_PS_centred_copy_without_tide = high_pass_filter(Sea_pressure_PS_centred_copy, "Sea_pressure_PS_centred_copy", cutoff, fe_PS)
    AST_distance_ADCP_copy_without_tide = high_pass_filter(AST_distance_ADCP_copy, "AST_distance_ADCP_copy", cutoff, fe_ADCP)
    
    Altimeter_pressure_ADCP_copy_without_tide = Altimeter_pressure_ADCP_copy_without_tide.iloc[samples_cutoff_filter:] #On supprime les premiers samples pour éviter le régime transitoire du filtre
    Sea_pressure_PS_centred_copy_without_tide = Sea_pressure_PS_centred_copy_without_tide.iloc[samples_cutoff_filter:]
    AST_distance_ADCP_copy_without_tide = AST_distance_ADCP_copy_without_tide.loc[samples_cutoff_filter:]
    Time_without_tide = Time.iloc[samples_cutoff_filter:]
    Time_without_tide = Time_without_tide.iloc[:-22]


    #Sea Pressure PS centred vs AST pressure from ADCP without tide
    plot_dataframe(N, "ADCP vs PS Pressure (dBar) without tide" ,
                   [(Time_without_tide,AST_distance_ADCP_copy_without_tide,Altimeter_pressure_ADCP_copy_without_tide,Sea_pressure_PS_centred_copy_without_tide),
                    (Time_without_tide.min()+timedelta(minutes=5),Time_without_tide.max()-timedelta(minutes=5))])
    
    AST_pressure_ADCP_copy_without_tide_spectrum, freqs_spectrum = compute_spectrum_energy(Altimeter_pressure_ADCP_copy_without_tide,"Altimeter_pressure_ADCP_copy_without_tide", fe_ADCP)
    Sea_pressure_PS_centred_copy_without_tide_spectrum, freqs_spectrum = compute_spectrum_energy(Sea_pressure_PS_centred_copy_without_tide, "Sea_pressure_PS_centred_copy_without_tide", fe_PS)
    AST_distance_ADCP_copy_without_tide_spectrum, freqs_spectrum = compute_spectrum_energy(AST_distance_ADCP_copy_without_tide,"AST_distance_ADCP_copy_without_tide", fe_ADCP)


    #Spetre (Amplitude in dB)
    plot_dataframe(N, "Energy (dBar²/Hz) in log steps",
                   [(freqs_spectrum,AST_pressure_ADCP_copy_without_tide_spectrum, Sea_pressure_PS_centred_copy_without_tide_spectrum, AST_distance_ADCP_copy_without_tide_spectrum),
                    (freqs_spectrum.min(),1),
                    (fmin_ig, fmax_ig, 'Infra gravity waves interval'), 
                    (fmin_ss,fmax_ss, 'Sea swell waves interval')])
    

    
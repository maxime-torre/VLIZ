import sys
import os
import pandas as pd
from datetime import timedelta
from scipy import stats
import numpy as np
# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Plots_datas.plots_dataframe import plot_dataframe_dict, plot_dataframe, plot_dataframe_columns, plot_with_linear_regression
from Read_Datas.read_excel_sheets_to_dfs import read_excel_sheets_to_dfs
from Read_Datas.read_pickle_to_df import read_pickle_to_df
from Read_Datas.read_datas_sheet_to_dfs_only import read_excel_sheets_xlsx, read_excel_sheets_csv
from Read_Datas.read_semicolon_seperated_csv import read_semicolon_separated_csv
from Plots_datas.plot_pressure_data_comparaison import plot_pressure_data_comparaison
from Process_Datas.compute_spectrum import compute_spectrum_energy, compute_2D_spectrum
from Process_Datas.butter_lowpass_filter import butter_bandpass_filter, high_pass_filter
from Process_Datas.add_waves_description_columns import depth_to_pressure, pressure_from_depth_hydraustatique_and_dynamique, pressure_to_depth
from Process_Datas.butter_lowpass_filter import low_pass_filter


def plot_ADCP_PressurevsAltimeter_comparaison(N, pickle_path_file_ADCP, cutoff, fe_ADCP,fmin_ig, fmax_ig, fmin_ss, fmax_ss):
    df_ADCP = read_pickle_to_df(pickle_path_file_ADCP)
    df_ADCP = df_ADCP.head(N)
    df_tide_ADCP = low_pass_filter(df_ADCP['AltimeterDistanceAST'], "AltimeterDistanceAST", cutoff, fe_ADCP)
    df_tide_ADCP = df_tide_ADCP.iloc[600:-600]
    df_tide_ADCP = pd.Series(df_tide_ADCP, name="df_tide_ADCP")
    df_tide_ADCP_centred = df_tide_ADCP - df_tide_ADCP.mean()
    df_tide_ADCP_centred = pd.Series(df_tide_ADCP_centred, name="df_tide_ADCP_centred")
    df_tide_ADCP_centred_elevated = df_tide_ADCP_centred - df_tide_ADCP_centred.min()
    df_tide_ADCP_centred_elevated = pd.Series(df_tide_ADCP_centred_elevated, name="df_tide_ADCP_centred_elevated")

    Time = df_ADCP.Time


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


    rolling_P_linear_theory = P_linear_theory.rolling(window=10).mean()
    rolling_P_linear_theory = pd.Series(rolling_P_linear_theory, name="Rolling_P_linear_theory_from_ADCP")

    Estimation_depth_ADCP = pressure_to_depth(df_ADCP['AltimeterPressure'],df_tide_ADCP, fe_ADCP )
    Estimation_depth_ADCP = pd.Series(Estimation_depth_ADCP, name="Estimation_depth_ADCP")
    slope, intercept, r_value, p_value, std_err = stats.linregress(Estimation_depth_ADCP, df_ADCP['AltimeterDistanceAST'])
    line = slope*Estimation_depth_ADCP+intercept

    Estimation_depth_ADCP_after_correction = Estimation_depth_ADCP*slope + intercept
    
    Amplitude_difference_distanceAST_Estimation_after_correction = df_ADCP['AltimeterDistanceAST'] -(Estimation_depth_ADCP*slope + intercept)
    Amplitude_difference_distanceAST_Estimation_after_correction = pd.Series(Amplitude_difference_distanceAST_Estimation_after_correction, name="Amplitude_difference_distanceAST_Estimation_after_correction")
    Amplitude_difference_distanceAST_Estimation_after_correction = Amplitude_difference_distanceAST_Estimation_after_correction.iloc[600:-600]

    Amplitude_difference_distanceAST_AltimeterPressure = df_ADCP['AltimeterDistanceAST'] - df_ADCP['AltimeterPressure']
    Amplitude_difference_distanceAST_AltimeterPressure = pd.Series(Amplitude_difference_distanceAST_AltimeterPressure, name="Amplitude_difference_distanceAST_AltimeterPressure")

    plot_dataframe(N, "DistanceAST (m) vs Estimation_depth_ADCP (m)" ,
                    [(Time,df_ADCP['AltimeterDistanceAST'], Estimation_depth_ADCP),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])

    plot_with_linear_regression(Estimation_depth_ADCP,df_ADCP['AltimeterDistanceAST'], "AltimeterDistanceAST (ADCP) vs Elevation estimation from AltimeterPressure (ADCP)")

    plot_dataframe(N, "AltimeterDistanceAST (m) vs Estimation_depth_ADCP_after_correction (m)" ,
                    [(Time, df_ADCP['AltimeterDistanceAST'], Estimation_depth_ADCP*slope + intercept),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])

    plot_dataframe(N, "DistanceAST (m) vs AltimeterPressure (dBar)" ,
                    [(Time,df_ADCP['AltimeterDistanceAST'], df_ADCP['AltimeterPressure']),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])

    plot_dataframe(N, "Amplitude_difference_distanceAST_Estimation_after_correction (m) and tide_centred (m)" ,
                    [(Time,Amplitude_difference_distanceAST_Estimation_after_correction, df_tide_ADCP),
                    (Time.min(),Time.max())])

    plot_dataframe(N, "Amplitude_difference_distanceAST_Estimation_after_correction (m) and df_tide_ADCP_centred_elevated (m)" ,
                    [(Time,Amplitude_difference_distanceAST_Estimation_after_correction, df_tide_ADCP_centred_elevated),
                    (Time.min(),Time.max())])
    
    AltimeterDistanceAST_without_tide = high_pass_filter(df_ADCP['AltimeterDistanceAST'], "AltimeterDistanceAST", cutoff, fe_ADCP)
    AltimeterPressure_without_tide = high_pass_filter(df_ADCP['AltimeterPressure'], "AltimeterPressure", cutoff, fe_ADCP)
    Estimation_depth_ADCP_after_correction_without_tide = high_pass_filter(Estimation_depth_ADCP_after_correction, "Estimation_depth_ADCP_after_correction", cutoff, fe_ADCP)
    
    AltimeterDistanceAST_without_tide_spectrum, freqs_spectrum = compute_spectrum_energy(AltimeterDistanceAST_without_tide,"AltimeterDistanceAST_without_tide", fe_ADCP)
    AltimeterDistanceAST_without_tide_spectrum = pd.Series(AltimeterDistanceAST_without_tide_spectrum, name="Energy of AltimeterDistanceAST")
    AltimeterPressure_without_tide_without_tide_spectrum, freqs_spectrum = compute_spectrum_energy(AltimeterPressure_without_tide,"AltimeterPressure_without_tide", fe_ADCP)
    AltimeterPressure_without_tide_without_tide_spectrum = pd.Series(AltimeterPressure_without_tide_without_tide_spectrum, name="Energy of AltimeterPressure")
    Estimation_depth_ADCP_after_correction_without_tide_spectrum, freqs_spectrum = compute_spectrum_energy(Estimation_depth_ADCP_after_correction_without_tide,"Estimation_depth_ADCP_after_correction_without_tide", fe_ADCP)
    Estimation_depth_ADCP_after_correction_without_tide_spectrum = pd.Series(Estimation_depth_ADCP_after_correction_without_tide_spectrum, name="Energy of depth estimation from AltimeterPressure")

    #Spetre (Amplitude in dB
    plot_dataframe(N, "Energy (dBar²/Hz) in log scale",
                   [(freqs_spectrum,AltimeterDistanceAST_without_tide_spectrum,Estimation_depth_ADCP_after_correction_without_tide_spectrum, AltimeterPressure_without_tide_without_tide_spectrum),
                    (freqs_spectrum.min(),1),
                    (fmin_ig, fmax_ig, 'Infra gravity waves interval'), 
                    (fmin_ss,fmax_ss, 'Sea swell waves interval')])
    
    plot_dataframe(N, "Energy (dBar²/Hz) in log scale",
                   [(freqs_spectrum,AltimeterDistanceAST_without_tide_spectrum,Estimation_depth_ADCP_after_correction_without_tide_spectrum, AltimeterPressure_without_tide_without_tide_spectrum),
                    (freqs_spectrum.min(),0.3),
                    (fmin_ig, fmax_ig, 'Infra gravity waves interval'), 
                    (fmin_ss,0.3, 'Sea swell waves interval')])

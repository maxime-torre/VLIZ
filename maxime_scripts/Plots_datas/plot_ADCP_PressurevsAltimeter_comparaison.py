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
from Process_Datas.butter_lowpass_filter import butter_bandpass_filter, high_pass_filter, low_pass_filter
from Process_Datas.add_waves_description_columns import depth_to_pressure, pressure_from_depth_hydraustatique_and_dynamique, pressure_to_depth
from Process_Datas.butter_lowpass_filter import low_pass_filter
from Plots_datas.u_tide_estimation import u_tide_estimation


def plot_ADCP_PressurevsAltimeter_comparaison(N, pickle_path_file_ADCP, cutoff, fe_ADCP,fmin_ig, fmax_ig, fmin_ss, fmax_ss,Latitute):
    df_ADCP = read_pickle_to_df(pickle_path_file_ADCP)
    df_ADCP = df_ADCP.head(N)
    AltimeterDistanceAST = df_ADCP['AltimeterDistanceAST']
    AltimeterDistanceAST = pd.Series(AltimeterDistanceAST, name="AltimeterDistanceAST from ADCP (m)")
    AltimeterPressure = df_ADCP['AltimeterPressure']
    AltimeterPressure = pd.Series(AltimeterPressure, name="ADCP Pressure")
    df_tide_ADCP = low_pass_filter(AltimeterDistanceAST, "AltimeterDistanceAST", cutoff, fe_ADCP)
    df_tide_ADCP = df_tide_ADCP.iloc[600:-600]
    df_tide_ADCP = pd.Series(df_tide_ADCP, name="Tide (m) using LowPassFilter on AltimeterDistanceAST")
    df_tide_ADCP_centred = df_tide_ADCP - df_tide_ADCP.mean()
    df_tide_ADCP_centred = pd.Series(df_tide_ADCP_centred, name="df_tide_ADCP_centred")
    df_tide_ADCP_centred_elevated = df_tide_ADCP_centred - df_tide_ADCP_centred.min()
    df_tide_ADCP_centred_elevated = pd.Series(df_tide_ADCP_centred_elevated, name="df_tide_ADCP_centred_elevated")

    Time = df_ADCP.Time

    P_linear_theory = depth_to_pressure(AltimeterDistanceAST, df_tide_ADCP, fe_ADCP)
    P_linear_theory = pd.Series(P_linear_theory, name="P_linear_theory_from_ADCP")
    print(f"len(Eta) : {len(P_linear_theory)}")
    print(f"len(Time) : {len(Time)}")
    print(P_linear_theory)
    u_tide_estimation_m, AltimeterDistanceAST_without_tide_Utide = u_tide_estimation(AltimeterDistanceAST, Time, Latitute)
    u_tide_estimation_m = pd.Series(u_tide_estimation_m, name="Tide (m) using Utide Library")
    u_tide_estimation_m_centred = u_tide_estimation_m - u_tide_estimation_m.mean()
    u_tide_estimation_m_centred_elevated = u_tide_estimation_m_centred - u_tide_estimation_m_centred.min()
    u_tide_estimation_m_centred_elevated = pd.Series(u_tide_estimation_m_centred_elevated, name="Tide centred and elevated (m) using Utide Library")

    
    rolling_P_linear_theory = P_linear_theory.rolling(window=10).mean()
    rolling_P_linear_theory = pd.Series(rolling_P_linear_theory, name="Rolling_P_linear_theory_from_ADCP")

    Estimation_depth_ADCP = pressure_to_depth(AltimeterPressure,df_tide_ADCP, fe_ADCP )
    Estimation_depth_ADCP = pd.Series(Estimation_depth_ADCP, name="Surface elevation from wave theory applied to the PressureSensor of the ADCP")
    slope, intercept, r_value, p_value, std_err = stats.linregress(Estimation_depth_ADCP, AltimeterDistanceAST)
    line = slope*Estimation_depth_ADCP+intercept

    Estimation_depth_ADCP_after_correction = Estimation_depth_ADCP*slope + intercept
    Estimation_depth_ADCP_after_correction = pd.Series(Estimation_depth_ADCP_after_correction, name="Depth (m) estimation from AltimeterPressure using WavesTheory after correction")
    
    Amplitude_difference_distanceAST_Estimation_after_correction = AltimeterDistanceAST -(Estimation_depth_ADCP*slope + intercept)
    Amplitude_difference_distanceAST_Estimation_after_correction = pd.Series(Amplitude_difference_distanceAST_Estimation_after_correction, name="Amplitude difference (m) between AltimeterDistanceAST (m) and depth estimate after correction (m)")
    Amplitude_difference_distanceAST_Estimation_after_correction = Amplitude_difference_distanceAST_Estimation_after_correction.iloc[600:-600]

    plot_dataframe(N, "Depth (m)" ,
                   f"Depth (m) from ADCP plotted against time for the Trapergeer station over {N} samples",
                    [(Time,AltimeterDistanceAST, Estimation_depth_ADCP, u_tide_estimation_m, df_tide_ADCP),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])

    plot_with_linear_regression(Estimation_depth_ADCP,AltimeterDistanceAST, "AltimeterDistanceAST (ADCP) vs Elevation estimation from AltimeterPressure (ADCP)")

    plot_dataframe(N, "Depth (m)" ,
                   f"Depth (m) from ADCP plotted against time for the Trapergeer station over {N} samples after correction",
                    [(Time, AltimeterDistanceAST, Estimation_depth_ADCP_after_correction, u_tide_estimation_m, df_tide_ADCP),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])

    plot_dataframe(N, "Depth (m) vs AltimeterPressure (dBar)" , #have to create a new y axis for AltimeterPressure
                   f"Depth (m) and Pressure (dBar) from ADCP plotted against time for the Trapergeer station over {N} samples after correction",
                    [(Time,AltimeterDistanceAST, AltimeterPressure),
                    (Time.min()+timedelta(minutes=5),Time.max()-timedelta(minutes=5))])

    plot_dataframe(N, "Depth (m)" ,
                   f"Depth (m) and AltimeterPressure (dBar) from ADCP plotted against time for the Trapergeer station over {N} samples after correction",
                    [(Time,Amplitude_difference_distanceAST_Estimation_after_correction, df_tide_ADCP, u_tide_estimation_m),
                    (Time.min(),Time.max())])

    plot_dataframe(N, "Depth (m)" ,
                   f"Amplitude difference and Tides (m) from ADCP plotted against time for the Trapergeer station over {N} samples after correction",
                    [(Time,Amplitude_difference_distanceAST_Estimation_after_correction, df_tide_ADCP_centred_elevated, u_tide_estimation_m_centred_elevated),
                    (Time.min(),Time.max())])
    
    AltimeterDistanceAST_without_tide = high_pass_filter(AltimeterDistanceAST, "AltimeterDistanceAST", cutoff, fe_ADCP)
    AltimeterPressure_without_tide = high_pass_filter(AltimeterPressure, "AltimeterPressure", cutoff, fe_ADCP)
    Estimation_depth_ADCP_after_correction_without_tide = high_pass_filter(Estimation_depth_ADCP_after_correction, "Estimation_depth_ADCP_after_correction", cutoff, fe_ADCP)
    
    AltimeterDistanceAST_without_tide_spectrum, freqs_spectrum = compute_spectrum_energy(AltimeterDistanceAST_without_tide,"AltimeterDistanceAST_without_tide", fe_ADCP)
    AltimeterDistanceAST_without_tide_spectrum = pd.Series(AltimeterDistanceAST_without_tide_spectrum, name="Energy of AltimeterDistanceAST")
    AltimeterPressure_without_tide_without_tide_spectrum, freqs_spectrum = compute_spectrum_energy(AltimeterPressure_without_tide,"AltimeterPressure_without_tide", fe_ADCP)
    AltimeterPressure_without_tide_without_tide_spectrum = pd.Series(AltimeterPressure_without_tide_without_tide_spectrum, name="Energy of AltimeterPressure")
    Estimation_depth_ADCP_after_correction_without_tide_spectrum, freqs_spectrum = compute_spectrum_energy(Estimation_depth_ADCP_after_correction_without_tide,"Estimation_depth_ADCP_after_correction_without_tide", fe_ADCP)
    Estimation_depth_ADCP_after_correction_without_tide_spectrum = pd.Series(Estimation_depth_ADCP_after_correction_without_tide_spectrum, name="Energy of depth estimation from AltimeterPressure")
    AltimeterDistanceAST_without_tide_Utide_spectrum, freqs_spectrum = compute_spectrum_energy(AltimeterDistanceAST_without_tide_Utide,"AltimeterDistanceAST_without_tide_Utide", fe_ADCP)
    AltimeterDistanceAST_without_tide_Utide_spectrum = pd.Series(AltimeterDistanceAST_without_tide_Utide_spectrum, name="Energy of AltimeterDistanceAST using Utide ")
    
    freqs_spectrum = pd.Series(freqs_spectrum, name="Frequency")
    #Spetre (Amplitude in dB
    plot_dataframe(N, "Energy (dBar²/Hz) in log scale",
                   f"Energy (dBar²/Hz) from ADCP plotted against frequency for the Trapergeer station over {N} samples between 0 and 1 Hz ",
                   [(freqs_spectrum,AltimeterDistanceAST_without_tide_spectrum,Estimation_depth_ADCP_after_correction_without_tide_spectrum, AltimeterPressure_without_tide_without_tide_spectrum, AltimeterDistanceAST_without_tide_Utide_spectrum),
                    (freqs_spectrum.min(),1),
                    (fmin_ig, fmax_ig, 'Infra gravity waves interval'), 
                    (fmin_ss,fmax_ss, 'Sea swell waves interval')])
    
    plot_dataframe(N, "Energy (dBar²/Hz) in log scale",
                   f"Energy (dBar²/Hz) from ADCP plotted against frequency for the Trapergeer station over {N} samples between 0 and 0.3 Hz ",
                   [(freqs_spectrum,AltimeterDistanceAST_without_tide_spectrum,Estimation_depth_ADCP_after_correction_without_tide_spectrum, AltimeterPressure_without_tide_without_tide_spectrum, AltimeterDistanceAST_without_tide_Utide_spectrum),
                    (freqs_spectrum.min(),0.3),
                    (fmin_ig, fmax_ig, 'Infra gravity waves interval'), 
                    (fmin_ss,0.3, 'Sea swell waves interval')])
    
    plot_dataframe(N, "Energy (dBar²/Hz) in log scale",
                   f"Energy (dBar²/Hz) from ADCP plotted against frequency for the Trapergeer station over {N} samples between 0 and 0.05 Hz ",
                   [(freqs_spectrum,AltimeterDistanceAST_without_tide_spectrum,Estimation_depth_ADCP_after_correction_without_tide_spectrum, AltimeterPressure_without_tide_without_tide_spectrum, AltimeterDistanceAST_without_tide_Utide_spectrum),
                    (freqs_spectrum.min(),0.05),
                    (fmin_ig, fmax_ig, 'Infra gravity waves interval'), 
                    (fmin_ss,0.05, 'Sea swell waves interval')])

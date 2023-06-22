import sys
import os
import pandas as pd
from scipy.signal import butter,filtfilt
import numpy as np
from scipy.fft import fft, fftfreq
from datetime import datetime, timedelta

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def calculate_Hm0(signal, dt, fmin, fmax):
    n = len(signal)   

    # Fast Fourier transforms
    f = np.fft.fft(signal)
    
    # Calculate the spectral energy
    p = f*np.conj(f)/n
    energy = 2*dt*p[0:n//2] 
    energy = energy.real
    
    # Calculate the frequency
    fre = fftfreq(n, dt)[:n//2]
    
    # Integral of the spectrum
    index = np.where((fre>fmin) & (fre<fmax))[0]
    m0 = sum(energy[index])*(fre[1]-fre[0])
    
    # Significant spectral height
    Hm0 = 4*np.sqrt(m0)

    return Hm0

def fourier(signal, fmin, fmax, fs):
    dt = 1/fs
    n = len(signal)   

    f = np.fft.fft(signal)
    p = f*np.conj(f)/n
    energy = 2*dt*p[0:n//2] 
    energy = energy.real
    
    fre = fftfreq(n, dt)[:n//2]
    
    Hm0 = calculate_Hm0(signal, dt, fmin, fmax)

    index = np.where((fre>fmin) & (fre<fmax))[0]

    if len(index)==0:
        index = np.array([1])
    else:
        index = index
                
    indmax = np.where(energy[index]==max(energy[index]))
    Tp = 1/fre[index][indmax][0]

    return [energy[index], fre[index], Hm0, Tp]

# Define the fourier_windows function

def fourier_windows(df, seconds, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fe_ig, fe_ss):
    # Initialize columns to store the results
    df["Tp,IG"] = np.nan
    df["frequency,IG"] = np.nan
    df["energy,IG"] = np.nan
    df['Hm0,IG'] = np.nan
    df["Tp,SS"] = np.nan
    df["frequency,SS"] = np.nan
    df["energy,SS"] = np.nan
    df['Hm0,SS'] = np.nan
    
    df['Hm0,total'] = np.nan
    
    half_window = timedelta(seconds = seconds / 2)
    
    # Loop through each timestamp
    for i, row in df.iterrows():
        t = row['Time']
        print(f" i : {i}")
        
        # Get data in current time window
        window = df.loc[(df['Time'] >= t - half_window) & (df['Time'] < t + half_window), 'Sea pressure']
        
        # Check if window has data
        if len(window) > 0:
            # Apply fourier function for Infra gravity (IG) waves
            result_IG = fourier(window, fmin_ig, fmax_ig, fe_ig)

            # Apply fourier function for Sea Swell (SS) waves
            result_SS = fourier(window, fmin_ss, fmax_ss, fe_ss)
            
            # Save the results for this timestamp
            df.loc[i, "energy,IG"] = np.mean(result_IG[0])
            df.loc[i, "frequency,IG"] = np.mean(result_IG[1])
            df.loc[i, "Tp,IG"] = result_IG[3]
            print(f"Hm0,IG : {result_IG[2]}")
            df.loc[i, 'Hm0,IG'] = result_IG[2]
            
            df.loc[i, "energy,SS"] = np.mean(result_SS[0])
            df.loc[i, "frequency,SS"] = np.mean(result_SS[1])
            df.loc[i, "Tp,SS"] = result_SS[3]
            print(f"Hm0,SS : {result_SS[2]}")
            df.loc[i, 'Hm0,SS'] = result_SS[2]
            
            df.loc[i,'Hm0,total'] = df.loc[i, 'Hm0,IG'] + df.loc[i, 'Hm0,SS']

    return df





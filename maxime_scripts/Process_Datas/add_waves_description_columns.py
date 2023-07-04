import sys
import os
import pandas as pd
from scipy.signal import butter,filtfilt
import numpy as np
from scipy.fft import fft, fftfreq
from datetime import datetime, timedelta
from tqdm import tqdm

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

def fourier_yuri(signal,fmin,fmax, fs):
    dt = 1/fs
    # print(str(fmin)[0:6]+' Hz < f < '+str(fmax)[0:6]+' Hz'); print(' ')
    # Number of sample points
    n = len(signal)   
    
    # Remove mean from the signal
    # mean = np.mean(signal)
    
    # Fast Fourier transforms
    # f = np.fft.fft(signal-mean)
    f = np.fft.fft(signal)
    
    #Calculate the spectral energy
    p = f*np.conj(f)/n
    energy = 2*dt*p[0:n//2]; 
    energy = energy.real
    
    #Calculate the frequency
    fre = fftfreq(n, dt)[:n//2]
    # fre = 1/dt*np.arange(0,n)/n
    
    #Integral of the spectrum
    index = np.where((fre>fmin) & (fre<fmax))[0]
    m0 = sum(energy[index])*(fre[1]-fre[0])
    
    #Significant spectral height
    Hm0 = 4*np.sqrt(m0); 
    # print('Hm0 = '+str(Hm0)[0:6]+' m')
    
    #Peak period
    if len(index)==0:
        index = np.array([1])
    else:
        index = index
                
    indmax = np.where(energy[index]==max(energy[index]))
    Tp = 1/fre[index][indmax][0]; 
    # print('Tp = '+str(Tp)[0:6]+' s'); print(' '); print(' ')

    return [energy[index], fre[index], Hm0, Tp]

# Define the fourier_windows function

def fourier_windows(df,df_signal_name, second, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fe_ig, fe_ss, save_data):
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
    
    half_window = timedelta(seconds= second / 2)
     
    # Loop through each timestamp
    for i, row in tqdm(list((df.iterrows()))):
        t = row['Time']
        #print(f" i : {i}")
        
        # Get data in current time window
        window = df.loc[(df['Time'] >= t - half_window) & (df['Time'] < t + half_window), df_signal_name]
        
        # Check if window has data
        if len(window) > 0:
            # Apply fourier function for Infra gravity (IG) waves
            result_IG = fourier_yuri(window, fmin_ig, fmax_ig, fe_ig)

            # Apply fourier function for Sea Swell (SS) waves
            result_SS = fourier_yuri(window, fmin_ss, fmax_ss, fe_ss)
            
            # Save the results for this timestamp
            df.loc[i, "energy,IG"] = np.mean(result_IG[0])
            df.loc[i, "frequency,IG"] = np.mean(result_IG[1])
            df.loc[i, "Tp,IG"] = result_IG[3]
            df.loc[i, 'Hm0,IG'] = result_IG[2]
            
            df.loc[i, "energy,SS"] = np.mean(result_SS[0])
            df.loc[i, "frequency,SS"] = np.mean(result_SS[1])
            df.loc[i, "Tp,SS"] = result_SS[3]
            df.loc[i, 'Hm0,SS'] = result_SS[2]
            
            df.loc[i,'Hm0,total'] = df.loc[i, 'Hm0,IG'] + df.loc[i, 'Hm0,SS']
            
    if save_data != None:
        df.to_pickle(save_data)
        return df
    else:
        return df
    
"""def fourier_windows_yuri(data, surface, hour, fmin, fsep, fmax, fs):

    # Define start and end times for the data analysis
    START = datetime(2023, 2, 8, 12,0,0)
    END = datetime(2023, 4, 5, 12,0,0)
    
    # Set the initial start and end times
    tstart = datetime(year=data.time.iloc[0].year, month=data.time.iloc[0].month, day=data.time.iloc[0].day, hour=data.time.iloc[0].hour, minute=0)
    tend = tstart + timedelta(hours=hour)
    
    # Initialize dictionaries to store the results
    wave = {}
    wave["time"] = []
    wave["Hm0,IG"] = []
    wave["Tp,IG"] = []
    wave["frequency,IG"] = []
    wave["energy,IG"] = []
    wave["Hm0,SS"] = []
    wave["Tp,SS"] = []
    wave["frequency,SS"] = []
    wave["energy,SS"] = []
    wave["current"] = []
    wave["tide"] = []
    wave["direction"] = []
    
    # Iterate through the data with the given time window
    while tend < datetime(year=data.time.iloc[-1].year, month=data.time.iloc[-1].month, day=data.time.iloc[-1].day, hour=data.time.iloc[-1].hour):
        print(tstart)
        tstart = tstart + timedelta(hours=hour)
        tend = tend + timedelta(hours=hour)
        index_time = np.where((data.time<tend) & (data.time>tstart))[0]
    
        # If there is data in the current time window, analyze it
        if len(index_time)>0:
            window = surface.iloc[index_time]
    
            # Analyze the infragravity (IG) waves
            appo = fourier_yuri(window,fmin,fsep,fs)
            wave["time"].append(tstart)
            wave["Hm0,IG"].append(appo["Hm0"])
            wave["Tp,IG"].append(appo["Tp"])
            wave["frequency,IG"].append(appo["frequency"])
            wave["energy,IG"].append(appo["energy"])
    
            # Analyze the sea swell (SS) waves
            appo = fourier_yuri(window,fsep,fmax,fs)
            wave["Hm0,SS"].append(appo["Hm0"])
            wave["Tp,SS"].append(appo["Tp"])
            wave["frequency,SS"].append(appo["frequency"])
            wave["energy,SS"].append(appo["energy"])
    
    # Return the results
    return wave"""





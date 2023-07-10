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

def fourier(signal,fmin,fmax, fs):
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

def fourier_windows(df, df_name, seconds, fmin_ig, fmax_ig, fmin_ss, fmax_ss, fe_ig, fe_ss):
    # Initialize columns to store the results
    df["Tp,IG"] = np.nan
    df["frequency,IG"] = np.nan
    df["energy,IG"] = np.nan
    df['Hm0,IG'] = np.nan
    df["Tp,SS"] = np.nan
    df["frequency,SS"] = np.nan
    df["energy,SS"] = np.nan
    df['Hm0,SS'] = np.nan
    
    half_window = timedelta(seconds = seconds / 2)

    # Loop through each timestamp
    for i, row in tqdm(list((df.iterrows()))):
        t = row['Time']

        # Get data in current time window
        window = df.loc[(df['Time'] >= t - half_window) & (df['Time'] < t + half_window), df_name]

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
            df.loc[i, "Hm0,IG"] = result_IG[2]

            df.loc[i, "energy,SS"] = np.mean(result_SS[0])
            df.loc[i, "frequency,SS"] = np.mean(result_SS[1])
            df.loc[i, "Tp,SS"] = result_SS[3]
            df.loc[i, "Hm0,SS"] = result_SS[2]

    return df

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

    #Create dictionary
    result = {}
    result['energy'] = energy[index]
    result['frequency'] = fre[index]
    result['Hm0'] = Hm0
    result['Tp'] = Tp
    
    return result


def fourier_windows_yuri(data, surface, minute, fmin, fsep, fmax, fs, save_data_ADCP_path):
    df = pd.DataFrame()
    
    # Set the initial start and end times
    tstart = datetime(year=data.Time.iloc[0].year, month=data.Time.iloc[0].month, day=data.Time.iloc[0].day, hour=data.Time.iloc[0].hour, minute=0)
    tend = tstart + timedelta(minutes=minute)
    
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
    while tend < datetime(year=data.Time.iloc[-1].year, month=data.Time.iloc[-1].month, day=data.Time.iloc[-1].day, hour=data.Time.iloc[-1].hour):
        print(tstart)
        tstart = tstart + timedelta(minutes=minute)
        tend = tend + timedelta(minutes=minute)
        index_time = np.where((data.Time<tend) & (data.Time>tstart))[0]
    
        # If there is data in the current time window, analyze it
        if len(index_time)>0:
            window = surface.iloc[index_time]
    
            # Analyze the infragravity (IG) waves
            appo = fourier_yuri(window,fmin,fsep,fs)
            wave["time"].append(tstart)
            wave["Hm0,IG"].append(appo["Hm0"])
            wave["Tp,IG"].append(appo["Tp"])
            wave["frequency,IG"].append(appo["frequency"].mean())
            wave["energy,IG"].append(appo["energy"].mean())
            
            # Analyze the sea swell (SS) waves
            appo = fourier_yuri(window,fsep,fmax,fs)
            wave["Hm0,SS"].append(appo["Hm0"])
            wave["Tp,SS"].append(appo["Tp"])
            wave["frequency,SS"].append(appo["frequency"].mean())
            wave["energy,SS"].append(appo["energy"].mean())
            
    df['time'] = wave["time"]
    df['Hm0,IG'] = wave["Hm0,IG"]
    df['Tp,IG'] = wave["Tp,IG"]
    df['frequency,IG'] =  wave["frequency,IG"]
    df['energy,IG'] = wave["energy,IG"]
    df['Hm0,SS'] = wave["Hm0,SS"]
    df['Tp,SS'] =  wave["Tp,SS"]
    df['frequency,SS'] = wave["frequency,SS"]
    df['energy,SS'] = wave["energy,SS"]
    
    df.to_pickle(save_data_ADCP_path)
    
    # Return the results
    return df

def depth_to_pressure(surface, tide, fs):
    hbed = 0.3 # Sensor height from bed (m)  
    tide_signal = tide + hbed
    
    signal = surface
    h = tide_signal.mean() #Mean water depth in (m)
    sample=len(signal) #number of sample in input file
    
    FFTEta = np.fft.fft(signal)
    
    f=np.linspace(0,fs,len(signal)) #frequency
    w=2*np.pi*f #Angular frequency
    
    #Estimation of wave number (k) from Goad (2010)
    k0=w**2/9.81 #Deep water wave number
    k0h=k0*h
    L0 = 9.81/(2*np.pi)*(1/f)**2
    k0 = 2*np.pi/L0
    L = L0*np.tanh(np.sinh(k0h))
    k = 2*np.pi/L
    # k=kh/h #Calculating wave number from Goda (2010)
    k[w==0]=0
    
    #Calculation of pressure response factor
    Kp=np.cosh(k*hbed)/np.cosh(k*h)
    # Kp=np.cosh(-k*(h-hbed))/np.cosh(k*h)
    kmaxL=np.pi/(h-hbed) # Wave number associated with fmaxpcorrL
    KpminL=np.cosh(kmaxL*hbed)/np.cosh(kmaxL*h) # Minimum Limit for K_p calculated based on linear wave theory
    Kp[Kp < KpminL] = KpminL # Check to avoid large amplification, Kp should be larger than minimum K_p calculated based on linear wave theory
    
    Kp1=Kp[0:int(sample/2)]
    Kp1=np.flipud(Kp1)

    
    # Kp[int(sample/2):]=Kp1 #make Kp symetric around fr/2
    Kp[len(Kp) - len(Kp1):] = Kp1 #make Kp symetric around fr/2
    
    #correcting pressure
    FFTEtacor= FFTEta/Kp			    # applies correction factor
    Eta = np.real(np.fft.ifft(FFTEtacor))	# corrected water surface levels time series
    return Eta

def pressure_to_depth(pressure_corrected, tide, fs):
    hbed = 0.3 # Sensor height from bed (m)
    tide_signal = tide + hbed

    signal = pressure_corrected
    h = tide_signal.mean() #Mean water depth in (m)
    sample=len(signal) #number of sample in input file

    FFTEta = np.fft.fft(signal)

    f=np.linspace(0,fs,len(signal)) #frequency
    w=2*np.pi*f #Angular frequency

    #Estimation of wave number (k) from Goad (2010)
    k0=w**2/9.81 #Deep water wave number
    k0h=k0*h
    L0 = 9.81/(2*np.pi)*(1/f)**2
    k0 = 2*np.pi/L0
    L = L0*np.tanh(np.sinh(k0h))
    k = 2*np.pi/L
    # k=kh/h #Calculating wave number from Goda (2010)
    k[w==0]=0

    #Calculation of pressure response factor
    Kp=np.cosh(k*hbed)/np.cosh(k*h)
    # Kp=np.cosh(-k*(h-hbed))/np.cosh(k*h)
    kmaxL=np.pi/(h-hbed) # Wave number associated with fmaxpcorrL
    KpminL=np.cosh(kmaxL*hbed)/np.cosh(kmaxL*h) # Minimum Limit for K_p calculated based on linear wave theory
    Kp[Kp < KpminL] = KpminL # Check to avoid large amplification, Kp should be larger than minimum K_p calculated based on linear wave theory

    Kp1=Kp[0:int(sample/2)]
    Kp1=np.flipud(Kp1)

    # Kp[int(sample/2):]=Kp1 #make Kp symetric around fr/2
    Kp[len(Kp) - len(Kp1):] = Kp1 #make Kp symetric around fr/2

    #correcting pressure
    FFTEtauncor= FFTEta*Kp # applies inverse of correction factor
    Eta = np.real(np.fft.ifft(FFTEtauncor)) # uncorrected water surface levels time series
    return Eta


def pressure_from_depth_hydraustatique(h):
    rho = 1018 # Density of sea water in kg/m^3
    g = 9.81 # Acceleration due to gravity in m/s^2
    P = rho * g * h
    P_dbar = P / 1e4 # Convert from Pascals to decibars
    return P_dbar

def pressure_from_depth_hydraustatique_and_dynamique(surface, tide, fs, hbed):
    tide_signal = tide + hbed
    f=np.linspace(0,fs,len(surface)) #frequency
    w=2*np.pi*f #Angular frequency
    
    #Estimation of wave number (k) from Goad (2010)
    k0=w**2/9.81 #Deep water wave number
    k0h=k0*tide_signal
    L0 = 9.81/(2*np.pi)*(1/f)**2
    k0 = 2*np.pi/L0
    L = L0*np.tanh(np.sinh(k0h))
    k = 2*np.pi/L
    Kp=np.cosh(k*hbed)/np.cosh(k*tide_signal)
    pressure = (surface)*Kp
    
    return pressure
    

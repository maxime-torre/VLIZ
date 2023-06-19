import sys
import os
import pandas as pd
from scipy.signal import butter,filtfilt
import numpy as np

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def add_surface_correlation_column_and_cte_evaluation(df, fs, hbed):
    tstart = df['Time'].min()
    tend = df['Time'].max()
    min_index = np.where(df['Time'] == tstart)[0][0]
    max_index = np.where(df['Time'] == tend)[0][0]
    signal = df['Sea pressure'].iloc[min_index:max_index+1]
    appo = np.empty([0])
    h = df['tide'].iloc[min_index:max_index+1].mean() #Mean water depth in (m)
    sample=len(signal) #number of sample in input file
    
    f=np.linspace(0,fs,len(signal)) #frequency
    w=2*np.pi*f #Angular frequency

    FFTEta = np.fft.fft(signal)

    #Estimation of wave number (k) from Goad (2010)
    k0=w**2/9.81 #Deep water wave number
    L0 = 9.81/(2*np.pi)*(1/f)**2
    k0 = 2*np.pi/L0
    L = L0*np.tanh(np.sinh(k0*h))
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
    Kp[len(Kp1):]=Kp1 #make Kp symetric around fr/2
    
    #correcting pressure
    FFTEtacor= FFTEta/Kp			    # applies corection factor
    Eta = np.real(np.fft.ifft(FFTEtacor))	# corected water surface levels time series
    appo = np.concatenate((appo, Eta))
    
    """df['surface_corr'] = np.nan
    FFTEtacor_series = pd.Series(FFTEtacor)
    df['FFTEtacor_real'] = FFTEtacor_series.apply(lambda x: x.real)
    df['FFTEtacor_imag'] = FFTEtacor_series.apply(lambda x: x.imag)
    df['FFTEtacor_amp'] = FFTEtacor_series.apply(lambda x: abs(x))
    df['FFTEtacor_phase'] = FFTEtacor_series.apply(lambda x: np.angle(x))
    df['surface_corr'] = appo"""
    
    df['k0 (deep water number)'] = np.nan
    
    df['k0 (deep water number)'] = k0

    return [Kp.mean(), h.mean() ,k.mean()]

def check_complex_values(df):
    for column in df.columns:
        if any(isinstance(val, complex) for val in df[column]):
            print(f"La colonne {column} contient des valeurs complexes")

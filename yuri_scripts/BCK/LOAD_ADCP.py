# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 13:27:21 2023

@author: yuri.pepi
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import dolfyn as dlfn
import pickle
import scipy
from scipy.fft import fft, fftfreq
import matplotlib.dates as mdates
import math
import oceanwaves
from scipy import signal
from scipy.signal import butter,filtfilt
import os

# %%

FS = 20
SAVE = 0
SIZE = 100
LW = 2

# Load the signature, AWAC, RBR, wave, and buoy data from pickled files
f = open('Signature_Trap.pckl', 'rb')
signature_all = pickle.load(f)   # Signature data from Trapegeer 
f.close()

f = open('Signature_Rave1.pckl', 'rb')
signature_rave1 = pickle.load(f)   # Signature data from Raversijde 1 
f.close()

f = open('Signature_Rave2.pckl', 'rb')
signature_rave2 = pickle.load(f)   # Signature data from Raversijde 2 
f.close()

f = open('AWAC_Nie.pckl', 'rb')
awac_all = pickle.load(f)       # AWAC data from Nieuwport 
f.close()

f = open('RBR_ALL.pckl', 'rb')
rbr_all = pickle.load(f)        # RBR data from both areas
f.close()

f = open('WAVE_ALL.pckl', 'rb')
# Wave data from AWAC, signature at Trapegeer, and RBR at Trapegeer and Nieuwport
[awac_wave, signa_wave, rbr_trap_wave, 
              rbr_nieu_wave, rbr_trap_wave_corr, rbr_nie_wave_corr, signa_wave_rave1, signa_wave_rave2] = pickle.load(f)
f.close()

f = open('BUOY_ALL.pckl', 'rb')
# Buoy data for Trapegeer, Nieuwport, Westhinder, and Kwintebank buoys
[trap, nieu, west, kwin] = pickle.load(f)
f.close()

# Clean up the workspace by deleting the file object and avoiding name clashes
del f

# %%
""" 

""" 
# %%


"""   
LOAD DATA
"""
# %% SIGNATURE 1000


# # Set the directory path containing the ad2cp files from SIGNATURE1000

# folder_path = "C:/Users/yuri.pepi/Desktop/IG-WAVES/Winter 22-23/Nortek 102377/102377/AD2CP/"

# # Create an empty list to hold the data frames
# dfs_all = []


# # Loop through all the files in the folder
# for file_name in os.listdir(folder_path):
#     print(file_name)
#     # Read the ad2cp file
#     df = dlfn.read(folder_path + file_name)
#     dlfn.rotate2(df,'earth')
#     print("Loaded")
#     # Append the data frame to the list of data frames
#     dfs_all.append(df)
#     print("Appended")
#     print("--------------------------------")

#     # %%

# # Create an empty list to hold the data frames
# dfs = []

# for dataframe in dfs_all:
#     time = pd.to_datetime(np.array(dataframe.time)) #Time
#     ast = np.array(dataframe.ast_dist) #AST
#     # create a DataFrame using the two arrays
#     df = pd.DataFrame({'time': time, 'ast': ast})
#     # Append the data frame to the list of data frames
#     dfs.append(df)
#     fs =dataframe.fs #Sample frequency
#     dt = 1/fs

# del time; del ast;

# data = pd.concat(dfs, ignore_index=True)
# # %%

# # Saving the objects:
# f = open('Signature_Trap.pckl', 'wb')
# pickle.dump(data, f)
# f.close()

# %% SIGNATURE1000 - Raversijde 1 - 2

# # Set the directory path containing the Excel files
# folder_path = "C:/Users/yuri.pepi/Desktop/Yuri/IG WAVES/SCRIPT/appo"

# # Create an empty list to hold the data frames
# dfs = []

# # Loop through all the files in the folder
# for file_name in os.listdir(folder_path):
#     print(file_name)
#     # Read the Excel file into a data frame
#     df = pd.read_csv(os.path.join(folder_path, file_name), sep=';')
#     # Select the 3 columns you want to keep
#     df = df[['DateTime', 'AltimeterDistanceAST', 'Pitch', 'Roll']]
#     # Append the data frame to the list of data frames
#     dfs.append(df)

# # Concatenate all the data frames into a single data frame
# result = pd.concat(dfs, ignore_index=True)

# # result = result.drop(columns=['time'])
# result = result.rename(columns={'DateTime': 'time'})
# result = result.rename(columns={'AltimeterDistanceAST': 'ast'})
# result = result.rename(columns={'Pitch': 'pitch'})
# result = result.rename(columns={'Roll': 'roll'})

# #Convert date column in datetime format
# result['time'] = pd.to_datetime(result['time'])
# # result = pd.concat([result, result1]).reset_index(drop=True)

# # Order the database based on the date
# result = result.sort_values('time')

# # Saving the objects:
# f = open('Signature_Rave2.pckl', 'wb')
# pickle.dump(result, f)
# f.close()

# fig=plt.figure(figsize=(36,24))
# ax=fig.add_subplot(111)
# plt.plot(result.time, result.ast,'.')

# %% AWAC 1MHz

# # specify the file path and file name
# folder_path = "C:/Users/yuri.pepi/Desktop/IG-WAVES/Winter 22-23/AWAC Nieuwpoort/"

# # load the file into a Pandas DataFrame
# wad = pd.read_csv(folder_path + 'AWAC_105.wad', header=None, delimiter=r"\s+", names=[
#     "Burst counter",
#     "Ensemble counter",
#     "Pressure",
#     "AST Distance1 (Beam4)",
#     "AST Distance2 (Beam4)",
#     "AST Quality (Beam4)",
#     "Analog input",
#     "Velocity (Beam1)",
#     "Velocity (Beam2)",
#     "Velocity (Beam3)",
#     "Amplitude (Beam1)",
#     "Amplitude (Beam2)",
#     "Amplitude (Beam3)"
# ])

# # load the file into a Pandas DataFrame
# whd = pd.read_csv(folder_path + 'AWAC_105.whd', header=None, delimiter=r"\s+", names=[
#     "Month",
#     "Day",
#     "Year",
#     "Hour", 
#     "Minute",
#     "Second",
#     "Burst counter",
#     "No of wave data records",
#     "Cell position",
#     "Battery voltage",
#     "Soundspeed",
#     "Heading",
#     "Pitch",
#     "Roll",
#     "Minimum pressure",
#     "Maximum pressure",
#     "Temperature",
#     "CellSize",
#     "Noise amplitude beam 1",
#     "Noise amplitude beam 2",
#     "Noise amplitude beam 3",
#     "Noise amplitude beam 4",
#     "AST window start",
#     "AST window size",
#     "AST window offset"
# ])
# whd['date'] = pd.to_datetime(whd[['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']])


# # %%

# # Create a timedelta object for dt
# delta = timedelta(seconds=0.5)

# # Create an empty array for datetime objects
# datetime_list = []

# # Loop through each row in whd.date and create a datetime object for each row
# for date_str in whd.date:
#     datetime_array = []
#     print(date_str)
#     print("-----------------------------")
#     # Loop through the number of samples and create a datetime for each sample
#     for i in range(2400):
#         sample_time = date_str + i * delta
#         datetime_array.append(sample_time)

#     datetime_array_np = np.array(datetime_array, dtype='datetime64[s]')
#     datetime_list.append(datetime_array_np)
    
# time_awac = np.concatenate(datetime_list)[0:len(wad)]

# # %%
# # create a new dataframe
# awac_all = pd.DataFrame({'time': time_awac, 'ast': wad["AST Distance1 (Beam4)"]})

# # %%
# # Saving the objects:
# f = open('AWAC_ALL.pckl', 'wb')
# pickle.dump([wad, whd], f)
# f.close()

# f = open('AWAC_Nie.pckl', 'wb')
# pickle.dump(awac_all, f)
# f.close()

# %% RBR quartz3


# # Set the directory path containing the rbr files

# folder_path_nie = "C:/Users/yuri.pepi/Desktop/IG-WAVES/Winter 22-23/RBR 210960/210960_20230417_0957/"
# folder_path_trap = "C:/Users/yuri.pepi/Desktop/IG-WAVES/Winter 22-23/RBR 210961/210961_20230417_0929_v2/"

# # load the file into a Pandas DataFrame
# rbr_trap = pd.read_csv(folder_path_trap + '210961_20230417_0929_v2_data.txt', skiprows=2, header=None, delimiter=r",", names=[
#     "time",
#     "temperature brp",
#     "pressure",
#     "temperature",
#     "sea pressure",
#     "depth",
#     "period",
#     "period2"])

# rbr_nie = pd.read_csv(folder_path_nie + '210960_20230417_0957_data.txt', header=None, skiprows=2, delimiter=r",", names=[
#     "time",
#     "temperature brp",
#     "pressure",
#     "temperature",
#     "sea pressure",
#     "depth",
#     "period",
#     "period2"])

# rbr_nie.time = pd.to_datetime(rbr_nie.time)
# rbr_trap.time = pd.to_datetime(rbr_trap.time)

# # Define a timedelta object
# delta = timedelta(days=8278, hours=14, minutes=27, seconds=39)

# # Add the timedelta to the datetime object
# rbr_nie.time = rbr_nie.time + delta


# # Saving the objects:
# f = open('RBR_ALL.pckl', 'wb')
# pickle.dump([rbr_trap, rbr_nie], f)
# f.close()


# %%


"""   
FILTER DATA - remove errors and deploy/recovery activities
"""  
# %% SIGNATURE Trap


# fs = 4
# dt = 1/fs

# time_all = signature_all.time
# surface_all = signature_all.ast

# tstart = datetime(year=time_all[0].year, month=time_all[0].month, day=time_all[0].day+1, hour=time_all[0].hour) #Starting time
# tend = datetime(year=time_all.iloc[-1].year, month=time_all.iloc[-1].month, day=time_all.iloc[-1].day-1, hour=time_all.iloc[-1].hour) #Ending time
# index_time = np.where((time_all<tend) & (time_all>tstart) & (np.isfinite(surface_all)) & (surface_all>4) & (~np.isnan(surface_all)))[0]

# signature = signature_all[index_time[0]:index_time[-1]]
# signature = signature[~np.isnan(signature.ast) & np.isfinite(signature.ast)]

# %% SIGNATURE Rave1


# fs = 4
# dt = 1/fs

# time_all = signature_rave1.time
# surface_all = signature_rave1.ast

# tstart = datetime(year=time_all[0].year, month=time_all[0].month, day=time_all[0].day+1, hour=time_all[0].hour) #Starting time
# tend = datetime(year=time_all.iloc[-1].year, month=time_all.iloc[-1].month, day=time_all.iloc[-1].day-1, hour=time_all.iloc[-1].hour) #Ending time
# index_time = np.where((time_all<tend) & (time_all>tstart) & (np.isfinite(surface_all)) & (surface_all>4) & (~np.isnan(surface_all)))[0]

# signature_rave1 = signature_rave1[index_time[0]:index_time[-1]]
# signature_rave1 = signature_rave1[~np.isnan(signature_rave1.ast) & np.isfinite(signature_rave1.ast)]

# %% SIGNATURE Rave2


# fs = 4
# dt = 1/fs

# time_all = signature_rave2.time
# surface_all = signature_rave2.ast

# tstart = datetime(year=time_all[0].year, month=time_all[0].month, day=time_all[0].day+1, hour=time_all[0].hour) #Starting time
# tend = datetime(year=time_all.iloc[-1].year, month=time_all.iloc[-1].month, day=time_all.iloc[-1].day-1, hour=time_all.iloc[-1].hour) #Ending time
# index_time = np.where((time_all<tend) & (time_all>tstart) & (np.isfinite(surface_all)) & (surface_all>4) & (~np.isnan(surface_all)))[0]

# signature_rave2 = signature_rave2[index_time[0]:index_time[-1]]
# signature_rave2 = signature_rave2[~np.isnan(signature_rave2.ast) & np.isfinite(signature_rave2.ast)]
# %% AWAC
 
# fs = 2
# dt = 1/fs

# time_all = awac_all.time
# surface_all = awac_all.ast

# tstart = datetime(year=time_all[0].year, month=time_all[0].month, day=time_all[0].day+1, hour=time_all[0].hour) #Starting time
# tend = datetime(year=time_all.iloc[-1].year, month=time_all.iloc[-1].month, day=time_all.iloc[-1].day-1, hour=time_all.iloc[-1].hour) #Ending time
# index_time = np.where((time_all<tend) & (time_all>tstart) & (np.isfinite(surface_all)) & (surface_all>4) & (~np.isnan(surface_all)))[0]

# awac = awac_all[index_time[0]:index_time[-1]]
# awac = awac[~np.isnan(awac.ast) & np.isfinite(awac.ast)]



# %%


"""
LOW PASS FILTER (remove TIDE)
"""

# %% ALL

# def butter_lowpass_filter(dataset, cutoff, fs, order):
#     nyq = fs * 0.5
#     normal_cutoff = cutoff / nyq
#     # Get the filter coefficients 
#     b, a = butter(order, normal_cutoff, btype='low', analog=False)
#     y = filtfilt(b, a, dataset)
#     return y

# cutoff = 1/300
# order = 2
# # Filter the data

# signature["tide"] = butter_lowpass_filter(signature.ast, cutoff, 4, order)
# signature["surface"] = signature.ast-signature.tide

# signature_rave1["tide"] = butter_lowpass_filter(signature_rave1.ast, cutoff, 4, order)
# signature_rave1["surface"] = signature_rave1.ast-signature_rave1.tide

# signature_rave2["tide"] = butter_lowpass_filter(signature_rave2.ast, cutoff, 4, order)
# signature_rave2["surface"] = signature_rave2.ast-signature_rave2.tide

# awac["tide"] = butter_lowpass_filter(awac.ast, cutoff, 2, order)
# awac["surface"] = awac.ast-awac.tide

# rbr_nie["tide"] = butter_lowpass_filter(rbr_nie["sea pressure"], cutoff, 4, order)
# rbr_nie["surface"] = rbr_nie["sea pressure"]-rbr_nie.tide

# rbr_trap["tide"] = butter_lowpass_filter(rbr_trap["sea pressure"], cutoff, 4, order)
# rbr_trap["surface"] = rbr_trap["sea pressure"]-rbr_trap.tide







# %%


"""   
Wave Linear Theory
"""  
# %% RBR

# hbed = 0.3 # Sensor height from bed (m)
# pres = rbr_nie.surface
# tide =rbr_nie.tide+hbed

# START = datetime(2023, 2, 8, 12,0,0)
# END = datetime(2023, 4, 5, 12,0,0)

# tstart = datetime(year=rbr_nie.time.iloc[0].year, month=rbr_nie.time.iloc[0].month, day=rbr_nie.time.iloc[0].day, hour=rbr_nie.time.iloc[0].hour, minute=0) #Starting time
# # tstart = START #Starting time
# tend = tstart + timedelta(hours=hour) #Ending time
    
# n = 0 #Counter
# appo = np.empty([0])
# while tend<=datetime(year=rbr_nie.time.iloc[-1].year, month=rbr_nie.time.iloc[-1].month, day=rbr_nie.time.iloc[-1].day, hour=rbr_nie.time.iloc[-1].hour):
# # while tend<=END:
#     print(tstart)
#     index_time = np.where((rbr_nie.time<tend) & (rbr_nie.time>tstart))[0]
#     signal = pres.iloc[n:n+len(index_time)+1]
#     h = tide.iloc[n:n+len(index_time)+1].mean() #Mean water depth in (m)
#     n = n+len(index_time)+1
#     tstart = tstart + timedelta(hours=hour)
#     tend = tend + timedelta(hours=hour)
#     sample=len(signal) #number of sample in input file
    
#     f=np.linspace(0,fs,len(signal)) #frequency
#     w=2*np.pi*f #Angular frequency

#     FFTEta = np.fft.fft(signal)

#     #Estimation of wave number (k) from Goad (2010)
#     k0=w**2/9.81 #Deep water wave number
#     k0h=k0*h
#     # kh=np.zeros(len(k0h))
#     # kh[k0h>=1]=k0h[k0h>=1]
#     # kh[k0h<1]=(k0h[k0h<1])**0.5
#     # for i in range(0,3,1):
#     #     # kh=kh-((kh-k0h*(np.tanh(kh))**-1)/(1+k0h*((np.tanh(kh))**(-2)-1))) #Calculating wave number from Goda (2010)
#     #     kh=k0h*(np.tanh(kh))**-1 #Calculating wave number from Goda (2010)
    
#     L0 = 9.81/(2*np.pi)*(1/f)**2
#     k0 = 2*np.pi/L0
#     L = L0*np.tanh(np.sinh(k0*h))
#     k = 2*np.pi/L
#     # k=kh/h #Calculating wave number from Goda (2010)
#     k[w==0]=0
    

#     #Calculation of pressure response factor
#     Kp=np.cosh(k*hbed)/np.cosh(k*h)
#     # Kp=np.cosh(-k*(h-hbed))/np.cosh(k*h)
#     kmaxL=np.pi/(h-hbed) # Wave number associated with fmaxpcorrL
#     KpminL=np.cosh(kmaxL*hbed)/np.cosh(kmaxL*h) # Minimum Limit for K_p calculated based on linear wave theory
#     Kp[Kp < KpminL] = KpminL # Check to avoid large amplification, Kp should be larger than minimum K_p calculated based on linear wave theory
       
#     Kp1=Kp[0:int(sample/2)]
#     Kp1=np.flipud(Kp1)
#     # Kp[int(sample/2):]=Kp1 #make Kp symetric around fr/2
#     Kp[len(Kp1):]=Kp1 #make Kp symetric around fr/2
    
#     #correcting pressure
#     FFTEtacor= FFTEta/Kp			    # applies corection factor
#     Eta = np.real(np.fft.ifft(FFTEtacor))	# corected water surface levels time series
#     appo = np.concatenate((appo, Eta))
#     # fig=plt.figure(figsize=(24,12))
#     # ax=fig.add_subplot(111)
#     plt.plot(f,Kp,'b.')

# START = datetime(2022, 12, 1, 12,0,0)
# END = datetime(2023, 5, 1, 12,0,0)
# index_time = np.where((rbr_nie.time<END) & (rbr_nie.time>=START))[0]
# rbr_nie["surface_corr"] = rbr_nie["surface"].copy()
# # rbr_nie["surface_corr"][index_time] = appo
# rbr_nie["surface_corr"][0:len(appo)] = appo

# del appo

# hbed = 0.3 # Sensor height from bed (m)
# pres = rbr_trap.surface
# tide =rbr_trap.tide+hbed

# START = datetime(2023, 2, 8, 12,0,0)
# END = datetime(2023, 4, 5, 12,0,0)

# tstart = datetime(year=rbr_trap.time.iloc[0].year, month=rbr_trap.time.iloc[0].month, day=rbr_trap.time.iloc[0].day, hour=rbr_trap.time.iloc[0].hour, minute=0) #Starting time
# # tstart = START #Starting time
# tend = tstart + timedelta(hours=hour) #Ending time
    
# n = 0 #Counter
# appo = np.empty([0])
# while tend<=datetime(year=rbr_trap.time.iloc[-1].year, month=rbr_trap.time.iloc[-1].month, day=rbr_trap.time.iloc[-1].day, hour=rbr_trap.time.iloc[-1].hour):
# # while tend<=END:
#     print(tstart)
#     index_time = np.where((rbr_trap.time<tend) & (rbr_trap.time>tstart))[0]
#     signal = pres.iloc[n:n+len(index_time)+1]
#     h = tide.iloc[n:n+len(index_time)+1].mean() #Mean water depth in (m)
#     n = n+len(index_time)+1
#     tstart = tstart + timedelta(hours=hour)
#     tend = tend + timedelta(hours=hour)
#     sample=len(signal) #number of sample in input file
    
#     f=np.linspace(0,fs,len(signal)) #frequency
#     w=2*np.pi*f #Angular frequency

#     FFTEta = np.fft.fft(signal)

#     #Estimation of wave number (k) from Goad (2010)
#     k0=w**2/9.81 #Deep water wave number
#     k0h=k0*h
#     # kh=np.zeros(len(k0h))
#     # kh[k0h>=1]=k0h[k0h>=1]
#     # kh[k0h<1]=(k0h[k0h<1])**0.5
#     # for i in range(0,3,1):
#     #     # kh=kh-((kh-k0h*(np.tanh(kh))**-1)/(1+k0h*((np.tanh(kh))**(-2)-1))) #Calculating wave number from Goda (2010)
#     #     kh=k0h*(np.tanh(kh))**-1 #Calculating wave number from Goda (2010)
    
#     L0 = 9.81/(2*np.pi)*(1/f)**2
#     k0 = 2*np.pi/L0
#     L = L0*np.tanh(np.sinh(k0*h))
#     k = 2*np.pi/L
#     # k=kh/h #Calculating wave number from Goda (2010)
#     k[w==0]=0
    

#     #Calculation of pressure response factor
#     Kp=np.cosh(k*hbed)/np.cosh(k*h)
#     # Kp=np.cosh(-k*(h-hbed))/np.cosh(k*h)
#     kmaxL=np.pi/(h-hbed) # Wave number associated with fmaxpcorrL
#     KpminL=np.cosh(kmaxL*hbed)/np.cosh(kmaxL*h) # Minimum Limit for K_p calculated based on linear wave theory
#     Kp[Kp < KpminL] = KpminL # Check to avoid large amplification, Kp should be larger than minimum K_p calculated based on linear wave theory
       
#     Kp1=Kp[0:int(sample/2)]
#     Kp1=np.flipud(Kp1)
#     # Kp[int(sample/2):]=Kp1 #make Kp symetric around fr/2
#     Kp[len(Kp1):]=Kp1 #make Kp symetric around fr/2
    
#     #correcting pressure
#     FFTEtacor= FFTEta/Kp			    # applies corection factor
#     Eta = np.real(np.fft.ifft(FFTEtacor))	# corected water surface levels time series
#     appo = np.concatenate((appo, Eta))
#     # fig=plt.figure(figsize=(24,12))
#     # ax=fig.add_subplot(111)
#     plt.plot(f,Kp,'b.')

# START = datetime(2022, 12, 1, 12,0,0)
# END = datetime(2023, 5, 1, 12,0,0)
# index_time = np.where((rbr_trap.time<END) & (rbr_trap.time>=START))[0]
# rbr_trap["surface_corr"] = rbr_trap["surface"].copy()
# # rbr_trap["surface_corr"][index_time] = appo
# rbr_trap["surface_corr"][0:len(appo)] = appo





# %%


"""   
FAST FOURIER TRANSFORMATION
"""
# %% FOURIER ALL

fmin =  1/300
fsep = 1/16.87 
# fsep = 1/500
fmax = 1

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

    #Create dictionary
    result = {}
    result['energy'] = energy[index]
    result['frequency'] = fre[index]
    result['Hm0'] = Hm0
    result['Tp'] = Tp
    
    return result

# adcp = fourier(data.ast, fmin, fmax, fs)

# %% FOURIER per WINDOWS

from datetime import datetime, timedelta
from scipy.fft import fft, fftfreq

#INPUT
fmin =  1/300
fsep = 1/30 
# fsep = 1/500
fmax = 1
hour = 3 #Window size

def fourier_windows(data, surface, hour, fmin, fsep, fmax, fs):
    
    START = datetime(2023, 2, 8, 12,0,0)
    END = datetime(2023, 4, 5, 12,0,0)
    
    tstart = datetime(year=data.time.iloc[0].year, month=data.time.iloc[0].month, day=data.time.iloc[0].day, hour=data.time.iloc[0].hour, minute=0) #Starting time
    # tstart = START #Starting time
    tend = tstart + timedelta(hours=hour) #Ending time
    
    
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
    # wave["velN"] = []
    # wave["vel"] = []
    while tend<datetime(year=data.time.iloc[-1].year, month=data.time.iloc[-1].month, day=data.time.iloc[-1].day, hour=data.time.iloc[-1].hour):
    # while tend<END:
        print(tstart)
        tstart = tstart + timedelta(hours=hour)
        tend = tend + timedelta(hours=hour)
        index_time = np.where((data.time<tend) & (data.time>tstart))[0]
        if len(index_time)>0:
            window = surface.iloc[index_time]
            
        # IG WAVES
        appo = fourier(window,fmin,fsep,fs)
        wave["time"].append(tstart)
        wave["Hm0,IG"].append(appo["Hm0"])
        wave["Tp,IG"].append(appo["Tp"])
        wave["frequency,IG"].append(appo["frequency"])
        wave["energy,IG"].append(appo["energy"])
        # SS WAVES
        appo = fourier(window,fsep,fmax,fs)
        wave["Hm0,SS"].append(appo["Hm0"])
        wave["Tp,SS"].append(appo["Tp"])
        wave["frequency,SS"].append(appo["frequency"])
        wave["energy,SS"].append(appo["energy"])
               
        # avg_tide = data.tide.iloc[index_time].mean()
        # wave["tide"].append(avg_tide)

        # avg_dir = data.direction.iloc[index_time].mean()
        # wave["direction"].append(avg_dir)
        
    return wave

print("START")
# awac_wave = fourier_windows(awac, awac.surface, hour, fmin, fsep, fmax, 2)
# print("AWAC")
# signa_wave = fourier_windows(signature, signature.surface, hour, fmin, fsep, fmax, 4)
# print("SIGNATURE Trap")
# signa_wave_rave1 = fourier_windows(signature_rave1, signature_rave1.surface, hour, fmin, fsep, fmax, 4)
# print("SIGNATURE Rave1")
# signa_wave_rave2 = fourier_windows(signature_rave2, signature_rave2.surface, hour, fmin, fsep, fmax, 4)
# print("SIGNATURE Rave2")
# rbr_trap_wave = fourier_windows(rbr_trap, rbr_trap.surface, hour, fmin, fsep, fmax, 4)
# print("PS TRAP")
# rbr_nie_wave = fourier_windows(rbr_nie, rbr_nie.surface, hour, fmin, fsep, fmax, 4)
# print("PS NIE")
# rbr_trap_wave_corr = fourier_windows(rbr_trap, rbr_trap.surface_corr, hour, fmin, fsep, fmax, 4)
# print("PS TRAP + WLT")
# rbr_nie_wave_corr = fourier_windows(rbr_nie, rbr_nie.surface_corr, hour, fmin, fsep, fmax, 4)
# print("PS NIE + WLT")
# print("END")

# Saving the objects:
f = open('WAVE_ALL.pckl', 'wb')
pickle.dump([awac_wave, signa_wave, rbr_trapegeer_wave, 
              rbr_nieuwport_wave, rbr_trapegeer_wave_corr, rbr_nieuwport_wave_corr, signa_wave_rave1, signa_wave_rave2], f)
f.close()




# %%

START = datetime(2022, 12, 23, 1,0,0)
END = datetime(2023, 1, 8, 4,0,0)

index = np.where((result.time<END) & (result.time>START))[0]

appo = result.iloc[index]

# %%

fig=plt.figure(figsize=(36,24))
ax=fig.add_subplot(111)
plt.plot(result1.time, result1.ast,'.')


















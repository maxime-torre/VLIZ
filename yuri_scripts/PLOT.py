# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 10:52:08 2023

@author: yuri.pepi
"""

# %% 
"""   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
PLOT DATA
"""  '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
# %%
"""   
PLOT SENSORS
""" 

# %%
FS = 25
def plot(a,b):
    ax.set_ylim(a, b)
    # ax.set_xlim(datetime(2022, 9, 1, 12,0,0), datetime(2022, 9, 1, 12, 3)) #yyy, m, d
    ax.tick_params(axis='both', which='major', labelsize=FS)
    ax.legend(loc=4,fontsize=FS)
    plt.grid(True)
    plt.grid(b=True, which='minor', color='gray',linestyle='--')
    myFmt = mdates.DateFormatter('%b-%d %H:%M')
    ax.xaxis.set_major_formatter(myFmt)
    # plt.show()
    fig.tight_layout()



fig=plt.figure(figsize=(36,24))
ax=fig.add_subplot(211)
plt.title("ADCP Signature1000 - 4 Hz", fontsize = 1.3*FS)
plt.plot(signature.time,signature.ast, color='#2CA02C', label="Acoustic Surface Tracking (AST)")
plt.plot(signature.time,signature.tide,'--', c="gray", linewidth=3, label="Long components")
ymajor_ticks = np.arange(0, 16, 2)
yminor_ticks = np.arange(0, 16, 0.5)
ax.set_yticks(ymajor_ticks)
ax.set_yticks(yminor_ticks, minor=True)
plot(0, 16)
plt.ylabel(r" $h_0$ [m]",fontsize=1.5*FS)

ax=fig.add_subplot(212)
plt.plot(signature.time, signature.surface,'#2CA02C', label="Water surface elevation from AST")
ymajor_ticks = np.arange(-6, 6, 1.5)
yminor_ticks = np.arange(-6, 6, 0.5)
ax.set_yticks(ymajor_ticks)
ax.set_yticks(yminor_ticks, minor=True)
plot(-4, 4)
# plt.xlabel(r"Date [mm-day hr]",fontsize=1.5*FS)
plt.ylabel(r" $\eta$  [m]",fontsize=1.5*FS)

print("SIGNATURE")
"""  '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%' """

fig=plt.figure(figsize=(36,24))
ax=fig.add_subplot(211)
plt.title("ADCP AWAC 1MHz - 2 Hz", fontsize = 1.3*FS)
plt.plot(awac.time,awac.ast, color='#1F77B4', label="Acoustic Surface Tracking (AST)")
plt.plot(awac.time,awac.tide,'--', c="gray", linewidth=3, label="Long components")
ymajor_ticks = np.arange(0, 16, 2)
yminor_ticks = np.arange(0, 16, 0.5)
ax.set_yticks(ymajor_ticks)
ax.set_yticks(yminor_ticks, minor=True)
plot(0, 16)
plt.ylabel(r" $h_0$ [m]",fontsize=1.5*FS)

ax=fig.add_subplot(212)
plt.plot(awac.time, awac.surface,'#1F77B4', label="Water surface elevation from AST")
ymajor_ticks = np.arange(-6, 6, 1.5)
yminor_ticks = np.arange(-6, 6, 0.5)
ax.set_yticks(ymajor_ticks)
ax.set_yticks(yminor_ticks, minor=True)
plot(-4, 4)
# plt.xlabel(r"Date [mm-day hr]",fontsize=1.5*FS)
plt.ylabel(r" $\eta$  [m]",fontsize=1.5*FS)

print("AWAC")
"""  '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%' """
fig=plt.figure(figsize=(36,24))
ax=fig.add_subplot(211)
plt.title("PS Quartz3 - 4 Hz (AWAC)", fontsize = 1.3*FS)
plt.plot(rbr_nie.time,rbr_nie["sea pressure"],   '--', color='darkorange', label="Acoustic Surface Tracking (AST)")
plt.plot(rbr_nie.time,rbr_nie.tide,'--', c="gray", linewidth=3, label="Long components")
ymajor_ticks = np.arange(0, 16, 2)
yminor_ticks = np.arange(0, 16, 0.5)
ax.set_yticks(ymajor_ticks)
ax.set_yticks(yminor_ticks, minor=True)
plot(0, 16)
plt.ylabel(r" $h_0$ [m]",fontsize=1.5*FS)

ax=fig.add_subplot(212)
plt.plot(rbr_nie.time, rbr_nie.surface,  '--', color='darkorange', label="Water surface elevation from AST")
ymajor_ticks = np.arange(-6, 6, 1.5)
yminor_ticks = np.arange(-6, 6, 0.5)
ax.set_yticks(ymajor_ticks)
ax.set_yticks(yminor_ticks, minor=True)
plot(-4, 4)
# plt.xlabel(r"Date [mm-day hr]",fontsize=1.5*FS)
plt.ylabel(r" $\eta$  [m]",fontsize=1.5*FS)

print("PS1")
"""  '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%' """

fig=plt.figure(figsize=(36,24))
ax=fig.add_subplot(211)
plt.title("PS Quartz3 - 4 Hz (Signature)", fontsize = 1.3*FS)
plt.plot(rbr_trap.time,rbr_trap["sea pressure"],   ':', color='darkorange', label="Acoustic Surface Tracking (AST)")
plt.plot(rbr_trap.time,rbr_trap.tide,'--', c="gray", linewidth=3, label="Long components")
ymajor_ticks = np.arange(0, 16, 2)
yminor_ticks = np.arange(0, 16, 0.5)
ax.set_yticks(ymajor_ticks)
ax.set_yticks(yminor_ticks, minor=True)
plot(0, 16)
plt.ylabel(r" $h_0$ [m]",fontsize=1.5*FS)

ax=fig.add_subplot(212)
plt.plot(rbr_trap.time, rbr_trap.surface,  ':', color='darkorange', label="Water surface elevation from AST")
ymajor_ticks = np.arange(-6, 6, 1.5)
yminor_ticks = np.arange(-6, 6, 0.5)
ax.set_yticks(ymajor_ticks)
ax.set_yticks(yminor_ticks, minor=True)
plot(-4, 4)
# plt.xlabel(r"Date [mm-day hr]",fontsize=1.5*FS)
plt.ylabel(r" $\eta$  [m]",fontsize=1.5*FS)
print("PS2")
# %%
# %%
"""   
COMPARISON ADCP vs WAVE BUOY
""" 

# %%

def plot(ax, a, b, ylabel, y_major_ticks, y_minor_ticks):
    ax.tick_params(axis='both', which='major', labelsize=FS)
    ax.legend(loc=4, fontsize=FS)
    plt.grid(True)
    plt.grid(b=True, which='minor', color='gray', linestyle='--')
    myFmt = mdates.DateFormatter('%b-%d %H:%M')
    ax.xaxis.set_major_formatter(myFmt)
    ax.tick_params(axis='x', which='major', pad=25)
    ax.tick_params(axis='y', which='major', pad=25)
    ax.set_yticks(y_major_ticks)
    ax.set_yticks(y_minor_ticks, minor=True)
    plt.ylabel(ylabel, fontsize=1.5 * FS, labelpad=20)
    ax.legend(loc=2, fontsize=FS)    
    ax.set_ylim(a, b)
    ax.set_xlim(datetime(2022, 12, 14, 12, 0, 0), datetime(2023, 4, 5, 12, 0))
    
    fig.tight_layout()


"""
"""

# Define variables
FS = 30
LW = 3
y_major_ticks = np.arange(0, 6, 0.5)
y_minor_ticks = np.arange(0, 6, 0.25)

fig = plt.figure(figsize=(36, 18))
# Subplot 1
ax1 = fig.add_subplot(211)
# ax1.plot(west['time'], west['Hm'], '-.', color='gray', label="Westhinder buoy", linewidth=LW)
# ax1.plot(nieu['time'], nieu['Hm'], '-.', color='m', label="Nieuwpoort buoy", linewidth=LW)
ax1.plot(np.array(awac_wave['time']), awac_wave['Hm0,SS'], '#1F77B4', label="AWAC 1MHz", linewidth=LW*1.1)
ax1.plot(np.array(rbr_nie_wave_corr['time']), rbr_nie_wave_corr['Hm0,SS'], '--', color='k', label="Quartz3 + WLT - AWAC", linewidth=LW*1.1)

plot(ax1, 0, 3, r" $H_{m0, SS}$ [m]", y_major_ticks, y_minor_ticks)


# Define variables
FS = 30
LW = 3
y_major_ticks = np.arange(0, 6, 0.5)
y_minor_ticks = np.arange(0, 6, 0.25)

fig = plt.figure(figsize=(36, 18))
# Subplot 1
ax1 = fig.add_subplot(211)
# ax1.plot(west['time'], west['Hm'], '-.', color='gray', label="Westhinder buoy", linewidth=LW)
# ax1.plot(nieu['time'], nieu['Hm'], '-.', color='m', label="Nieuwpoort buoy", linewidth=LW)
# ax1.plot(rave1['time'], rave1['Hm'], '-.', color='m', label="Raversijde buoy", linewidth=LW)
# ax1.plot(np.array(awac_wave['time']), awac_wave['Hm0,SS'], '#1F77B4', label="AWAC 1MHz", linewidth=LW*1.1)
# ax1.plot(np.array(rbr_nie_wave_corr['time']), rbr_nie_wave_corr['Hm0,SS'], '--', color='k', label="Quartz3 + WLT - AWAC", linewidth=LW*1.1)
# ax1.plot(np.array(rbr_nie_wave_corr['time']), rbr_nie_wave_corr['Hm0,SS'], '--', color='k', label="Quartz3 + WLT - AWAC", linewidth=LW*1.1)
ax1.plot(np.array(signa_wave_rave1['time']), signa_wave_rave1['Hm0,SS'], ':', color='k', label="SIGNATURE 1000 - Raversijde1", linewidth=LW*1.1)
ax1.plot(np.array(signa_wave_rave2['time']), signa_wave_rave2['Hm0,SS'], '--', color='r', label="SIGNATURE 1000 - Raversijde2", linewidth=LW*1.1)

# appo=np.array(rbr_nie_wave_corr['Hm0,SS'])/np.array(rbr_nie_wave_corr['Hm0,SS'])

plot(ax1, 0, 4, r" $H_{m0, SS}$ [m]", y_major_ticks, y_minor_ticks)

# Subplot 2
ax2 = fig.add_subplot(212)
# ax2.plot(west['time'], west['Hm'], '-.', color='gray', label="Westhinder buoy", linewidth=LW)
# ax2.plot(trap['time'], trap['Hm'], '-.', color='m', label="Trapegeer buoy", linewidth=LW)
# ax2.plot(np.array(signa_wave['time']), signa_wave['Hm0,SS'], '#2CA02C', label="SIGNATURE 1000", linewidth=LW*1.1)
# ax2.plot(np.array(rbr_trap_wave_corr['time']), rbr_trap_wave_corr['Hm0,SS'], ':', color='k', label="Quartz3 + WLT - SIGNATURE", linewidth=LW*1.1)

plot(ax2, 0, 4, r" $H_{m0, SS}$ [m]", y_major_ticks, y_minor_ticks)





# Subplot 2
ax2 = fig.add_subplot(212)
# ax2.plot(west['time'], west['Hm'], '-.', color='gray', label="Westhinder buoy", linewidth=LW)
# ax2.plot(trap['time'], trap['Hm'], '-.', color='m', label="Trapegeer buoy", linewidth=LW)
ax2.plot(np.array(signa_wave['time']), signa_wave['Hm0,SS'], '#2CA02C', label="SIGNATURE 1000", linewidth=LW*1.1)
ax2.plot(np.array(rbr_trap_wave_corr['time']), rbr_trap_wave_corr['Hm0,SS'], ':', color='k', label="Quartz3 + WLT - SIGNATURE", linewidth=LW*1.1)

plot(ax2, 0, 3, r" $H_{m0, SS}$ [m]", y_major_ticks, y_minor_ticks)
"""
# %% WAVE PERIOD
"""

fig = plt.figure(figsize=(36, 18))
# Subplot 1
y_major_ticks = np.arange(0, 32, 4)
y_minor_ticks = np.arange(0, 32, 2)
ax1 = fig.add_subplot(211)
# ax1.plot(west['time'], west['Hm'], '-.', color='gray', label="Westhinder buoy", linewidth=LW)
# ax1.plot(nieu['time'], nieu['Hm'], '-.', color='m', label="Nieuwpoort buoy", linewidth=LW)
ax1.plot(np.array(awac_wave['time']), awac_wave['Tp,SS'], '#1F77B4', label="AWAC 1MHz", linewidth=LW*1.1)
ax1.plot(np.array(rbr_nie_wave_corr['time']), rbr_nie_wave_corr['Tp,SS'], '--', color='k', label="Quartz3 + WLT - AWAC", linewidth=LW*1.1)

plot(ax1, 0, 24, r" $T_{p, SS}$ [s]", y_major_ticks, y_minor_ticks)

# Subplot 2

ax2 = fig.add_subplot(212)
# ax2.plot(west['time'], west['Tm'], '-.', color='gray', label="Westhinder buoy", linewidth=LW)
# ax2.plot(trap['time'], trap['Hm'], '-.', color='m', label="Trapegeer buoy", linewidth=LW)
ax2.plot(np.array(signa_wave['time']), signa_wave['Tp,SS'], '#2CA02C', label="SIGNATURE 1000", linewidth=LW*1.1)
ax2.plot(np.array(rbr_trap_wave_corr['time']), rbr_trap_wave_corr['Tp,SS'], ':', color='k', label="Quartz3 + WLT - SIGNATURE", linewidth=LW*1.1)

plot(ax2, 0, 24, r" $T_{p, SS}$ [s]", y_major_ticks, y_minor_ticks)

# %%

"""
# %% WAVE HEIGHT
"""

# Define variables
FS = 30
LW = 3
y_major_ticks = np.arange(0, 6, 0.5)/10
y_minor_ticks = np.arange(0, 6, 0.25)/10

fig = plt.figure(figsize=(36, 18))
# Subplot 1
ax1 = fig.add_subplot(211)
# ax1.plot(west['time'], west['Hm'], '-.', color='gray', label="Westhinder buoy", linewidth=LW)
# ax1.plot(nieu['time'], nieu['Hm'], '-.', color='m', label="Nieuwpoort buoy", linewidth=LW)
# ax1.plot(np.array(awac_wave['time']), awac_wave['Hm0,IG'], '#1F77B4', label="AWAC 1MHz", linewidth=LW*1.1)
# ax1.plot(np.array(rbr_nie_wave_corr['time']), rbr_nie_wave_corr['Hm0,IG'], '--', color='k', label="Quartz3 + WLT - AWAC", linewidth=LW*1.1)

plot(ax1, 0, 0.3, r" $H_{m0, IG}$ [m]", y_major_ticks, y_minor_ticks)

# Subplot 2
ax2 = fig.add_subplot(212)
# ax2.plot(west['time'], west['Hm'], '-.', color='gray', label="Westhinder buoy", linewidth=LW)
# ax2.plot(trap['time'], trap['Hm'], '-.', color='m', label="Trapegeer buoy", linewidth=LW)
ax2.plot(np.array(signa_wave['time']), signa_wave['Hm0,IG'], '#2CA02C', label="SIGNATURE 1000", linewidth=LW*1.1)
ax2.plot(np.array(rbr_trap_wave_corr['time']), rbr_trap_wave_corr['Hm0,IG'], ':', color='k', label="Quartz3 + WLT - SIGNATURE", linewidth=LW*1.1)

plot(ax2, 0, .3, r" $H_{m0, SS}$ [m]", y_major_ticks, y_minor_ticks)



"""
# %% WAVE PERIOD
"""

fig = plt.figure(figsize=(36, 18))
# Subplot 1
y_major_ticks = np.arange(0, 32, 4)*10
y_minor_ticks = np.arange(0, 32, 2)*10
ax1 = fig.add_subplot(211)
# ax1.plot(west['time'], west['Hm'], '-.', color='gray', label="Westhinder buoy", linewidth=LW)
# ax1.plot(nieu['time'], nieu['Hm'], '-.', color='m', label="Nieuwpoort buoy", linewidth=LW)
ax1.plot(np.array(awac_wave['time']), awac_wave['Tp,IG'], '#1F77B4', label="AWAC 1MHz", linewidth=LW*1.1)
ax1.plot(np.array(rbr_nie_wave_corr['time']), rbr_nie_wave_corr['Tp,IG'], '--', color='k', label="Quartz3 + WLT - AWAC", linewidth=LW*1.1)

plot(ax1, 0, 320, r" $T_{p, SS}$ [s]", y_major_ticks, y_minor_ticks)

# Subplot 2

ax2 = fig.add_subplot(212)
# ax2.plot(west['time'], west['Hm'], '-.', color='gray', label="Westhinder buoy", linewidth=LW)
# ax2.plot(trap['time'], trap['Hm'], '-.', color='m', label="Trapegeer buoy", linewidth=LW)
ax2.plot(np.array(signa_wave['time']), signa_wave['Tp,IG'], '#2CA02C', label="SIGNATURE 1000", linewidth=LW*1.1)
ax2.plot(np.array(rbr_trap_wave_corr['time']), rbr_trap_wave_corr['Tp,IG'], ':', color='k', label="Quartz3 + WLT - SIGNATURE", linewidth=LW*1.1)

plot(ax2, 0, 320, r" $T_{p, SS}$ [s]", y_major_ticks, y_minor_ticks)


# %%
# f = np.array(signa_wave["frequency,SS"])[0]
# t = np.array(signa_wave["time"])
# Sxx = np.transpose(np.array(signa_wave["energy,SS"]), (1, 0))
# t = np.array(signa_wave["time"])[0:-1]
# fSS = np.array(signa_wave["frequency,SS"])[0]
# SxxSS = np.transpose(signa_wave["energy,SS"][0:-1])
# fIG = np.array(signa_wave["frequency,IG"])[0]
# SxxIG = np.transpose(signa_wave["energy,IG"][0:-1])

t = np.array(awac_wave["time"])[0:-1]
fSS = np.array(awac_wave["frequency,SS"])[0]
SxxSS = np.transpose(awac_wave["energy,SS"][0:-1])
fIG = np.array(awac_wave["frequency,IG"])[0]
SxxIG = np.transpose(awac_wave["energy,IG"][0:-1])
   
    
def plot_spectrogram(ax):
    plt.ylabel('Frequency [Hz]', fontsize=1.5 * FS, labelpad=20)
    plt.xlabel('Time', fontsize=1.5 * FS, labelpad=20)
    # cb.set_label('Energy [$m^2/s$]', fontsize=1.5 * FS, labelpad=20)
    # Set the colorbar label font size
    # cb.set_label('Amplitude', fontsize=FS)
    ax.tick_params(axis='both', which='major', labelsize=FS)
    # cb.ax.tick_params(labelsize=FS)
    myFmt = mdates.DateFormatter('%b-%d %H:%M')
    ax.xaxis.set_major_formatter(myFmt)
    ax.set_xlim(datetime(2023, 2, 16, 12, 0, 0), datetime(2023, 4, 5, 12, 0))
    ax.set_ylim(0, 1)
    plt.show()

def plot(ax, a, b, ylabel, y_major_ticks, y_minor_ticks):
    ax.tick_params(axis='both', which='major', labelsize=FS)
    ax.legend(loc=4, fontsize=FS, ncol=2)
    plt.grid(True)
    plt.grid(b=True, which='minor', color='gray', linestyle='--')
    myFmt = mdates.DateFormatter('%b-%d %H:%M')
    ax.xaxis.set_major_formatter(myFmt)
    ax.tick_params(axis='x', which='major', pad=25)
    ax.tick_params(axis='y', which='major', pad=25)
    ax.set_yticks(y_major_ticks)
    ax.set_yticks(y_minor_ticks, minor=True)
    plt.ylabel(ylabel, fontsize=1.5 * FS, labelpad=20)
    ax.legend(loc=2, fontsize=FS)    
    ax.set_ylim(a, b)
    ax.set_xlim(datetime(2023, 2, 16, 12, 0, 0), datetime(2023, 3, 16, 12, 0))
    
    fig.tight_layout()

# Define variables
FS = 30
LW = 3
y_major_ticks = np.arange(0, 6, 0.8)
y_minor_ticks = np.arange(0, 6, 0.25)

fig = plt.figure(figsize=(36, 18))
# Subplot 1
ax1 = fig.add_subplot(511)
# ax1.plot(west['time'], west['Hm'], '-.', color='gray', label="Westhinder buoy", linewidth=LW)
# ax1.plot(kwin['time'], kwin['Hm'], '-.', color='salmon', label="Kwintebank buoy", linewidth=LW)
# ax1.plot(nieu['time'], nieu['Hm'], '-.', color='m', label="Nieuwpoort buoy", linewidth=LW)
ax1.plot(np.array(awac_wave['time']), awac_wave['Hm0,SS'], '#1F77B4', label="ADCP - Nieuwpoort", linewidth=LW*1.1)
ax1.plot(np.array(signa_wave['time']), signa_wave['Hm0,SS'], 'k', label="ADCP - Trapegeer", linewidth=LW*1.1, alpha=0.5)
ax1.plot(np.array(signa_wave_rave1['time']), signa_wave_rave1['Hm0,SS'], 'y', label="ADCP - Raversijde 1", linewidth=LW*1.1)
ax1.plot(np.array(signa_wave_rave2['time']), signa_wave_rave2['Hm0,SS'], 'darkorange', label="ADCP - Raversijde 2", linewidth=LW*1.1)
# ax1.plot(np.array(rbr_nie_wave_corr['time']), rbr_nie_wave_corr['Hm0,SS'], '--', color='k', label="Quartz3 + WLT - AWAC", linewidth=LW*1.1)
plot(ax1, 0, 4, r" $H_{m0, SS}$ [m]", y_major_ticks, y_minor_ticks)

# Subplot 2
ax2 = fig.add_subplot(512)
# ax1.plot(west['time'], west['Hm'], '-.', color='gray', label="Westhinder buoy", linewidth=LW)
# ax1.plot(nieu['time'], nieu['Hm'], '-.', color='m', label="Nieuwpoort buoy", linewidth=LW)
# ax2.plot(np.array(awac_wave['time']), awac_wave['Hm0,IG'], '#1F77B4', label="AWAC 1MHz", linewidth=LW*1.1)
ax2.plot(np.array(rbr_nie_wave_corr['time']), rbr_nie_wave_corr['Hm0,IG'], ':', color='#1F77B4', label="PS - Nieuwpoort", linewidth=LW*1.1)
ax2.plot(np.array(rbr_trap_wave_corr['time']), rbr_trap_wave_corr['Hm0,IG'], '--', color='k', label="PS - Trapegeer", linewidth=LW*1.1)

plot(ax2, 0, 0.4, r" $H_{m0, IG}$ [m]", y_major_ticks/10, y_minor_ticks/10)


# Subplot 3
y_major_ticks = np.arange(0, 32, 6)
y_minor_ticks = np.arange(0, 32, 2)
ax3 = fig.add_subplot(513)
ax3.plot(np.array(awac_wave['time']), awac_wave['Tp,SS'], '#1F77B4', label="ADCP - Nieuwpoort", linewidth=LW*1.1)
ax3.plot(np.array(signa_wave['time']), np.array(signa_wave['Tp,SS'])+2, 'k', label="ADCP - Trapegeer", linewidth=LW*1.1)
ax3.plot(np.array(signa_wave_rave1['time']), signa_wave_rave1['Tp,SS'], 'y', label="ADCP - Raversijde 1", linewidth=LW*1.1)
ax3.plot(np.array(signa_wave_rave2['time']), signa_wave_rave2['Tp,SS'], 'darkorange', label="ADCP - Raversijde 2", linewidth=LW*1.1)
# ax3.plot(np.array(rbr_nie_wave_corr['time']), rbr_nie_wave_corr['Tp,SS'], '--', color='k', label="Quartz3 + WLT - AWAC", linewidth=LW*1.1)

plot(ax3, 0, 20, r" $T_{p, SS}$ [s]", y_major_ticks, y_minor_ticks)

# Subplot 4
# y_major_ticks = np.arange(0, 360, 40)
# y_minor_ticks = np.arange(0, 360, 20)
# ax4 = fig.add_subplot(514)
# ax4.plot(west['time'], west['dirlow'], '-.', color='gray', label="Westhinder buoy", linewidth=LW)
# # ax3.plot(np.array(rbr_nie_wave_corr['time']), rbr_nie_wave_corr['Tp,SS'], '--', color='k', label="Quartz3 + WLT - AWAC", linewidth=LW*1.1)
# plot(ax4, 0, 360, r" $Dir, SS$ [deg]", y_major_ticks, y_minor_ticks)
# ax4.legend(loc=3, fontsize=FS)

y_major_ticks = np.arange(0, 360, 60)
y_minor_ticks = np.arange(0, 360, 20)
ax4 = fig.add_subplot(514)
ax4.plot(np.array(rbr_nie_wave_corr['time']), rbr_nie_wave_corr['Tp,IG'], ':', color='#1F77B4', label="PS - Nieuwpoort", linewidth=LW*1.1)
ax4.plot(np.array(rbr_trap_wave_corr['time']), rbr_trap_wave_corr['Tp,IG'], '--', color='k', label="PS - Trapegeer", linewidth=LW*1.1)
plot(ax4, 0, 320, r" $T_{p, IG}$ [s]", y_major_ticks, y_minor_ticks)
ax4.legend(loc=3, fontsize=FS)


# Subplot 5
ax5 = fig.add_subplot(515)
# Plot the spectrogram
img = ax5.pcolormesh(t, fIG, SxxIG, cmap='viridis', vmin=0, vmax=0.05)
img = ax5.pcolormesh(t, fSS, SxxSS, cmap='viridis', vmin=0, vmax=0.05)
plot_spectrogram(ax5)
# %%COMPARISON WAVE BUOYS

# Define variables
FS = 30
LW = 3
alp = 0.8
y_major_ticks = np.arange(0, 6, 0.8)
y_minor_ticks = np.arange(0, 6, 0.2)
START = datetime(2023, 2, 16, 12, 0, 0)
END = datetime(2023, 3, 16, 12, 0)


fig = plt.figure(figsize=(36, 18))
# Subplot 1
index_adcp = np.where((np.array(signa_wave['time'])<END) & (np.array(signa_wave['time'])>START))[0]   
index_buoy = np.where((trap['time']<END) & (trap['time']>=START))[0]    
diff = trap['Hm'][index_buoy] - np.array(signa_wave['Hm0,SS'])[index_adcp]

ax1 = fig.add_subplot(411)
ax1.plot(trap['time'], trap['Hm'], '--', color='k', label="Trapegeer buoy", linewidth=LW)
ax1.plot(np.array(signa_wave['time']), signa_wave['Hm0,SS'], 'k', label="ADCP - Trapegeer", linewidth=LW*1.1, alpha=alp)
ax1.plot(trap['time'][index_buoy], diff, ':', color='darkorange', linewidth=LW)
plot(ax1, -0.1, 4, r" $H_{m0, SS}$ [m]", y_major_ticks, y_minor_ticks)

# Subplot 2
index_adcp = np.where((np.array(awac_wave['time'])<END) & (np.array(awac_wave['time'])>START))[0]   
index_buoy = np.where((nieu['time']<END) & (nieu['time']>=START))[0]    
diff = nieu['Hm'][index_buoy] - np.array(awac_wave['Hm0,SS'])[index_adcp]

ax2 = fig.add_subplot(412)
ax2.plot(nieu['time'], nieu['Hm'], '--', color='k', label="Nieuwpoort buoy", linewidth=LW)
ax2.plot(np.array(awac_wave['time']), awac_wave['Hm0,SS'], '#1F77B4', label="ADCP - Nieuwpoort", linewidth=LW*1.1, alpha=alp)
ax2.plot(nieu['time'][index_buoy], diff, ':', color='darkorange', linewidth=LW)
plot(ax2, -0.1, 4, r" $H_{m0, SS}$ [m]", y_major_ticks, y_minor_ticks)

# ax1.plot(np.array(signa_wave_rave1['time']), signa_wave_rave1['Hm0,SS'], 'y', label="ADCP - Raversijde 1", linewidth=LW*1.1)

# Subplot 3
index_adcp = np.where((np.array(signa_wave_rave1['time'])<END) & (np.array(signa_wave_rave1['time'])>START))[0]   
index_buoy = np.where((rave1['time']<END) & (rave1['time']>START))[0]    
diff = rave1['Hm'][index_buoy] - np.array(signa_wave_rave1['Hm0,SS'])[index_adcp]

ax3 = fig.add_subplot(413)
ax3.plot(rave1['time'], rave1['Hm'], '--', color='k', label="Raversijde 1 buoy", linewidth=LW)
ax3.plot(np.array(signa_wave_rave1['time']), signa_wave_rave1['Hm0,SS'], 'y', label="ADCP - Raversijde 1", linewidth=LW*1.1)
ax3.plot(rave1['time'][index_buoy], diff, ':', color='darkorange', linewidth=LW)
plot(ax3, -0.1, 4, r" $H_{m0, SS}$ [m]", y_major_ticks, y_minor_ticks)

# Subplot 4
index_adcp = np.where((np.array(signa_wave_rave2['time'])<END) & (np.array(signa_wave_rave2['time'])>=START))[0] 
index_buoy = np.where((rave2['time']<END) & (rave2['time']>=START))[0]    
diff = nieu['Hm'][index_buoy] - np.array(signa_wave_rave2['Hm0,SS'])[index_adcp]

ax4 = fig.add_subplot(414)
ax4.plot(rave1['time'], rave1['Hm'], '--', color='k', label="Raversijde 2 buoy", linewidth=LW)
ax4.plot(np.array(signa_wave_rave2['time']), signa_wave_rave2['Hm0,SS'], 'darkorange', label="ADCP - Raversijde 2", linewidth=LW*1.1)
ax4.plot(rave2['time'][index_buoy], diff, ':', color='darkorange', linewidth=LW)
plot(ax4, -0.1, 4, r" $H_{m0, SS}$ [m]", y_major_ticks, y_minor_ticks)

# %%TOTAL WAVE HEIGHT
def plot(ax, a, b, ylabel, y_major_ticks, y_minor_ticks):
    ax.tick_params(axis='both', which='major', labelsize=FS)
    ax.legend(loc=4, fontsize=FS, ncol=2)
    plt.grid(True)
    plt.grid(b=True, which='minor', color='gray', linestyle='--')
    myFmt = mdates.DateFormatter('%b-%d')
    ax.xaxis.set_major_formatter(myFmt)
    ax.tick_params(axis='x', which='major', pad=25)
    ax.tick_params(axis='y', which='major', pad=25)
    ax.set_yticks(y_major_ticks)
    ax.set_yticks(y_minor_ticks, minor=True)
    plt.ylabel(ylabel, fontsize=1.5 * FS, labelpad=20)
    ax.legend(loc=1, fontsize=FS)    
    ax.set_ylim(a, b)
    # ax.set_xlim(datetime(2023, 2, 18, 12, 0, 0), datetime(2023, 2, 23, 12, 0))
    ax.set_xlim(datetime(2023, 3, 1, 12, 0, 0), datetime(2023, 3, 9, 12, 0))
    
    fig.tight_layout()

# Define variables
FS = 30
LW = 3
y_major_ticks = np.arange(0, 6, 0.4)
y_minor_ticks = np.arange(0, 6, 0.2)
START = datetime(2023, 2, 18, 12, 0, 0)
END = datetime(2023, 2, 23, 12, 0, 0)
index_adcp = np.where((np.array(awac_wave['time'])<END) & (np.array(awac_wave['time'])>START))[0]   
index_ps = np.where((np.array(rbr_nie_wave_corr['time'])<END) & (np.array(rbr_nie_wave_corr['time'])>START))[0]   
    
fig = plt.figure(figsize=(30, 14))
# Subplot 1
ax1 = fig.add_subplot(221)
# ax1.plot(west['time'], west['Hm'], '-.', color='gray', label="Westhinder buoy", linewidth=LW)
# ax1.plot(kwin['time'], kwin['Hm'], '-.', color='salmon', label="Kwintebank buoy", linewidth=LW)
# ax1.plot(nieu['time'], nieu['Hm'], '-.', color='m', label="Nieuwpoort buoy", linewidth=LW)
tot = np.array(awac_wave['Hm0,SS'])[index_adcp]+np.array(rbr_nie_wave_corr['Hm0,IG'])[index_ps]
ax1.plot(np.array(awac_wave['time'])[index_adcp], tot, color='#1F77B4', label="$H_{m0, Tot}$ - Nieuwpoort", linewidth=LW*1.1)
ax1.plot(np.array(awac_wave['time']), awac_wave['Hm0,SS'], '--', color='#1F77B4', label="$H_{m0, SS}$ - Nieuwpoort", linewidth=LW*1.1)
ax1.plot(np.array(signa_wave_rave1['time']), signa_wave_rave1['Hm0,IG'], '--', color='r', label="$H_{m0, SS}$ - Nieuwpoort", linewidth=LW*1.1)
ax1.plot(np.array(rbr_nie_wave_corr['time']), rbr_nie_wave_corr['Hm0,IG'], ':', color='#1F77B4', label="$H_{m0, IG}$ - Nieuwpoort", linewidth=LW*1.1)


# max(tot)
# max(np.array(awac_wave['Hm0,SS'])[index_adcp])
# max(np.array(rbr_nie_wave_corr['Hm0,IG'])[index_ps])
# ax1.plot(np.array(signa_wave['time']), signa_wave['Hm0,SS'], 'k', label="ADCP - Trapegeer", linewidth=LW*1.1)
# ax1.plot(np.array(signa_wave_rave1['time']), signa_wave_rave1['Hm0,SS'], 'y', label="ADCP - Raversijde 1", linewidth=LW*1.1)
# ax1.plot(np.array(signa_wave_rave2['time']), signa_wave_rave2['Hm0,SS'], 'darkorange', label="ADCP - Raversijde 2", linewidth=LW*1.1)
# ax1.plot(np.array(rbr_nie_wave_corr['time']), rbr_nie_wave_corr['Hm0,SS'], '--', color='k', label="Quartz3 + WLT - AWAC", linewidth=LW*1.1)
plot(ax1, 0, 0.4, r" $H_{m0}$ [m]", y_major_ticks, y_minor_ticks)

index_adcp = np.where((np.array(signa_wave['time'])<END) & (np.array(signa_wave['time'])>START))[0]   
index_ps = np.where((np.array(rbr_trap_wave_corr['time'])<END) & (np.array(rbr_trap_wave_corr['time'])>START))[0]   
# Subplot 2
ax2 = fig.add_subplot(222)
# ax1.plot(west['time'], west['Hm'], '-.', color='gray', label="Westhinder buoy", linewidth=LW)
# ax1.plot(kwin['time'], kwin['Hm'], '-.', color='salmon', label="Kwintebank buoy", linewidth=LW)
# ax1.plot(nieu['time'], nieu['Hm'], '-.', color='m', label="Nieuwpoort buoy", linewidth=LW)
tot = np.array(signa_wave['Hm0,SS'])[index_adcp]+np.array(rbr_trap_wave_corr['Hm0,IG'])[index_ps]
ax2.plot(np.array(signa_wave['time'])[index_adcp], tot, color='k', label="$H_{m0, Tot}$ - Trapegeer", linewidth=LW*1.1)
ax2.plot(np.array(signa_wave['time']), signa_wave['Hm0,SS'], '--', color='k', label="$H_{m0, SS}$ - Trapegeer", linewidth=LW*1.1)
ax2.plot(np.array(rbr_trap_wave_corr['time']), rbr_trap_wave_corr['Hm0,IG'], ':', color='k', label="$H_{m0, IG}$ - Trapegeer", linewidth=LW*1.1)

# max(tot)
# max(np.array(signa_wave['Hm0,SS'])[index_adcp])
# max(np.array(rbr_trap_wave_corr['Hm0,IG'])[index_ps])
# ax1.plot(np.array(signa_wave['time']), signa_wave['Hm0,SS'], 'k', label="ADCP - Trapegeer", linewidth=LW*1.1)
# ax1.plot(np.array(signa_wave_rave1['time']), signa_wave_rave1['Hm0,SS'], 'y', label="ADCP - Raversijde 1", linewidth=LW*1.1)
# ax1.plot(np.array(signa_wave_rave2['time']), signa_wave_rave2['Hm0,SS'], 'darkorange', label="ADCP - Raversijde 2", linewidth=LW*1.1)
# ax1.plot(np.array(rbr_nie_wave_corr['time']), rbr_nie_wave_corr['Hm0,SS'], '--', color='k', label="Quartz3 + WLT - AWAC", linewidth=LW*1.1)
plot(ax2, 0, 3.4, r" $H_{m0}$ [m]", y_major_ticks, y_minor_ticks)

# %%IG waves and sandbanks

def plot(ax, a, b, ylabel, y_major_ticks, y_minor_ticks,appo):
    ax.tick_params(axis='both', which='major', labelsize=FS)
    ax.legend(loc=4, fontsize=FS, ncol=2)
    plt.grid(True)
    plt.grid(b=True, which='minor', color='gray', linestyle='--')
    myFmt = mdates.DateFormatter('%b-%d')
    ax.xaxis.set_major_formatter(myFmt)
    ax.tick_params(axis='x', which='major', pad=25)
    ax.tick_params(axis='y', which='major', pad=25)
    ax.set_yticks(y_major_ticks)
    ax.set_yticks(y_minor_ticks, minor=True)
    plt.ylabel(ylabel, fontsize=1.5 * FS, labelpad=20)
    ax.legend(loc=1, fontsize=FS)    
    ax.set_ylim(a, b)
    ax.set_xlim(appo)
    # ax.set_xlim(datetime(2023, 3, 1, 12, 0, 0), datetime(2023, 3, 9, 12, 0))
    # ax.set_xlim(datetime(2023, 3, 1, 12, 0, 0), datetime(2023, 3, 9, 12, 0))
    
    fig.tight_layout()

# Define variables
FS = 30
LW = 3
y_major_ticks = np.arange(-0.4, 6, 0.4)
y_minor_ticks = np.arange(-.4, 6, 0.2)
START = datetime(2023, 2, 23, 12, 0, 0)
END = datetime(2023, 2, 27, 12, 0)
# index_adcp = np.where((np.array(signa_wave['time'])<END) & (np.array(signa_wave['time'])>START))[0]   
index_ps_nie = np.where((np.array(rbr_nie_wave_corr['time'])<END) & (np.array(rbr_nie_wave_corr['time'])>START))[0]   
index_ps_trap = np.where((np.array(rbr_trap_wave_corr['time'])<END) & (np.array(rbr_trap_wave_corr['time'])>START))[0]   
diff = np.array(rbr_trap_wave_corr['Hm0,IG'])[index_ps_trap] - np.array(rbr_nie_wave_corr['Hm0,IG'])[[index_ps_nie]]

 
fig = plt.figure(figsize=(30, 14))
# Subplot 1
ax1 = fig.add_subplot(221)
ax1.plot(np.array(rbr_trap_wave_corr['time']), rbr_trap_wave_corr['Hm0,IG'], '--', color='k', label="$H_{m0, IG}$ - Trapegeer", linewidth=LW*1.1)
ax1.plot(np.array(rbr_nie_wave_corr['time']), rbr_nie_wave_corr['Hm0,IG'], ':', color='#1F77B4', label="$H_{m0, IG}$ - Nieuwpoort", linewidth=LW*1.1)
ax1.plot(np.array(rbr_trap_wave_corr['time'])[index_ps_trap], diff, '-', color='darkorange', label="Difference", linewidth=LW*1.1)

plot(ax1, -0.04, 0.4, r" $H_{m0, IG}$ [m]", y_major_ticks/10, y_minor_ticks/10,(START, END))


START = datetime(2023, 3, 9, 12, 0, 0)
END = datetime(2023, 3, 12, 12, 0)
index_ps_nie = np.where((np.array(rbr_nie_wave_corr['time'])<END) & (np.array(rbr_nie_wave_corr['time'])>START))[0]   
index_ps_trap = np.where((np.array(rbr_trap_wave_corr['time'])<END) & (np.array(rbr_trap_wave_corr['time'])>START))[0]   
diff = np.array(rbr_trap_wave_corr['Hm0,IG'])[index_ps_trap] - np.array(rbr_nie_wave_corr['Hm0,IG'])[[index_ps_nie]]

# Subplot 2
ax2 = fig.add_subplot(222)
ax2.plot(np.array(rbr_trap_wave_corr['time']), rbr_trap_wave_corr['Hm0,IG'], '--', color='k', label="$H_{m0, IG}$ - Trapegeer", linewidth=LW*1.1)
ax2.plot(np.array(rbr_nie_wave_corr['time']), rbr_nie_wave_corr['Hm0,IG'], ':', color='#1F77B4', label="$H_{m0, IG}$ - Nieuwpoort", linewidth=LW*1.1)
ax2.plot(np.array(rbr_trap_wave_corr['time'])[index_ps_trap], diff, '-', color='darkorange', label="Difference", linewidth=LW*1.1)

plot(ax2, -0.04, 0.4, r" $H_{m0, IG}$ [m]", y_major_ticks/10, y_minor_ticks/10,(START, END))

# %%%INFLUENCE DIRECTION SS

# Set the index to the time column
rave1 = rave1.set_index('time')

# Resample the data to 1-hour frequency
rave1 = rave1.resample('3H').asfreq()

# Interpolate the missing values
rave1 = rave1.interpolate()

# Reset the index to the default RangeIndex
rave1 = rave1.reset_index(drop=False)

# Rename the time column to its original name
rave1 = rave1.rename(columns={'index': 'time'})


START = datetime(2023, 2, 18, 12, 0, 0)
END = datetime(2023, 3, 14, 12, 0)
index_rave1 = np.where((rave1.time<END) & (rave1.time>=START))[0] 
index_ps_nie = np.where((np.array(rbr_nie_wave_corr['time'])<END) & (np.array(rbr_nie_wave_corr['time'])>START))[0]   
index_ps_trap = np.where((np.array(rbr_trap_wave_corr['time'])<END) & (np.array(rbr_trap_wave_corr['time'])>START))[0]   

direction = rave1.dirhigh[index_rave1]
# hm = np.array(awac_wave['Hm0,SS'])[index_adcp]
hm = rave1.Hm[index_rave1]
hm_ig_trap = np.array(rbr_trap_wave_corr['Hm0,IG'])[index_ps_trap]
hm_ig_nie = np.array(rbr_nie_wave_corr['Hm0,IG'])[index_ps_nie]


# Define the intervals of rave1.dirhigh
dirhigh_intervals = [(0, 60), (240, 300), (300, 360)]

y_major_ticks = np.arange(0, 6, 0.2)
y_minor_ticks = np.arange(0, 6, 0.05)

# Create a new figure with subplots for each interval
fig, axes = plt.subplots(nrows=len(dirhigh_intervals), ncols=1, figsize=(36, 24), sharex=True)

# Iterate over the intervals and plot Hm0_rave1 vs Hm0_rbr_trap for each one
for i, (dirhigh_min, dirhigh_max) in enumerate(dirhigh_intervals):
    # Filter the values of rave1.Hm0 and rave1.dirhigh within the current interval
    mask = (direction >= dirhigh_min) & (direction < dirhigh_max)
    Hm0_rave1_interval = hm[mask]
    dirhigh_rave1_interval = direction[mask]
    
    # Filter the values of rbr_trap_wave_corr['Hm0,IG'] that correspond to the same values of dirhigh_rave1
    mask = np.isin(direction, dirhigh_rave1_interval)
    Hm0_rbr_trap_interval = hm_ig_trap[mask]
    Hm0_rbr_nie_interval = hm_ig_nie[mask]
    
    
    # Plot the two arrays on the current subplot
    ax = axes[i]
    ax.plot(Hm0_rave1_interval, Hm0_rbr_trap_interval, 's', markersize=20)
    ax.plot(Hm0_rave1_interval, Hm0_rbr_nie_interval, 'ko', markersize=20)
    # Fit a linear regression line to the data and plot it on the same subplot
    x = Hm0_rave1_interval
    y_trap = Hm0_rbr_trap_interval
    y_nie = Hm0_rbr_nie_interval
    coeffs_trap = np.polyfit(x, y_trap, 3)
    coeffs_nie = np.polyfit(x, y_nie, 3)
    p_trap = np.poly1d(coeffs_trap)
    p_nie = np.poly1d(coeffs_nie)
    xp = np.linspace(0, 3.2, 100)
    ax.plot(xp, p_trap(xp), ':', color='k', linewidth=3, label="Trapegeer")
    ax.plot(xp, p_nie(xp), '--', color='lightblue', linewidth=3, label="Nieuwpoort")
    
    ax.set_title(f'Direction Sea-Swell waves: {dirhigh_min}-{dirhigh_max} degrees', fontsize=FS)
    ax.set_xlabel(r" $H_{m0, SS}$ [m]", fontsize=1.5 * FS, labelpad=20)
    ax.set_ylabel(r" $H_{m0, IG}$ [m]", fontsize=1.5 * FS, labelpad=20)
    ax.tick_params(axis='both', which='major', labelsize=FS)
    ax.set_yticks(y_major_ticks)
    ax.set_yticks(y_minor_ticks, minor=True)
    ax.set_xticks(y_major_ticks)
    ax.set_xticks(y_minor_ticks, minor=True)
    ax.grid(True)
    ax.grid(b=True, which='minor', color='gray', linestyle='--')
    ax.set_xlim([0, 3.2])
    ax.set_ylim([0, 0.4])
    ax.legend(loc=2, fontsize=FS, ncol=2)
# Adjust the spacing between the subplots
fig.tight_layout()
 

import sys
import os
import pandas as pd
import numpy as np

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import plotly.graph_objects as go
from scipy.signal import spectrogram

import plotly.graph_objects as go
from scipy.signal import spectrogram

def compute_spectrogram(signal, fe, fmin, fmax):
    f, t, Sxx = spectrogram(signal, fe)
    Sxx = 10 * np.log10(Sxx)

    # Creer le figure
    fig = go.Figure(data=go.Heatmap(
                   z=Sxx,
                   x=t,
                   y=f,
                   colorscale='Hot'))

    fig.update_layout(
        title='Spectrogramme',
        xaxis_title='Temps [sec]',
        yaxis_title='Fréquence [Hz]',
        autosize=True,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        )
    )
    
    # Set the y-axis limits
    fig.update_yaxes(range=[fmin, fmax])

    fig.show()


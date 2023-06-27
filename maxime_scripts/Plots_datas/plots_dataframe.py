import pandas as pd
import parameters as parameters
import warnings
import sys
import os
import plotly.graph_objects as go
import plotly.express as px
import plotly.subplots as sp
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import numpy as np
import random
from scipy.signal import hilbert

# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


def plot_dataframe_dict(df_dict, N):
    for key in df_dict:
        # Prendre les N premières valeurs de chaque DataFrame
        df_N = df_dict[key].head(N)

        # Déterminer le nombre de colonnes numériques
        num_columns = sum([1 for column in df_N.columns if column != 'Time' and pd.api.types.is_numeric_dtype(df_N[column])])

        # Créer un subplot pour chaque colonne numérique
        fig = sp.make_subplots(rows=num_columns, cols=1)

        # Indice de la ligne pour le subplot
        row_index = 1

        for column in df_N.columns:
            if column != 'Time' and pd.api.types.is_numeric_dtype(df_N[column]):  # Ignorer les colonnes non numériques
                fig.add_trace(go.Scatter(x=df_N['Time'], y=df_N[column], mode='lines', name=column), row=row_index, col=1)
                row_index += 1
                
        fig.update_layout(
            title_text=f"Visualisation des {N} premières valeurs du DataFrame: {key}",
            height=200*num_columns,  # Hauteur dynamique en fonction du nombre de colonnes
        )
        fig.show()

def get_random_color():
    # Generate a random color
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    return f'rgb({r},{g},{b})'


def subplot_dataframe(df, N, *args):
    # Chercher la première colonne qui est de type datetime
    if 'DateTime' in df.columns:
        df['DateTime'] = pd.to_datetime(df['DateTime'], format='%m/%d/%Y %H:%M:%S')
    elif 'Time' in df.columns:
        df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %H:%M:%S')
    else:
        print("No suitable column for conversion to DateTime found.")

    time_column = next((col for col in df.columns if df[col].dtype == 'datetime64[ns]'), None)

    if time_column is None:
        print("Aucune colonne de type datetime trouvée.")
        return
 
    # Prendre les N premières valeurs du DataFrame
    df_N = df.head(N)

    # Déterminer le nombre de colonnes numériques et le nombre d'arguments supplémentaires
    num_columns = sum([1 for column in df_N.columns if column != time_column and (pd.api.types.is_numeric_dtype(df_N[column]) or df_N[column].dtype == np.complex)]) + len(args)

    # Créer un subplot pour chaque colonne numérique et chaque argument supplémentaire
    fig = make_subplots(rows=num_columns, cols=1)

    # Indice de la ligne pour le subplot
    row_index = 1

    # Ajouter les tracés pour chaque argument supplémentaire
    for arg in args:
        x, y = arg[:2]  # Extraire x et y

        # Extraire xmin et xmax si disponibles, sinon les définir à None
        xmin = arg[2] if len(arg) > 2 else None
        xmax = arg[3] if len(arg) > 3 else None

        # Si xmin et xmax sont définis, filtrer les données
        if xmin is not None and xmax is not None:
            mask = (x >= xmin) & (x <= xmax)
            x = x[mask]
            y = y[mask]

        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'{y.name} en fonction de {x.name}'), row=row_index, col=1)
        fig.update_xaxes(title_text=x.name, row=row_index, col=1)
        fig.update_yaxes(title_text=y.name, row=row_index, col=1)
        row_index += 1

    fig.update_layout(
        title_text=f"Visualisation des {N} premières valeurs du DataFrame",
        height=200*num_columns,
        showlegend=True,
    )

    fig.show()
    
def plot_dataframe(N, y_legend_name, *args):
    fig = go.Figure()

    # Create a list to hold the names of all y traces for the title
    y_names = []

    for arg in args:
        x, *ys = arg[0]
        x_range = arg[1] if len(arg) > 1 else None
        crossbars = arg[2:] if len(arg) > 2 else []

        if x_range is not None:
            xmin, xmax = x_range
            mask = (x >= xmin) & (x <= xmax)
            x = x[mask]
            ys = [y.reindex(x.index)[mask] for y in ys]  # Réindexation avant d'appliquer le masque

        for y in ys:
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=y.name))
            y_names.append(y.name)

        for crossbar in crossbars:
            x1_crossbar, x2_crossbar, name = crossbar
            min_y = min(min(y) for y in ys)
            max_y = max(max(y) for y in ys)
            line_color = get_random_color()

            # Draw rectangle
            fig.add_shape(type="rect",
                x0=x1_crossbar, y0=min_y, x1=x2_crossbar, y1=max_y,
                line=dict(color=line_color, width=2),
                fillcolor=line_color, opacity=0.2
            )
            
            # Add invisible trace for the legend
            fig.add_trace(go.Scatter(
                x=[None], y=[None],
                mode='markers+text',
                marker=dict(size=10, color=line_color, symbol='square'),
                showlegend=True,
                name=name
            ))

    # Create the title using the x and y names
    title_text = f"Plot of {', '.join(y_names)} as a function of {x.name} over {N} values"

    fig.update_layout(
        title_text=title_text,
        title_font_size=25,
        legend=dict(
            yanchor="top",
            y=-0,
            xanchor="left",
            x=0,
            font=dict(size=20)
        ),
        xaxis_title=x.name,
        yaxis_title=y_legend_name,  # Ajout du nom de la légende de l'axe Y
        xaxis_tickfont=dict(size=25),
        yaxis_tickfont=dict(size=25),
        xaxis_title_font=dict(size=25),
        yaxis_title_font=dict(size=25)
    )

    fig.show()

def plot_dataframe_columns(df):
    # Chercher la première colonne qui est de type datetime
    if 'DateTime' in df.columns:
        df['DateTime'] = pd.to_datetime(df['DateTime'], format='%m/%d/%Y %H:%M:%S')
    elif 'Time' in df.columns:
        df['Time'] = pd.to_datetime(df['Time'])
    else:
        print("No suitable column for conversion to DateTime found.")

    time_column = next((col for col in df.columns if df[col].dtype == 'datetime64[ns]'), None)

    if time_column is None:
        print("Aucune colonne de type datetime trouvée.")
        return

    # Déterminer le nombre de colonnes numériques
    num_columns = sum([1 for column in df.columns if column != time_column and (pd.api.types.is_numeric_dtype(df[column]) or df[column].dtype == np.complex)])

    # Créer un subplot pour chaque colonne numérique
    fig = make_subplots(rows=num_columns, cols=1)

    # Indice de la ligne pour le subplot
    row_index = 1

    for column in df.columns:
        if column != time_column and (pd.api.types.is_numeric_dtype(df[column]) or df[column].dtype == np.complex):
            fig.add_trace(go.Scatter(x=df[time_column], y=df[column], mode='lines', name=f'{column} en fonction de {time_column}'), row=row_index, col=1)
            fig.update_xaxes(title_text=time_column, row=row_index, col=1)
            fig.update_yaxes(title_text=column, row=row_index, col=1)
            row_index += 1

    fig.update_layout(
        title_text="Visualisation des colonnes du DataFrame",
        height=200*num_columns,
        showlegend=True,
    )

    fig.show()
    
def compute_envelope(signal, window_size):
    """
    Compute the lower and upper envelope of a signal by taking the rolling
    minimum and maximum over a window of a specified size.
    """
    signal_series = pd.Series(signal)
    lower_envelope = signal_series.rolling(window_size, center=True).min()
    upper_envelope = signal_series.rolling(window_size, center=True).max()

    return lower_envelope, upper_envelope

def plot_envelopes(signal1, signal2, sampling_rate, window_size):
    # Calculate the envelopes of the signals
    lower1, upper1 = compute_envelope(signal1, window_size)
    lower2, upper2 = compute_envelope(signal2, window_size)

    # Create an array for time which we'll use for plotting
    time = np.arange(len(signal1)) / sampling_rate

    # Create the figure
    fig = go.Figure()

    # Add traces for Signal 1 and its envelope
    #fig.add_trace(go.Scatter(x=time, y=signal1, mode='lines', name='Signal 1'))
    fig.add_trace(go.Scatter(x=time, y=lower1, mode='lines', name='Lower'+signal1.name, line=dict(dash='dash')))
    #fig.add_trace(go.Scatter(x=time, y=upper1, mode='lines', name='Upper'+signal1.name, line=dict(dash='dash')))

    # Add traces for Signal 2 and its envelope
    #fig.add_trace(go.Scatter(x=time, y=signal2, mode='lines', name='Signal 2'))
    fig.add_trace(go.Scatter(x=time, y=lower2, mode='lines', name='Lower'+signal2.name, line=dict(dash='dash')))
    #fig.add_trace(go.Scatter(x=time, y=upper2, mode='lines', name='Upper'+signal2.name, line=dict(dash='dash')))

    fig.update_layout(
        title_text='Signal comparison with envelopes',
        title_font_size=25,  # Taille de la police du titre
        legend=dict(
            yanchor="top",
            y=-0,
            xanchor="left",
            x=0,
            font=dict(size=20)  # Taille de la police de la légende
        ),
        xaxis_title='Time (s)',  # Ajout de la légende de l'axe x
        yaxis_title='Amplitude (dBar) ',  # Ajout de la légende de l'axe y
        xaxis_tickfont=dict(size=25),  # Augmentation de la taille des marqueurs
        yaxis_tickfont=dict(size=25),   # Augmentation de la taille des marqueurs de l'axe y
        xaxis_title_font=dict(size=25),  # Augmentation de la taille de la police pour la légende de l'axe x
        yaxis_title_font=dict(size=25)   # Augmentation de la taille de la police pour la légende de l'axe y
    )

    fig.show()
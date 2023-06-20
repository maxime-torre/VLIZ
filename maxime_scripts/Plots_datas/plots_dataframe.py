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

def plot_dataframe(df, N, *args):
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








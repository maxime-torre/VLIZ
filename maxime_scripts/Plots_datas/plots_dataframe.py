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

def plot_dataframe(df, N):
    # Chercher la première colonne qui est de type datetime
    df['DateTime'] = pd.to_datetime(df['DateTime'], format='%m/%d/%Y %H:%M:%S')

    time_column = next((col for col in df.columns if df[col].dtype == 'datetime64[ns]'), None)

    if time_column is None:
        print("Aucune colonne de type datetime trouvée.")
        return
 
    # Prendre les N premières valeurs du DataFrame
    df_N = df.head(N)

    # Déterminer le nombre de colonnes numériques
    num_columns = sum([1 for column in df_N.columns if column != time_column and pd.api.types.is_numeric_dtype(df_N[column])])

    # Créer un subplot pour chaque colonne numérique
    fig = make_subplots(rows=num_columns, cols=1)

    # Indice de la ligne pour le subplot
    row_index = 1

    for column in df_N.columns:
        if column != time_column and pd.api.types.is_numeric_dtype(df_N[column]):  # Ignorer les colonnes non numériques
            fig.add_trace(go.Scatter(x=df_N[time_column], y=df_N[column], mode='lines', name=column), row=row_index, col=1)
            row_index += 1

    fig.update_layout(
        title_text=f"Visualisation des {N} premières valeurs du DataFrame",
        height=200*num_columns,  # Hauteur dynamique en fonction du nombre de colonnes
        xaxis=dict(  # Formater l'axe des x pour un affichage plus court
            tickformat='%Y-%m-%d %H:%M:%S'
        )
    )
    fig.show()







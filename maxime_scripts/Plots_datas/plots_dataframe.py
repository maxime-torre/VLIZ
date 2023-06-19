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

def plot_dataframe(df, N):
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

    # Déterminer le nombre de colonnes numériques
    num_columns = sum([1 for column in df_N.columns if column != time_column and (pd.api.types.is_numeric_dtype(df_N[column]) or df_N[column].dtype == np.complex)])

    # Créer un subplot pour chaque colonne numérique
    fig = make_subplots(rows=num_columns, cols=1)

    # Indice de la ligne pour le subplot
    row_index = 1

    for column in df_N.columns:
        if column != time_column:
            if pd.api.types.is_numeric_dtype(df_N[column]):  # Ignorer les colonnes non numériques
                fig.add_trace(go.Scatter(x=df_N[time_column], y=df_N[column], mode='lines', name=column), row=row_index, col=1)
                row_index += 1
            elif df_N[column].dtype == np.complex:
                # Extraire les parties réelles et imaginaires des nombres complexes
                real_parts = df_N[column].apply(lambda x: x.real).to_list()
                imag_parts = df_N[column].apply(lambda x: x.imag).to_list()

                # Ajout d'une vérification pour s'assurer qu'il n'y a pas de nombres complexes dans les listes
                for part in real_parts + imag_parts:
                    if isinstance(part, complex):
                        raise ValueError(f"Un nombre complexe a été détecté dans les parties réelles ou imaginaires : {part}")

                fig.add_trace(go.Scatter(x=df_N[time_column], y=real_parts, mode='lines', name=f'{column} (partie réelle)'), row=row_index, col=1)
                row_index += 1
                fig.add_trace(go.Scatter(x=df_N[time_column], y=imag_parts, mode='lines', name=f'{column} (partie imaginaire)'), row=row_index, col=1)
                row_index += 1

    fig.update_layout(
        title_text=f"Visualisation des {N} premières valeurs du DataFrame",
        height=200*num_columns,
        showlegend=True,
    )

    fig.update_yaxes(title_text="Valeurs")
    fig.update_xaxes(title_text="Temps")

    fig.show()







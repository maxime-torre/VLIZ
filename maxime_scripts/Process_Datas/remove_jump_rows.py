import sys
import os
# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def remove_jump_rows(df, column, threshold, fs):
    # Calculer la dérivée
    df['derivative'] = df[column].diff()

    # Trouver les indices où la dérivée est grande
    jumps = df[df['derivative'].abs() > threshold]

    if len(jumps) == 0:
        print("No jumps found in data")
        return df
    samples_in_10min = 10 * 60 * fs

    # Supprimer les lignes avant le début du premier saut + 10 minutes et après la fin du second saut
    #+ samples_in_10min
    #- samples_in_10min
    start_index = jumps.index[0] + samples_in_10min
    end_index = jumps.index[-1] - samples_in_10min

    # Supprimer les lignes avant et après les sauts
    df_clean = df.loc[start_index:end_index]

    # Supprimer la colonne dérivée
    #df_clean = df_clean.drop(columns=['derivative'])

    return df_clean

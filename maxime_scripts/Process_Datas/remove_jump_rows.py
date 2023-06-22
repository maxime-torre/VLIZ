import sys
import os
# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def remove_jump_rows(df, column, threshold, fs):
    # Calculer la dérivée
    df['derivative'] = column.diff()
    print(f"Max derivation : {df['derivative'].max()}")
    print(f"Min derivation : {df['derivative'].min()}")

    # Trouver les indices où la dérivée est grande
    jumps = df[df['derivative'].abs() > threshold]

    if len(jumps) == 0:
        print("No jumps found in data")
        return df
    samples_in_10min = 10 * 60 * fs

    # Si il y a un seul saut
    if len(jumps) == 1:
        # Si le saut est au début
        if jumps.index[0] < len(df) / 2:
            start_index = jumps.index[0] + samples_in_10min
            df_clean = df.loc[start_index:]
        # Si le saut est à la fin
        else:
            end_index = jumps.index[0] - samples_in_10min
            df_clean = df.loc[:end_index]
    # Si il y a plusieurs sauts
    else:
        # Supprimer les lignes avant le début du premier saut + 10 minutes et avant la le début du second saut
        start_index = jumps.index[0] + samples_in_10min
        end_index = jumps.index[-1] - 4*samples_in_10min
        df_clean = df.loc[start_index:end_index]

    # Supprimer la colonne dérivée
    #df_clean = df_clean.drop(columns=['derivative'])

    return df_clean


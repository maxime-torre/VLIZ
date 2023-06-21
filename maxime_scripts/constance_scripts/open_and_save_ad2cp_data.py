import sys
import os
import pandas as pd
import dolfyn as dlfn


# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)


def read_ad2cp_to_dataframe(file_path):
    # Lire le fichier AD2CP avec Dolfyn
    data = dlfn.read(file_path)

    # Convertir les données en DataFrame pandas
    df = pd.DataFrame(data)

    return df
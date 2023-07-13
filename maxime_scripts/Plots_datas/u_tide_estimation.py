import sys
import os
import pandas as pd
from datetime import timedelta
from scipy import stats
import numpy as np
from utide import solve
from utide import reconstruct
# Ajouter le chemin du dossier grand-parent (le dossier principal V0)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def u_tide_estimation(distance, Time, latitude):
    coef = solve(Time, distance, lat=latitude)  # Remplacez 'your_latitude' par la latitude de votre site de mesure
    tide = reconstruct(Time, coef)
    u_tide_estimation_m = pd.Series(tide['h'], name="u_tide_estimation")
    print(u_tide_estimation_m)

    distance_without_tide = distance - u_tide_estimation_m
    distance_without_tide = pd.Series(distance_without_tide, name="Distance_without_tide_Utide")

    
    return u_tide_estimation_m, distance_without_tide

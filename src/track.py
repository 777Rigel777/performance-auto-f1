import fastf1
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



def load_track(year, race, sess_type):
    fastf1.Cache.enable_cache('../data/')
    session = fastf1.get_session(year, race, sess_type) # récupération de la courses
    session.load()
    fastest_lap = session.laps.pick_fastest() # récupération du tour le plus rapide
    telemetry = fastest_lap.get_telemetry() # récupération des données télémétrique

    track_data = telemetry[['X', 'Y', 'Distance']].copy() # mise en copy des éléments voulu
    track_data.describe() 
    track_data['X'] = track_data['X'].rolling(window=20, center=True).mean()
    track_data['Y'] = track_data['Y'].rolling(window=20, center=True).mean()

    
    return session, telemetry, track_data



def calcul_de_R(year, race, sess_type):
    session, telemetry, track_data = load_track(year,race,sess_type)

    X_point = np.gradient(track_data['X'],track_data['Distance']) # calcul de X_point dérivé de x par différences finies
    Y_point = np.gradient(track_data['Y'],track_data['Distance'])

    X_double_point = np.gradient(X_point,track_data['Distance']) # calcul de X_point dérivé de x par différences finies
    Y_double_point = np.gradient(Y_point,track_data['Distance'])

    R = (((X_point**2)+(Y_point)**2)**(3/2))/(np.abs(X_point*Y_double_point-Y_point*X_double_point))

    print(R)
    
    return R





def plot_R(year, race, sess_type):
    session, telemetry, track_data = load_track(year, race, sess_type)
    R = calcul_de_R(year, race, sess_type)

    plt.scatter(track_data['X'], track_data['Y'], 
            c=R, cmap='RdYlGn', vmin=0, vmax=500,
            s=5,          # taille des points
            linewidths=0.5,  # épaisseur du contour
            ) 
    plt.colorbar(label='R(s) (m)')
    
    plt.figure(figsize=(12, 4))
    plt.plot(track_data['Distance'], R)
    plt.xlabel('Distance (m)')
    plt.ylabel('R(s) (m)')
    plt.title('Rayon de courbure - Bakou')
    plt.ylim(0, 2000)  # on limite l'axe Y pour mieux voir
    plt.show()


plot_R(2022,8,'Q')



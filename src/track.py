import fastf1
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors
from scipy.interpolate import CubicSpline



def load_track(year, race, sess_type):
    fastf1.Cache.enable_cache('../data/')
    session = fastf1.get_session(year, race, sess_type) # récupération de la courses
    session.load()
    fastest_lap = session.laps.pick_fastest() # récupération du tour le plus rapide
    telemetry = fastest_lap.get_telemetry() # récupération des données télémétrique

    track_data = telemetry[['X', 'Y', 'Distance']].copy() # mise en copy des éléments voulu
    track_data.describe()
    
    print("X brut max:", telemetry['X'].max())
    print("X brut min:", telemetry['X'].min())
    print("Distance brut max:", telemetry['Distance'].max())
    

    
    return session, telemetry, track_data, fastest_lap



def calcul_de_R(year, race, sess_type):
    session, telemetry, track_data , fastest_lap = load_track(year,race,sess_type)

    pos_data = fastest_lap.get_pos_data()
    dx = np.diff(pos_data['X'])
    dy = np.diff(pos_data['Y'])

    distances = np.sqrt(dx**2 + dy**2)
    tel = telemetry[['X', 'Y', 'Distance']].dropna().copy()

    cs_x = CubicSpline(tel['Distance'], tel['X'])
    cs_y = CubicSpline(tel['Distance'], tel['Y'])

    s_new = np.arange(0, tel['Distance'].max(), 1)
    x_new = cs_x(s_new)
    y_new = cs_y(s_new)

    X_point = np.gradient(x_new,s_new) # calcul de X_point dérivé de x par différences finies
    Y_point = np.gradient(y_new,s_new)

    X_double_point = np.gradient(X_point,s_new) # calcul de X_point dérivé de x par différences finies
    Y_double_point = np.gradient(Y_point,s_new)

    

    R = (((X_point**2)+(Y_point)**2)**(3/2))/(np.abs(X_point*Y_double_point-Y_point*X_double_point))

    pos_data = fastest_lap.get_pos_data()
    print(pos_data.head(20))
    print(pos_data.columns.tolist())
    dx = np.diff(pos_data['X'])
    dy = np.diff(pos_data['Y'])

    print(np.nanpercentile(R, 1))
    print(np.nanpercentile(R, 5))
    print(np.nanpercentile(R, 25))

    plt.figure()
    plt.hist(R[R < 1000], bins=50)
    plt.show()
        

    return R, s_new, x_new, y_new





def plot_R(year, race, sess_type):
    R, s_new, x_new, y_new = calcul_de_R(year, race, sess_type)
    R_clipped = np.clip(R, 0, 400)
    
    plt.figure(figsize=(10, 10))
    plt.scatter(x_new, y_new,
                c=R_clipped, cmap='RdYlGn',
                vmin=0, vmax=400,
                s=2)
    plt.colorbar(label='R(s) (m)')
    plt.title('Rayon de courbure - Bakou')
    plt.axis('equal')
    plt.show()


plot_R(2022,8,'Q')





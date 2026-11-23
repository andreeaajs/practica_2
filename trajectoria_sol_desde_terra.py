import numpy as np
import matplotlib.pyplot as plt

T0 = 10 # FICAR LA HORA A LA QUE LA TERRA PASSA PEL PERIHELI 

_show = plt.show
plt.show = lambda *a, **k: None
from ResolucioEDO import x_t, y_t, r, s_3D, t_h
from Coordenades_respecte_centre_de_la_terra import r_t, matriu_Y, matriu_z, theta_0,w,r_I
plt.show = _show
plt.close('all')                   

x_t, y_t = np.array(x_t), np.array(y_t)    

s_I=matriu_Y.T @ matriu_z.T @ s_3D # sol en el sistema terra (transformació inversa)
alpha = np.arctan2(s_I[1], s_I[0]) # angle del Sol al voltant de l'eix de la Terra, visualitzat com si la Terra no gires [-pi,pi]
ah = 2*np.pi/24*(t_h + T0 - 12) # angle horari del sol (val zero al mig dia)

# ara hem de fer rotar aquest sistema amb la terra, llavors definim l'angle del meridià de l'observador
psi = alpha[0] + ah + (2 * np.pi / (365.25 * 24)) * t_h # s'ha afegit la correcció sidaria

# ara hem de definir la base de coordenades des de l'observador, mitjançant el vector zenital 

z_eix = np.array([[0.0], [0.0], [1.0]]) 

u_Z=r_I(psi / w)
u_E=np.cross(z_eix, u_Z, axis=0)
u_E=u_E/ np.linalg.norm(u_E, axis=0) # producte vectorial entre l'eiz z i el vector zenital normalitzat
u_N=np.cross(u_Z, u_E, axis=0)  # producte vectorial entre el vector zenital i el vector est normalitzat

# una vegada definits els eixos de coordenades a l'observador, hem de projectar el vector del sol amb productes escalars

s_zenit=np.sum(s_I*u_Z, axis=0)
s_est=np.sum(s_I*u_E, axis=0)
s_nord=np.sum(s_I*u_N, axis=0)

# per definir la posicio del sol a l'observador, definim l'altura i l'azimut
altura = np.arcsin(np.clip(s_zenit, -1.0, 1.0)) #np.clip per evitar errors de precisió numèrica que es vagin acumulant
azimut = np.arctan2(s_est, s_nord)

# GRAFIQUES

alt_deg = np.degrees(altura)
azi_deg = np.degrees(azimut) % 360  #passem de [-180,180] a [0,360]
dies = t_h / 24

plt.figure(figsize=(7, 5))
sc = plt.scatter(azi_deg, alt_deg, c=dies, cmap='twilight', s=12)
plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)  
plt.colorbar(sc, label='Dia de l\'any')
plt.xlabel('Azimut [°]')
plt.ylabel('Altura [°]')
plt.title(f'Analema solar a les {T0}:00 h')
plt.show()

# EL GRAFIC NO SURT BE PERQUE CAL CORRETJIR LA VELOCITAT DE LA ORBITA AL DOC RESOLUCIO DE EDO I ALTRES PARAMETRES


# PER FER MES GRAFIQUES O SIMULACIONS CAL REDUIR EL PAS DE TEMPS PER VEURE COM EVOLUCIONA LA TRAJECTORIA DEL SOL

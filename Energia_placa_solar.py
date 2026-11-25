import numpy as np
import matplotlib.pyplot as plt

_show = plt.show
plt.show = lambda *a, **k: None
from ResolucioEDO import a
from trajectoria_sol_desde_terra import  x_t, y_t, t_h, s_zenit
plt.show = _show
plt.close('all')

UA = 1.495978707e11
A=10 # area placa (canviar)

P_s=3.828e26 #potencia emessa pel sol


d= np.sqrt(x_t**2+y_t**2)*UA/a # per passar de unitats reduides a metres 

F=P_s/(4*np.pi*d**2) #flux de radiació solar a una distancia d (hem de ficar la distancia del nostre punt al sol en funció del temps, en unitats del SI, no GM=1)

# angle zenital = angle respecte la normal a la superficie de la terra
# ens volem quedar amb la component perpendicular del feix a la placa
# per lo petita que es la placa, podem considerar que nomès arriben els raigs en una direccio, que sera exactament la del vector que uneix el nostre punt amb el sol

P=F*np.maximum(0.0, s_zenit)*A #potencia que arriba a la placa solar (np.maximum per evitar potencies negatives de nit)


n_dies = len(P) // 24
E_diaria = P[:n_dies * 24].reshape(n_dies, 24).sum(axis=1) / 1000.0

plt.figure(figsize=(8, 4.5))
plt.plot(np.arange(n_dies), E_diaria, color='#2a78d6', lw=1.8)
plt.xlabel('Dia des del periheli')
plt.ylabel('Energia incident diària [kWh/dia]')
plt.title(f'Energia solar diària sobre una placa horitzontal de {A:.0f} m²')
plt.tick_params(direction='in')
plt.show()
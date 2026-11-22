import numpy as np
import matplotlib.pyplot as plt

_show = plt.show
plt.show = lambda *a, **k: None
from ResolucioEDO import x_t, y_t                          
from Coordenades_respecte_centre_de_la_terra import r_t    
plt.show = _show
plt.close('all')                   

x_t, y_t = np.array(x_t), np.array(y_t)    

s_I=Rz(chi) @ Ry(eps) @ s_3D # sol en el sistema de l'eix
alpha = np.arctan2(sI[1], sI[0]) # angle del Sol al voltant de l'eix de la Terra, visualitzat com si la Terra no gires

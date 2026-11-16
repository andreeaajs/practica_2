import numpy as np
import math as mth

#dades

w=1 #velocitat de rotacó de la terra
phi_0=22.23 #angle d'inlinació de la terra respecte de z
theta_0=1 #latitud
R_T=1 #radi de la terra
def r_I(t):
    r_I=[R_T*mth.cos(theta_0)*mth.cos(w*t), R_T*mth.cos(theta_0)*mth.sin(w*t), R_T*mth.sin(theta_0)
    ]
    return r_I

matriu_Y =[[mth.cos(phi_0), 0, mth.sin(phi_0)], [0,1,0], [-mth.sin(phi_0), 0, mth.cos(phi_0)]]
A=np.array(matriu_Y)

r_t=r_I @ A

print(r_t)
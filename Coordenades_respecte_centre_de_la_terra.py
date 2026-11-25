import numpy as np
import math as mth
import matplotlib.pyplot as plt

#dades

w=2*np.pi/24 #velocitat de rotacó de la terra
phi_0=np.radians(23.43928) #angle d'inlinació de la terra respecte de z
theta_0= np.radians(41.50) #latitud (revisar)
chi = np.radians(90 - 102.93768193) # longitud ecliptica del solstici - longitud ecliptica del periheli 
R_T=1 #radi de la terra
#radi en l'eix principal d'inèrcia
def r_I(t):
   t = np.asarray(t)
   return np.array([R_T*np.cos(theta_0)*np.cos(w*t),
                    R_T*np.cos(theta_0)*np.sin(w*t), 
                    R_T*np.sin(theta_0)*np.ones_like(t)])
    
#matriu rotació en y
matriu_Y =np.array([[np.cos(phi_0), 0, np.sin(phi_0)], 
                    [0,1,0], 
                    [-np.sin(phi_0), 0, np.cos(phi_0)]])

matriu_z = np.array([[np.cos(chi), -np.sin(chi), 0],
               [np.sin(chi),  np.cos(chi), 0],
               [0,            0,           1]])

#vector r en funció de t
def r_t(t):
    return matriu_z @ matriu_Y @ r_I(t)

t = np.linspace(0, 24, 400)
x, y, z = r_t(t)

plt.figure(figsize=(8, 5))

plt.plot(t, x, label='x')
plt.plot(t, y, label='y')
plt.plot(t, z, label='z')

plt.title("Vector de l'observador en el sistema de l'òrbita")
plt.xlabel("t [h]")
plt.ylabel("Components de r (en unitats de R_T)")

plt.grid(True)
plt.legend()

plt.show()

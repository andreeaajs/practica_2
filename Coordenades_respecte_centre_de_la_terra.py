import numpy as np
import math as mth
import matplotlib.pyplot as plt

#dades

w=2*np.pi/24 #velocitat de rotacó de la terra
phi_0=np.radians(22.23) #angle d'inlinació de la terra respecte de z
theta_0=1 #latitud
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

#vector r en funció de t
def r_t(t):
    return matriu_Y @ r_I(t)

t= np.linspace(0, 24, 400)
x, y, z = r_t(t)

plt.figure(figsize=(8, 5))

plt.plot(t, x, label='Dades')
plt.plot(t, y, label='Dades')
plt.plot(t, z, label='Dades')
# 3. Afegir títols i etiquetes
plt.title("Títol de la gràfica")
plt.xlabel("Eix X")
plt.ylabel("Eix Y")

# 4. Afegir quadrícula i llegenda
plt.grid(True)
plt.legend()

# 5. Mostrar la gràfica
plt.show()

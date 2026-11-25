
import matplotlib.pyplot as plt
import numpy as np
def der_vx(x,y):
    dervx = -x/((x**2+y**2)**(3/2))
    return dervx

def der_vy(x,y):
    dervy = -y/((x**2+y**2)**(3/2))
    return dervy

a= (2*np.pi)**(-2/3) # semieix major de l'òrbita de la terra per GM=1
e = 0.01671123 # excentricitat de l'òrbita de la terra
x_0 = a*(1 - e)
v_y_0 = np.sqrt((1/a)*(1+e)/(1-e)) 
y_0 = 0
v_x_0 = 0
r = [x_0, y_0, v_x_0, v_y_0]
x_t =[x_0]
y_t=[y_0]
t_t = [0]

t = 0 
h = 1/(365.256 * 24)


#[fx,fy,fvx,fvy]
while t < 1:
    t = t + h
    K1 = [r[2], r[3], der_vx(r[0],r[1]), der_vy(r[0],r[1])]
    K2 = [(r[2] + (h/2)*K1[2]),(r[3] + (h/2)*K1[3]), der_vx(r[0] + (h/2)*K1[0], r[1] + (h/2)*K1[1]), der_vy(r[0] + (h/2)*K1[0], r[1] + (h/2)*K1[1])]
    K3 = [(r[2] + (h/2)*K2[2]),(r[3] + (h/2)*K2[3]), der_vx(r[0] + (h/2)*K2[0], r[1] + (h/2)*K2[1]), der_vy(r[0] + (h/2)*K2[0], r[1] + (h/2)*K2[1])]
    K4 = [(r[2] + h*K3[2]),(r[3] + h*K3[3]), der_vx(r[0] + h*K3[0], r[1] + h*K3[1]), der_vy(r[0] + h*K3[0], r[1] + h*K3[1])]
    r = [r[i] + (h/6)*(K1[i] +2*(K2[i] + K3[i]) + K4[i]) for i in range(4)]
    x_t.append(r[0])
    y_t.append(r[1])
    t_t.append(t) 

plt.plot(x_t,y_t)
plt.show()

# vector de direcció terra-sol

r = np.array([x_t, y_t]) 
dist = np.linalg.norm(r, axis=0)
s = -r / dist
s_3D = np.vstack([s, np.zeros(s.shape[1])])

# temps en hores
t_h = np.array(t_t)*365.256*24 

import matplotlib.pyplot as plt

def der_vx(x,y):
    dervx = -x/((x**2+y**2)**(3/2))
    return dervx

def der_vy(x,y):
    dervy = -y/((x**2+y**2)**(3/2))
    return dervy



x = 3
y = 0
v_x = 0
v_y = 0.6
r = [x, y, v_x, v_y]
x_t =[x]
y_t=[y]

t = 0 
h = 1/365

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

plt.scatter(x_t,y_t)
plt.show()
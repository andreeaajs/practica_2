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
psi = alpha[0] + ah + (2 * np.pi / (365.256 * 24)) * t_h # s'ha afegit la correcció sidaria

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


#------------------------------------------------------------------------------------------------------


# GRAFIQUES

alt_deg = np.degrees(altura)
azi_deg = np.degrees(azimut) % 360  #passem de [-180,180] a [0,360]
dies = t_h / 24

# ELS 24 ANALEMES DEL DIA ALHORA
plt.figure(figsize=(7, 5))
sc = plt.scatter(azi_deg, alt_deg, c=dies, cmap='twilight', s=12)
plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)  
plt.colorbar(sc, label='Dia de l\'any')
plt.xlabel('Azimut [°]')
plt.ylabel('Altura [°]')
plt.title(f'Analema solar a les {T0}:00 h')
plt.show()

# ANALEMA DE LES 10:00
plt.figure(figsize=(7, 5))
sc = plt.scatter(azi_deg[::24], alt_deg[::24], c=dies[::24], cmap='twilight', s=12)
plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)  
plt.colorbar(sc, label='Dia de l\'any')
plt.xlabel('Azimut [°]')
plt.ylabel('Altura [°]')
plt.title(f'Analema solar a les {T0}:00 h')
plt.show()

#-------------------------------------------------------------------------------------------------

# CARTA SOLAR EN PROJECCIÓ POLAR

fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(projection='polar')
ax.set_theta_zero_location('N')   # 0° (Nord) a dalt
ax.set_theta_direction(-1)        # sentit horari (Est a la dreta)

# Trobem automàticament els dies dels solsticis i l'equinocci a partir de s_I[2] = sin(declinació)
dia_estiu = np.argmax(s_I[2]) // 24
dia_hivern = min(np.argmin(s_I[2]) // 24, len(s_I[2]) // 24 - 2)
dia_eq = np.argmin(np.abs(s_I[2][:180 * 24])) // 24

offset_mitjanit = (24 - T0) % 24  # alineem cada dia de 00:00 a 23:00 perquè la corba no salti

for dia, etiqueta, color in [
    (dia_estiu, 'Solstici d\'estiu', 'crimson'),
    (dia_eq, 'Equinocci', 'goldenrod'),
    (dia_hivern, 'Solstici d\'hivern', 'royalblue')
]:
    i0 = dia * 24 + offset_mitjanit
    sl = slice(i0, i0 + 24)
    dia_mask = alt_deg[sl] > 0
    ax.plot(azimut[sl][dia_mask], 90 - alt_deg[sl][dia_mask], label=etiqueta, color=color, lw=2)

# Superposem els analemes de cada hora (només de dia)
diurn = alt_deg > 0
ax.scatter(azimut[diurn], 90 - alt_deg[diurn], s=1, color='gray', alpha=0.35)

ax.set_ylim(0, 90)
ax.set_yticks([0, 30, 60, 90])
ax.set_yticklabels(['90°', '60°', '30°', '0°'])  # etiquetes d'altura real
ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1.1))
plt.title('Carta solar a la UAB')
plt.show()


#Hores de sortida, posta de Sol i durada del dia

sortides = np.where((s_zenit[:-1] <= 0) & (s_zenit[1:] > 0))[0]
postes   = np.where((s_zenit[:-1] >= 0) & (s_zenit[1:] < 0))[0]

# Interpolació lineal dels zeros de s_zenit
dt_s = t_h[sortides + 1] - t_h[sortides]
dt_p = t_h[postes + 1]   - t_h[postes]
t_sort = t_h[sortides] - s_zenit[sortides] * dt_s / (s_zenit[sortides + 1] - s_zenit[sortides])
t_post = t_h[postes]   - s_zenit[postes]   * dt_p / (s_zenit[postes + 1]   - s_zenit[postes])

# Hora solar [0, 24)
hora_sort = (t_sort + T0) % 24
hora_post = (t_post + T0) % 24

# Durada del dia (aparellant cada sortida amb la posta immediatament posterior)
t_post_aparellat = t_post[1:] if t_post[0] < t_sort[0] else t_post
n = min(len(t_sort), len(t_post_aparellat))
hores_llum = t_post_aparellat[:n] - t_sort[:n]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
ax1.plot(t_sort / 24, hora_sort, label='Sortida del Sol')
ax1.plot(t_post / 24, hora_post, label='Posta del Sol')
ax1.set_ylabel('Hora solar [h]')
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2.plot(t_sort[:n] / 24, hores_llum, color='darkorange')
ax2.set_xlabel('Dia des del periheli')
ax2.set_ylabel('Hores de llum [h]')
ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

#------------------------------------------------------------------------------------------------------

# SIMULACIÓ D'UN RELLOTGE DE SOL


plt.figure(figsize=(8, 5))

# Ombra dels analemes per a cada hora (filtrem Sol baix perquè l'ombra no marxi a l'infinit)
visible = s_zenit > 0.25
plt.scatter(-s_est[visible] / s_zenit[visible], -s_nord[visible] / s_zenit[visible],
            s=1, color='gray', alpha=0.4, label='Analemes horaris')

# Corbes estacionals de l'ombra
for dia, etiqueta, color in [
    (dia_estiu, 'Solstici d\'estiu', 'crimson'),
    (dia_eq, 'Equinocci', 'goldenrod'),
    (dia_hivern, 'Solstici d\'hivern', 'royalblue')
]:
    i0 = dia * 24 + offset_mitjanit
    sl = slice(i0, i0 + 24)
    m = s_zenit[sl] > 0.25
    plt.plot(-s_est[sl][m] / s_zenit[sl][m], -s_nord[sl][m] / s_zenit[sl][m],
             lw=2, color=color, label=etiqueta)

plt.scatter([0], [0], color='black', zorder=5, label='Base del gnòmon')
plt.axis('equal')
plt.xlabel('Oest  ←  x [L]  →  Est')
plt.ylabel('Sud  ←  y [L]  →  Nord')
plt.title('Trajectòria de l\'ombra d\'un gnòmon vertical a la UAB')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from Functions1 import newmark
from scipy.integrate import odeint

ag_txt = np.loadtxt("ground_acc.txt", skiprows=0) #units are in g
ags = ag_txt.flatten("C")
# np.savetxt("ground_acc.txt", ags, fmt="%15.10f", delimiter=" ", newline="\n")
t_amount = len(ags)

dt = 0.05
start_t = 0
end_t = (t_amount - 1)*dt
t_list=np.linspace(start_t, end_t,t_amount)

pi = np.pi
T=0.1
f=1/T
m=1             #kg
wn=2 * pi * f   #rad/sec
k=m*wn**2       #N/m
eps=0.05        #ksi
c=2*eps*wn*m    #unitless

p_exc = -m * ags * 9.806

x0 = 0
v0 = 0
beta = 1/4
gamma = 1/2
x, v, a = newmark(m, c, k, dt, p_exc, beta, gamma, x0, v0)

plt.plot(t_list,a)
ax0 = plt.gca()
ax0.grid(True)
ax0.legend()
plt.xlabel("t(s)")
plt.ylabel("a (m/s2)")
plt.title("Acceleration")
plt.show()

plt.plot(t_list,v)
plt.xlabel("t(s)")
plt.ylabel("v (m/s)")
plt.title("Velocity")
plt.show()

plt.plot(t_list,x)
plt.xlabel("t(s)")
plt.ylabel("x (m)")
plt.title("Displacement")
plt.show()

# plt.plot(x,c*v)
# plt.xlabel("x (s)")
# plt.ylabel("fd (t)")
# plt.title("Damping Force - Displacement")
# plt.show()

# plt.plot(x,k*x)
# plt.xlabel("x (s)")
# plt.ylabel("fs (t)")
# plt.title("Spring Force - Displacement")
# plt.show()


# ###KONTROL #grafik üst üste gelirse turuncu olması gereklidir.
# lx , lv, la = linaccel(m, c, k, dt, p_exc, x0, v0)

# #hatayı yüzde olarak bulmak için aşağıdaki kodları kullanıyoruz.
# x_diff = nx - lx
# x_err = 100 * np.divide(x_diff, np.max(np.abs(nx)))

# plt.plot(t_list, x_err)
# plt.xlabel("t(s)")
# plt.ylabel("Displacement - Fark Oranı")
# plt.title("Error")
# plt.show()

# plt.plot(t_list, na, "-g", linewidth=5, label="newmark")
# plt.plot(t_list, la, "-b", linewidth=1, label="linaccel")
# ax0 = plt.gca()
# ax0.grid(True)
# ax0.legend()
# plt.xlabel("t(s)")
# plt.ylabel("a (m/s2)")
# plt.title("Acc")
# plt.show()

# plt.plot(t_list, nv, "-g", linewidth=5, label="newmark")
# plt.plot(t_list, lv, "-b", linewidth=1, label="linaccel")
# ax0 = plt.gca()
# ax0.grid(True)
# ax0.legend()
# plt.xlabel("t(s)")
# plt.ylabel("v (m/s)")
# plt.title("Velo")
# plt.show()

# plt.plot(t_list, nx, "-g", linewidth=5, label="newmark")
# plt.plot(t_list, lx, "-b", linewidth=1, label="linaccel")
# ax0 = plt.gca()
# ax0.grid(True)
# ax0.legend()
# plt.xlabel("t(s)")
# plt.ylabel("x (m)")
# plt.title("Disp")
# plt.show()

# plt.plot(nx, c*nv, "-g", linewidth=5, label="newmark")
# plt.plot(lx, c*lv, "-b", linewidth=1, label="linaccel")
# ax0 = plt.gca()
# ax0.grid(True)
# ax0.legend()
# plt.xlabel("x (s)")
# plt.ylabel("fd (t)")
# plt.title("Damping Force - Displacement")
# plt.show()

# plt.plot(nx, k*nx, "-g", linewidth=5, label="newmark")
# plt.plot(lx, k*lx, "-b", linewidth=1, label="linaccel")
# ax0 = plt.gca()
# ax0.grid(True)
# ax0.legend()
# plt.xlabel("x (s)")
# plt.ylabel("fs (t)")
# plt.title("Spring Force - Displacement")
# plt.show()



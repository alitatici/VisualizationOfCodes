#import math
import numpy as np

def linaccel(m, c, k, dt, p, x0, v0):
    t_amount = len(p)

    x=np.zeros(t_amount)
    v=np.zeros(t_amount)
    a=np.zeros(t_amount)

    x[0] = x0 
    v[0] = v0
    a[0] = (p[0] - c * v [0] - k * x[0])/m

    index_array = np.arange(1, t_amount)

    A=((m * 6) / (dt**2) + (c * 3) / dt + k )

    for i in index_array:
        B= m * (2 * a[i-1] + (6 * x[i-1]) / (dt**2) + (6* v[i-1]) / dt) + c * ( 2 * v[i-1] + a[i-1] * dt/2 + 3 * x[i-1] /dt) + p[i]
        x[i]=B/A
        v[i]= (3/dt)*(x[i]-x[i-1])- 2 * v[i-1] - a[i-1] * dt/2
        a[i] = (6 / dt**2) * (x[i] - x[i-1]) - 6 * v[i-1]/dt - 2 * a[i-1]

    return x, v, a

def newmark(m, c, k, dt, p, beta, gamma, x0, v0):
    t_amount = len(p)

    khat = k + (gamma * c / (beta * dt)) + m / (beta * (dt**2))
    constant1 = m / (beta*dt) + gamma*c / beta
    constant2 = m /(2*beta) + dt * (gamma/(2*beta)-1)*c 

    x=np.zeros(t_amount)
    v=np.zeros(t_amount)
    a=np.zeros(t_amount)

    x[0] = x0 
    v[0] = v0
    a[0] = (p[0] - c * v [0] - k * x[0])/m

    index_array = np.arange(1, t_amount)

    for i in index_array:

        delta_p = p[i] - p[i-1]
        delta_phat = delta_p + constant1 * v[i-1] + constant2 * a[i-1]

        delta_x = delta_phat/khat
        delta_v = delta_x * gamma / (beta * dt) - v[i-1] * gamma / beta + dt * (1-gamma/(2*beta))*a[i-1]
        delta_a = delta_x / (beta * (dt**2)) - v[i-1] / (beta * dt) - a[i-1] / (2 * beta)

        x[i] = x[i-1] + delta_x
        v[i] = v[i-1] + delta_v
        a[i] = a[i-1] + delta_a

    return x, v, a




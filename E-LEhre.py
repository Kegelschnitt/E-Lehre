#import :
from praktikum import analyse
from praktikum import cassy
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from uncertainties import ufloat


#Konstanten:
L = 9*10**-3
C =2.2*10**-6
R = 46.5
U_0 = 10.2

#R-Werte ermitteln:
R_grenz = 2*np.sqrt(L/C)

R_min =0
R_max =20

R_array = np.array([R_min, (R_grenz-R_min)/2, R_grenz, (R_max-R_grenz)/4+R_grenz,
                    (R_max-R_grenz)/4*2+R_grenz, (R_max-R_grenz)/4*3+R_grenz, R_max])




#Formeln:
omega_0 = 1/np.sqrt(L*C)
delta = R/(2*L)
omega = np.sqrt(omega_0**2 - delta**2)

print("omega" , omega)
print("omega_0", omega_0)
print("delta", delta)
print("R_grenz", R_grenz)



#Plot
#A = C*U_0*(delta+np.sqrt(delta**2-omega_0**2))/(2*np.sqrt(delta**2-omega_0**2))
#B = C*U_0*(-delta+np.sqrt(delta**2-omega_0**2))/(2*np.sqrt(delta**2-omega_0**2))

## Schwingfall
def U_plot(t):
    return U_0*(np.exp(-delta*t)*(np.cos(omega*t)+(delta/omega)*np.sin(omega*t)))

def I_plot(t):
    return -C*U_0*np.exp(-delta*t)*(omega+delta**2/omega)*np.sin(omega*t)

t = np.linspace(0, 0.005, 100)

#Plot I
plt.grid()
plt.plot(t, I_plot(t))
plt.xlabel("t")
plt.ylabel("I")
plt.show()

#Plot U
plt.grid()
plt.plot(t, U_plot(t))
plt.xlabel("t")
plt.ylabel("U")
plt.show()

#FFT:
FFT_I = analyse.fourier(t, I_plot(t))
FFT_U = analyse.fourier(t, U_plot(t))

plt.plot(FFT_I[0], FFT_I[1])
plt.xlabel("freq")
plt.ylabel("Amp")
plt.title("FFT I")
plt.show()

plt.plot(FFT_U[0], FFT_U[1])
plt.xlabel("freq")
plt.ylabel("Amp")
plt.title("FFT U")
plt.show()


#Output:


#Statistik:

Werte = np.array([1, 2, 3, 4, 5])
std = np.std(Werte, ddof=1)
mean = np.mean(Werte)

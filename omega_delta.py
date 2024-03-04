#import :
from praktikum import analyse
from praktikum import cassy
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from uncertainties import ufloat
import scipy



plt.rcParams['font.size'] = 24.0
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelsize'] = 'medium'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['lines.linewidth'] = 2.0

# Tabelle R mit Fehler:

R0 = ufloat(0.98, 0.01)
R1 = ufloat(5.12, 0.01)
R2 = ufloat(10.01, 0.01)
R3 = ufloat(19.85, 0.01)
R4 = ufloat(46.5, 0.02)

R_array = np.array([R0, R1, R2, R3, R4])

#Rauschmessung:

#parameter: U gemessen, t bis 10s, 501 werte
rausch_spannung = cassy.CassyDaten('rauschmessung/rauschmessung neu.labx')
U_rausch = rausch_spannung.messung(1).datenreihe('U_B1').werte
U_rausch_t = rausch_spannung.messung(1).datenreihe('t').werte



#parameter: I_A1 gemessen. t bis 10s, 201 werte
rausch_strom = cassy.CassyDaten('rauschmessung/rausch strom.labx')
I_rausch = rausch_strom.messung(1).datenreihe('I_A1').werte
I_rausch_t = rausch_strom.messung(1).datenreihe('t').werte


#Parameter: U_B1 gemessen, t bis 5s, 2501 werte:
rausch_syst = cassy.CassyDaten('rauschmessung/10Ohm ausschalten.labx')
U_rausch_syst = rausch_syst.messung(1).datenreihe('U_B1').werte
U_rausch_syst_t = rausch_syst.messung(1).datenreihe('t').werte

U_syst_mean_1 = np.mean(U_rausch_syst[1250:1800:1])
U_syst_mean_2 = np.mean(U_rausch_syst[1900:2500:1])
U_syst_std = np.std(U_rausch_syst[1000:1800:1])

print(U_syst_mean_1)
print(U_syst_mean_2)
U_syst_1 = ufloat(U_syst_mean_1, U_syst_std)
U_syst_2 = ufloat(U_syst_mean_2, U_syst_std)



U_Dif = U_syst_mean_2 - U_syst_mean_1
print('Dif: ',U_Dif)








# Daten Einlesen:
##Benutzt:
## Index n
## Zeit t/ms
## Spannung U_B1/V
## I_A1/A
##

## Struktur
'''
s[i][j] 
mit i = 
0 = 1 ohm
1 = 5
2 = 10
3 = 20
4 = 50

mit j = 
0 = 1
1 = 2
2 = 3.Messung

'''

#Matrix mit allen werten
w, h = 3, 5
s = [[0 for x in range(w)] for y in range(h)]
U = [[0 for x in range(w)] for y in range(h)]
I = [[0 for x in range(w)] for y in range(h)]

s[0][0] = cassy.CassyDaten('Schwingfall mit Cassy/1ohm/1ohm1.labx')
s[0][1] = cassy.CassyDaten('Schwingfall mit Cassy/1ohm/1ohm2.labx')
s[0][2] = cassy.CassyDaten('Schwingfall mit Cassy/1ohm/1ohm3.labx')

s[1][0] = cassy.CassyDaten('Schwingfall mit Cassy/5ohm/5 ohm1 .labx')
s[1][1] = cassy.CassyDaten('Schwingfall mit Cassy/5ohm/5.1 ohm 2.labx')
s[1][2] = cassy.CassyDaten('Schwingfall mit Cassy/5ohm/5.1 ohm 3.labx')

s[2][0] = cassy.CassyDaten('Schwingfall mit Cassy/10ohm/10 ohm 1.labx')
s[2][1] = cassy.CassyDaten('Schwingfall mit Cassy/10ohm/10 ohm 2.labx')
s[2][2] = cassy.CassyDaten('Schwingfall mit Cassy/10ohm/10 ohm 3.labx')

s[3][0] = cassy.CassyDaten('Schwingfall mit Cassy/20ohm/20 ohm 1.labx')
s[3][1] = cassy.CassyDaten('Schwingfall mit Cassy/20ohm/20 ohm 2.labx')
s[3][2] = cassy.CassyDaten('Schwingfall mit Cassy/20ohm/20 ohm 3.labx')

s[4][0] = cassy.CassyDaten('Schwingfall mit Cassy/50ohm/47 ohm 1.labx')
s[4][1] = cassy.CassyDaten('Schwingfall mit Cassy/50ohm/47 ohm 2.labx')
s[4][2] = cassy.CassyDaten('Schwingfall mit Cassy/50ohm/47 ohm 3.labx')


# U_Werte mit Korrektur systematischer Fehler:
for i in range(w):
    for j in range(h):
        U[j][i] = s[j][i].messung(1).datenreihe('U_B1').werte + U_Dif
        I[j][i] = s[j][i].messung(1).datenreihe('I_A1').werte


# Bsp:  print(U[4][2][200])




#Max/Min Bestimmen:

t = s[1][0].messung(1).datenreihe('t').werte


L = 9*10**-3
C =2.2*10**-6
omega_0 = 1/np.sqrt(L*C)
delta =[0 for x in range(h)]
for i in range(h):
    delta[i] = R_array[i].n / (2 * L)

print(delta)

omega = np.power((omega_0**2 - np.power(delta,2)),.5)
T = 2*np.pi*10**3/omega



Max = [[0 for x in range(w)] for y in range(h)]


Max[1][0] = scipy.signal.find_peaks(U[1][0])
print(Max[1][0])

peaks, _ = scipy.signal.find_peaks(U[1][0], height=0)



plt.plot(t[peaks], U[1][0][peaks], "x")


#plt.plot(t, U[0][0],color='yellow')
plt.scatter(t, U[1][0], color='orange', alpha=0.5, s=2)
plt.plot(t, U[2][0], color='red', alpha=0.5)
plt.plot(t, U[3][0], color='blue', alpha=0.5)
plt.plot(t, U[4][0], color='green', alpha=0.5)

plt.grid()
plt.show()









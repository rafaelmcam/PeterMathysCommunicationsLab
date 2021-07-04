import matplotlib.pyplot as plt
import numpy as np
from ModuleLab1 import *


Fs, rt = wavread("MyTest.wav")
Fb = 100
ttr = np.arange(rt.size) / Fs - 1 / (2 * Fb)

Fbparms = [Fb, 0]
rn, ixn = ftpam_rcvr01(ttr, rt, Fbparms)


exit(0)

# E1D -> estimativa do sinal transmitido (não deve ser perfeito por causo dos filtros)

FsT = 24000
tlenT = 0.02
ttT = np.arange(np.round(tlen*FsT))/float(FsT)

A = 0.5
deg1 = 349.1457286432161
deg2 = 30.7537688442211

xtT = A * (1.0 * np.sin(2*np.pi*700*ttT + np.pi / 180 * deg1) + 1 * np.sin(2*np.pi*1200*ttT + np.pi / 180 * deg2))
plt.figure(figsize = (14, 4))
plt.title(f"Sinal interpolado resultante, utilizando fator de upsample = {upsample_factor}\nDeg1/Deg2: {deg1}, {deg2}")
plt.plot(ttN, yNt)
plt.plot(tt, rt, marker = "o", color = "red", linestyle = "None")
plt.plot(ttT, xtT, color = "orange")
plt.xticks(np.arange(5) / 200)
plt.grid()
plt.show()


msf = 1
A = 0.5
for deg1 in np.linspace(-360, 360, 200):
    for deg2 in np.linspace(-360, 360, 200):
        xtT = A * (1 * np.sin(2*np.pi*700*ttT + np.pi / 180 * deg1) + 1 * np.sin(2*np.pi*1200*ttT + np.pi / 180 * deg2))
        diff = xtT - yNt
        ep = np.mean(np.power(diff, 2))
        if ep < msf:
            msf = ep
            print(deg1, deg2, ep)

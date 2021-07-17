import matplotlib.pyplot as plt
import numpy as np
from importlib import reload
from Resources import comsig
import bisect
import ModuleLab1
import ModuleLab2
import ModuleLab4
import ModuleLab5
import ModuleLab6
import ModuleLab7
import ModuleLab8


Fs = 44100
data = np.array([0, 1, 1, 1, 0, 0, 1, 0])
dn = comsig.sigSequ(data, FB = 100)

M = 2
FB = 100
data = np.array([0, 1, 1, 1, 0, 0, 1, 0])
sig_xt = ModuleLab8.cpfskxmtr(2, dn, 44100, 'rect', [], [300, 100])


plt.ylim([-1.5, 1.5])
plt.grid()
plt.plot(sig_xt.timeAxis(), sig_xt.signal(), color = "red")

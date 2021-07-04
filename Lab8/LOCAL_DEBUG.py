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
FB = 100
fc = 300

sig_an = comsig.sigSequ([np.random.randint(0, 2, 10), 2 * np.pi * np.random.rand(10) ], FB)

sig_xt, sig_st = ModuleLab8.askxmtr(sig_an, Fs, 'rect', [], 'noncoh', [fc])
plt.ylim([-2, 2])
plt.grid()
plt.plot(sig_xt.timeAxis(), sig_xt.signal())
plt.plot(sig_st.timeAxis(), sig_st.signal().real)
plt.plot(sig_st.timeAxis(), sig_st.signal().imag)
import matplotlib.pyplot as plt
import numpy as np
from importlib import reload
from Resources import comsig
import ModuleLab5


Fs = 44100
# Sampling rate
f1 = 700
# Test frequency 1
f2 = 720
# Test frequency 1
tlen = 2
# Duration in seconds
tt = np.arange(round(tlen*Fs))/float(Fs) # Time axis
x1t = np.sin(2*np.pi*f1*tt)
# Sine with freq f1
x2t = 0.01*np.cos(2*np.pi*f2*tt) # Attenuated cosine with freq f2
sig_xt = comsig.sigWave(x1t+x2t, Fs, 0) # Combined sinusoidal signal
ModuleLab5.showpsd(sig_xt,[-1000, 1000, -80], Fs) #Plot S_x(f)

1+1==2
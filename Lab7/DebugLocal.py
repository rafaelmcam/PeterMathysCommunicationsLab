
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
reload(ModuleLab1)
reload(ModuleLab2)
reload(ModuleLab4)
reload(ModuleLab5)
reload(ModuleLab6)
reload(ModuleLab7)

fc = 8000
Fs, rt1 = ModuleLab1.wavread("Lab7/Files/speech701.wav")
y = np.zeros(shape = rt1.shape, dtype = np.complex)
sig1 = comsig.sigWave(rt1, Fs)
x1 = ModuleLab7.qamxmtr(sig1, [fc, 0, 0], [4000, 15, 0.05])



1+1
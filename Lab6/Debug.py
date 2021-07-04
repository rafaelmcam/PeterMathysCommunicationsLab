import numpy as np
import matplotlib.pyplot as plt
from Resources import comsig
import ModuleLab1
import ModuleLab2
import ModuleLab4
import ModuleLab5
import ModuleLab6
FB = 815


Fs, rt = ModuleLab1.wavread("Lab6/Files/pamsig601.wav")
sig_xt = comsig.sigWave(rt, Fs, 0)
seq, sig, ixn = ModuleLab6.pamrcvr10(sig_xt, [FB, 0.0], ptype="rect", pparms=[3, 0.5])

1+1
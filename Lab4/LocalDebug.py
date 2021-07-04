import numpy as np
import matplotlib.pyplot as plt
from Resources import comsig
import ModuleLab1
import ModuleLab2
import ModuleLab4


# Para fL = 0.5 * Fb
Fs, rt = ModuleLab1.wavread("Lab4/pamsig403_part2_rcv_N_1_dot5.wav")
sig = comsig.sigWave(rt, Fs, 0)
dly = 0.0
ModuleLab4.showeye(sig, 100, 100, [dly, 3, -0.2, 1.0])


a = 1 + 1
import numpy as np
import matplotlib.pyplot as plt
from Resources import showfun_basic, comsig
import ModuleLab1
import ModuleLab2


string = "Test"
bit_sequence = ModuleLab1.asc2bin(string)
polar = 2 * bit_sequence - 1
polar = np.concatenate((np.zeros(2, ), polar, np.zeros(2,)))
Fs = 44100
Fb = 100
n0 = -2
ss = comsig.sigSequ(polar, FB=Fb, n0=n0)

k = 10
beta = 4

sig = ModuleLab2.pam10(ss, Fs = Fs, ptype="sinc", pparms=[k, beta])
stt = np.array(np.round(Fs * (np.arange(0, len(ss)) + n0) / Fb), dtype=np.int32) - int(np.ceil(Fs * (n0 - 0.5) / Fb))
stt = stt[2:-2]



1+1
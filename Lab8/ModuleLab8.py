import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from Resources import comsig
from ModuleLab6 import pam12


def askxmtr(sig_an, Fs, ptype, pparms, xtype, fcparms):
    """
        Amplitude Shift Keying (ASK) Transmitter for Coherent (’coh’) and Non-coherent (’noncoh’) ASK Signals
        >>>>> sig_xt,sig_st = askxmtr(sig_an,Fs,ptype,pparms,xtype,fcparms) <<<<<
        where
        sig_xt: waveform from class sigWave
        sig_xt.signal(): transmitted ASK signal, sampling rate Fs x(t) = s(t)*cos(2*pi*fc*t+(pi/180)*thetac)
        sig_xt.timeAxis(): time axis for x(t), starts at t=-TB/2
        sig_st: waveform from class sigWave
        sig_st.signal(): baseband PAM signal s(t) for ’coh’
        sig_st.signal(): st = sit + 1j*sqt for ’noncoh’
        sit: PAM signal of an*cos(pi/180*thetacn)
        sqt: PAM signal of an*sin(pi/180*thetacn)
        xtype: Transmitter type from list {’coh’,’noncoh’}
        sig_an: sequence from class sigSequ
        sig_an.signal() = [an] for {’coh’}
        sig_an.signal() = [[an],[thetacn]] for {’noncoh’}
        an: N-symbol DT input sequence a_n, 0<=n<N
        thetacn: N-symbol DT sequence theta_c[n] in degrees, used instead of thetac for {’noncoh’} ASK
        sig_an.get_FB(): baud rate of a_n (and theta_c[n]), TB=1/FB
        Fs: sampling rate of x(t), s(t)
        ptype: pulse type from list [’man’,’rcf’,’rect’,’rrcf’,’sinc’,’tri’]
        pparms = [] for {’man’,’rect’,’tri’}
        pparms = [k, alpha] for {’rcf’,’rrcf’}
        pparms = [k, beta] for {’sinc’}
        k: "tail" truncation parameter for {’rcf’,’rrcf’,’sinc’} (truncates at -k*TB and k*TB)
        alpha: Rolloff parameter for {’rcf’,’rrcf’}, 0<=alpha<=1
        beta: Kaiser window parameter for {’sinc’}
        fcparms = [fc, thetac] for {’coh’}
        fcparms = [fc] for {’noncoh’}
        fc: carrier frequency in Hz
        thetac: carrier phase in deg (0: cos, -90: sin)
        """

    if xtype == "coh":
        fc, thetac = fcparms
        sig_st = pam12(sig_an, Fs, ptype, pparms)
        sig_xt_s = sig_st.signal() * np.cos(
            2 * np.pi * fc * sig_st.timeAxis() + thetac * np.pi / 180)
        sig_xt = comsig.sigWave(sig_xt_s, Fs)
    elif xtype == "noncoh":
        fc = fcparms
        an, thetacn = sig_an.signal()
        ani = an * np.cos(thetacn * np.pi / 180)
        anq = an * np.sin(thetacn * np.pi / 180)
        sig_sti = pam12(
            comsig.sigSequ(ani, Fb=sig_an.get_FB(), n0=sig_an.get_n0()), Fs,
            ptype, pparms)
        sig_stq = pam12(
            comsig.sigSequ(anq, Fb=sig_an.get_FB(), n0=sig_an.get_n0()), Fs,
            ptype, pparms)
        sig_st = comsig.sigWave(sig_sti.signal() + 1j * sig_stq.signal(), Fs)
        x = sig_sti.signal() * np.cos(
            2 * np.pi * fc * sig_sti.timeAxis()) - sig_stq.signal() * np.sin(
                2 * np.pi * fc * sig_stq.timeAxis())
        sig_xt = comsig.sigWave(x, Fs)
    else:
        assert (False)
    return sig_xt, sig_st
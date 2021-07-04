import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from Resources import comsig
from ModuleLab6 import pam12, pamrcvr10


def askrcvr(sig_rt, rtype, fcparms, FBparms, ptype, pparms):
    """
    Amplitude Shift Keying (ASK) Receiver for Coherent (’coh’) and Non-coherent (’noncoh’) ASK Signals
    >>>>> sig_bn,sig_bt,sig_wt,ixn = askrcvr(sig_rt,rtype,fcparms,FBparms,ptype,pparms) <<<<<
    where
    sig_bn: sequence from class sigSequ
    sig_bn.signal(): received DT sequence b[n]
    sig_bt: waveform from class sigWave
    sig_bt.signal(): received ’CT’ PAM signal b(t)
    sig_wt: waveform from class sigWave
    sig_wt.signal(): wt = wit + 1j*wqt
    wit: in-phase component of b(t)
    wqt: quadrature component of b(t)
    ixn: sampling time indexes for b(t)->b[n], w(t)->w[n]
    sig_rt: waveform from class sigWave
    sig_rt.signal(): received (noisy) ASK signal r(t)
    sig_rt.timeAxis(): time axis for r(t)
    rtype: receiver type from list [’coh’,’noncoh’]
    fcparms = [fc, thetac] for {’coh’}
    fcparms = [fc] for {’noncoh’}
    fc: carrier frequency in Hz
    thetac: carrier phase in deg (0: cos, -90: sin)
    FBparms = [FB, dly]
    FB: baud rate of PAM signal, TB=1/FB
    dly: sampling delay for b(t)->b[n], fraction of TB sampling times are t=n*TB+t0 where t0=dly*TB
    ptype: pulse type from list
    [’man’,’rcf’,’rect’,’rrcf’,’sinc’,’tri’]
    pparms = [] for ’man’,’rect’,’tri’
    pparms = [k, alpha] for {’rcf’,’rrcf’}
    pparms = [k, beta]
    for {’sinc’}
    k: "tail" truncation parameter for {’rcf’,’rrcf’,’sinc’} (truncates at -k*TB and k*TB)
    alpha: Rolloff parameter for {’rcf’,’rrcf’}, 0<=alpha<=1
    """
    Fs = sig_rt.get_Fs()
    t0 = sig_rt.get_t0()
    if rtype == "coh":
        fc, thetac = fcparms
        thetacrad = thetac * np.pi / 180
        vt = sig_rt.signal() * 2 * np.cos(2 * np.pi * fc * sig_rt.timeAxis() + thetacrad)
        sig_vt = comsig.sigWave(vt, Fs, t0=t0)
        sig_bn, sig_bt, ixn = pamrcvr10(sig_vt, FBparms=FBparms, ptype=ptype, pparms=pparms)
        wit = sig_bt.signal().real
        wqt = sig_bt.signal().imag
        sig_wt = comsig.sigWave(wit + 1j * wqt, Fs, t0)
    elif rtype == "noncoh":
        fc = fcparms[0]
        vi = sig_rt.signal() * 2 * np.cos(2 * np.pi * fc * sig_rt.timeAxis())
        vq = - sig_rt.signal() * 2 * np.sin(2 * np.pi * fc * sig_rt.timeAxis())
        sig_vi = comsig.sigWave(vi, Fs, t0=t0)
        sig_vq = comsig.sigWave(vq, Fs, t0=t0)
        _, sig_bti, _ = pamrcvr10(sig_vi, FBparms=FBparms, ptype=ptype, pparms=pparms)
        wi = sig_bti.signal().real
        _, sig_btq, _ = pamrcvr10(sig_vq, FBparms=FBparms, ptype=ptype, pparms=pparms)
        wq = sig_btq.signal().real
        bt = (wi ** 2 + wq ** 2) ** 0.5

        # implementação de instantes de amostragem do lab6
        FB, dly = FBparms
        t_dly = dly / FB
        tdiff = sig_rt.timeAxis()[-1] - sig_rt.timeAxis()[0]
        N = np.ceil(FB * tdiff)

        Fs = sig_rt.get_Fs() # Sampling rate
        tt = sig_rt.timeAxis() # Time axis for r(t)
        nn0 = int(np.ceil((tt[0]-t_dly)*FB)) # First data index
                                            # Integer multiple of 1/FB
        ixnn0 = np.argmin(abs(tt-(nn0/float(FB)+t_dly)))
        N = int(np.floor((tt[-1]-tt[ixnn0])*FB)) + 1 # Number of data symbols
        ixn = ixnn0 + np.array(np.around(Fs*(np.arange(N))/float(FB)), np.int64) # Sampling indexes

        bn = bt[ixn]
        sig_bn = comsig.sigSequ(bn, FB)
        sig_bt = comsig.sigWave(bt, Fs, t0)
        sig_wt = comsig.sigWave(wi + 1j * wq, Fs, t0)
    else:
        assert (False)

    return sig_bn, sig_bt, sig_wt, ixn


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
        sig_xt = comsig.sigWave(sig_xt_s, Fs, t0=sig_st.get_t0())
    elif xtype == "noncoh":
        fc = fcparms[0]
        an, thetacn = sig_an.signal()
        ani = an * np.cos(thetacn * np.pi / 180)
        anq = an * np.sin(thetacn * np.pi / 180)
        sig_sti = pam12(
            comsig.sigSequ(ani, FB=sig_an.get_FB(), n0=sig_an.get_n0()), Fs,
            ptype, pparms)
        sig_stq = pam12(
            comsig.sigSequ(anq, FB=sig_an.get_FB(), n0=sig_an.get_n0()), Fs,
            ptype, pparms)
        sig_st = comsig.sigWave(sig_sti.signal() + 1j * sig_stq.signal(),
                                Fs,
                                t0=sig_sti.get_t0())
        x = sig_sti.signal() * np.cos(
            2 * np.pi * fc * sig_sti.timeAxis()) - sig_stq.signal() * np.sin(
                2 * np.pi * fc * sig_stq.timeAxis())
        sig_xt = comsig.sigWave(x, Fs, t0=sig_st.get_t0())
    else:
        assert (False)
    return sig_xt, sig_st
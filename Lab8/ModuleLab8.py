import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from Resources import comsig
from ModuleLab6 import pam12, pamrcvr10

def pam13(sig_an, Fs, ptype, pparms=[]):
    """
    Pulse amplitude modulation: a_n -> s(t), (n0-1/2)*TB<=t<(N+n0-1/2)*TB,
    V1.1 for ’rect’, ’sinc’, and ’tri’ pulse types.
    >>>>> sig_st = pam11(sig_an, Fs, ptype, pparms) <<<<<
    where
    sig_an: sequence from class sigSequ
    sig_an.signal(): N-symbol DT input sequence a_n, n0<=n<N+n0
    sig_an.get_FB(): Baud rate of a_n, TB=1/FB
    sig_an.get_n0(): Start index
    Fs: sampling rate of s(t)
    ptype: pulse type from list (’man’,’rcf’,’rect’,’sinc’,’tri’)
    pparms not used for ’man’,’rect’,’tri’
    pparms = [k, alpha] for ’rcf’
    pparms = [k, beta] for ’sinc’
    k: "tail" truncation parameter for ’rcf’,’sinc’ (truncates p(t) to -k*TB <= t < k*TB)
    alpha: Rolloff parameter for ’rcf’, 0<=alpha<=1
    beta: Kaiser window parameter for ’sinc’
    sig_st: waveform from class sigWave
    sig_st.timeAxis(): time axis for s(t), starts at (n0-1/2)*TB
    sig_st.signal(): CT output signal s(t), (n0-1/2)*TB<=t<(N+n0-1/2)*TB, with sampling rate Fs
    """
    N = len(sig_an)
    Fb = sig_an.get_FB()
    n0 = sig_an.get_n0()
    ixL = int(np.ceil(Fs * (n0 - 0.5) / Fb))
    ixR = int(np.ceil(Fs * (N + n0 - 0.5) / Fb))
    tt = np.arange(ixL, ixR) / Fs
    t0 = tt[0]
    ##
    an = sig_an.signal()
    ast = np.zeros(len(tt))
    ix = np.array(np.round(Fs * (np.arange(0, N) + n0) / Fb), dtype=np.int32)

    # place deltas
    ast[ix - int(ixL)] = Fs * an

    # pam pulse
    ptype = ptype.lower()

    if ptype == "rect":
        kL = -0.5
        kR = -kL
    elif ptype == "tri":
        kL = -1.0
        kR = -kL
    elif ptype == "sinc":
        assert(len(pparms) == 2)
        k, beta = pparms
        kL = -k
        kR = k
    elif ptype == "man":
        kL = -0.5
        kR = -kL
    elif ptype == "rcf":
        assert(len(pparms) == 2)
        k, alpha = pparms
        assert(alpha >= 0 and alpha <= 1)
        kL = -k
        kR = k
    elif ptype == "pr1":
        assert(len(pparms) == 1)
        k = pparms[0]
        kL = -k
        kR = k
    elif ptype == "rrcf":
        assert(len(pparms) == 2)
        k, alpha = pparms
        kL = -k
        kR = k
    else:
        kL = -1.0
        kR = -kL
    
    ixpL = int(np.ceil(Fs * kL / Fb))
    ixpR = int(np.ceil(Fs * kR / Fb))
    ttp = np.arange(ixpL, ixpR) / Fs
    pt = np.zeros(len(ttp))
    
    if ptype == "rect":
        ix = np.where(np.logical_and(ttp >= kL / Fb, ttp < kR / Fb))[0]
        pt[ix] = np.ones(len(ix))
    elif ptype == "tri":
        ix = np.where(np.logical_and(ttp >= kL / Fb, ttp < kR / Fb))[0]
        def tri_pulse(size):
            nt = size - 1
            p1 = np.arange(nt // 2) / (nt / 2)
            p2 = 1 - np.arange(nt - nt // 2 + 1) / (nt - nt // 2)
            return np.concatenate((p1, p2))
        pt[ix] = tri_pulse(len(ix))
    elif ptype == "sinc":
        ix = np.where(np.logical_and(ttp >= kL / Fb, ttp < kR / Fb))[0]
        # cuidado com 0!
        pt[ix] = np.sinc(ttp[ix] * Fb)
        pwt = pt * np.kaiser(len(pt), beta)
        pt = pwt
    elif ptype == "man":
        ix = np.where(np.logical_and(ttp >= kL / Fb, ttp < kR / Fb))[0]
        pt[ix] = np.ones(len(ix))
        ix2 = np.where(np.logical_and(ttp >= kL / Fb, ttp < 0))[0]
        pt[ix2] = -1
    elif ptype == "rcf":
        ix = np.where(np.logical_and(ttp >= kL / Fb, ttp < kR / Fb))[0]
        # pt[ix] = np.sinc(ttp[ix] * Fb) * np.cos(np.pi*alpha*Fb*ttp[ix]) / (1 - ((2*alpha*Fb*ttp[ix]) ** 2))
        pt[ix] = np.sinc(ttp[ix] * Fb) * np.cos(np.pi*alpha*Fb*ttp[ix])
        for idx in ix:
            den = (1 - ((2*alpha*Fb*ttp[idx]) ** 2))
            if den == 0:
                pt[idx] = np.sinc(ttp[idx] * Fb) * (np.pi / 4)
            else:
                pt[idx] /= den
    elif ptype == "pr1":
        ix = np.where(np.logical_and(ttp >= kL / Fb, ttp < kR / Fb))[0]
        for idx in ix:
            den = 1 - ttp[idx] * Fb
            if den == 0:
                pt[idx] = 1
            else:
                pt[idx] = np.sinc(ttp[idx] * Fb) / (1 - ttp[idx] * Fb)
        # pt[ix] = np.sinc(ttp[ix] * Fb)
    elif ptype == "rrcf":
        ix = np.where(np.logical_and(ttp >= kL / Fb, ttp < kR / Fb))[0]
        if alpha == 0:
            alpha += 1e-5
        for idx in ix:
            if ttp[idx] == 0:
                pt[idx] = 1 - alpha + (4 * alpha) / np.pi
            elif abs(ttp[idx]) == 1 / (4 * alpha * Fb):
                pt[idx] = (alpha / np.sqrt(2)) * ((1 + 2 / np.pi) * np.sin(np.pi / (4 * alpha)) + (1 - 2 / np.pi) * np.cos(np.pi / (4 * alpha)))
            else:
                pt[idx] = (1 / (Fb * np.pi)) * (np.sin((1 - alpha)*np.pi*ttp[idx]*Fb) + (4*alpha*ttp[idx]*Fb) * np.cos((1+alpha)*np.pi*ttp[idx]*Fb))
                pt[idx] /= ((1 - (4 * alpha * ttp[idx] * Fb) ** 2) * ttp[idx])
    else:
        raise NotImplementedError("Pulse type not recognized!") 

    st = np.convolve(ast, pt) / Fs
    st = st[-ixpL:ixR-ixL-ixpL]
    return comsig.sigWave(st, Fs, 0)

def cpfskxmtr(M,sig_dn,Fs,ptype,pparms,fcparms, ax = 0):
    """ M-ary Frequency Shift Keying (FSK) Transmitter for Continuous Phase FSK Signals
    >>>>> sig_xt = cpfskxmtr(M,sig_dn,Fs,ptype,pparms,fcparms) <<<<<
    where
    sig_xt: waveform from class sigWave
    sig_xt.signal(): transmitted FSK signal, sampling rate Fs
    sig_xt.timeAxis(): time axis for x(t), starts at t=-TB/2 M: number of distinct symbol values in d[n]
    sig_dn: sequence from class sigSequ
    sig_dn.signal() = dn
    dn: M-ary (0,1,..,M-1) N-symbol DT input sequence d_n
    sig_dn.get_FB(): baud rate of d_n, TB=1/FB
    Fs: sampling rate of x(t)
    ptype: pulse type from set {’man’,’rcf’,’rect’,’rrcf’,’sinc’,’tri’}
    pparms = [] for {’man’,’rect’,’tri’}
    pparms = [k alpha] for {’rcf’,’rrcf’}
    pparms = [k beta] for {’sinc’}
    k: "tail" truncation parameter for {’rcf’,’rrcf’,’sinc’} (truncates p(t) to -k*TB <= t < k*TB)
    alpha: Rolloff parameter for {’rcf’,’rrcf’}, 0<=alpha<=1
    beta: Kaiser window parameter for {’sinc’}
    fcparms = [fc, deltaf]
    fc: carrier frequency for {’cpfsk’}
    deltaf: frequency spacing for {’cpfsk’} for dn=0 -> fc, dn=1 -> fc+deltaf, dn=2 -> fc+2*deltaf, etc
    """
    # if ptype != "rect":
    #     raise NotImplementedError("Lógica feita para pulso retangular (fase variando linearmente dentro do intervalo do símbolo)")

    fc, deltaf = fcparms
    fcv = [fc + i * deltaf for i in range(M)]
    data = sig_dn.signal()
    L = len(data)
    FB = sig_dn.get_FB()
    cs = np.zeros(shape = (M, L))
    for i, symbol in enumerate(data):
        if i == 0:
            cs[symbol][i] += 1
            continue
        for j in range(M):
            cs[j][i] += cs[j][i - 1]
        cs[symbol][i] += 1

    sig_xt_compare = fskxmtr(M = M, sig_dn = sig_dn, Fs = Fs, ptype = ptype, pparms = pparms, xtype = 'coh', fcparms = [fcv, [0 for _ in range(M)]])
    xf = np.zeros(shape = (len(sig_xt_compare.signal()),))

    assert(np.isclose(sum(cs[:, L - 1]), L))
    theta_vec = np.zeros(shape=(L,))
    for i in range(1, L):
        acc = 0
        for j in range(M):
            acc += (fcv[j] * cs[j][i - 1] / FB)
        theta_vec[i] = 2 * np.pi * acc
        theta_vec[i] %= (2 * np.pi)

    ts = int(Fs / FB)
    mt = np.arange(ts) / Fs
    for i, d in enumerate(data):
        f, t = i * ts, (i + 1) * ts
        # print(f, t, theta_vec[i])
        # xf[f:t] = np.cos(2 * np.pi * fcv[d] * mt + theta_vec[i] - np.pi / 2)
        # xf = np.zeros(shape = (len(smi.signal()),))
        for j in range(M):
            fci = fcv[j]
            vec = np.where(sig_dn.signal() == j, 1, 0)
            smi = pam12(comsig.sigSequ([vec[i]], FB), Fs, ptype, pparms)
            xm = smi.signal() * np.cos(2 * np.pi * fci * mt + theta_vec[i] - np.pi / 2)
            xf[f:t] += xm

    return comsig.sigWave(xf, Fs, t0 = - 1 / (2 * FB))


def fskrcvr(M,sig_rt,rtype,fcparms,FBparms,ptype,pparms):
    """ M-ary Frequency Shift Keying (FSK) Receiver for Coherent (’coh’) and Non-coherent (’noncoh’) FSK Reception
    >>>>> sig_bn,sig_wt,ixn = fskrcvr(M,sig_rt,rtype,fcparms,FBparms,ptype,pparms) <<<<<
    where
    sig_bn: sequence from class sigSequ
    sig_bn.signal(): received DT sequence b[n]
    sig_wt: waveform from class sigWave
    sig_wt.signal(): wt = [[w0it+1j*w0qt],[w1it+1j*w1qt],..., [wM-1it+1j*wM-1qt]]
    wmit: m-th in-phase matched filter output
    wmqt: m-th quadrature matched filter output
    ixn: sampling time indexes for b(t)->b[n], w(t)->w[n]
    M: number of distinct FSK frequencies
    sig_rt: waveform from class sigwave
    sig_rt.signal(): received (noisy) FSK signal r(t)
    sig_rt.timeAxis(): time axis for r(t)
    rtype: receiver type from list {’coh’,’noncoh’}
    fcparms = [[fc0,fc1,...,fcM-1], [thetac0,thetac1,...,thetacM-1]] for {'coh'}
    fcparms = [fc0,fc1,...,fcM-1] for {’noncoh’}
    fc0,fc1,...,fcM-1: FSK (carrier) frequencies for {’coh’,’noncoh’}
    thetac0,thetac1,...,thetacM-1: FSK (carrier) phases in deg (0: cos, -90: sin) for {’coh’}
    FBparms = [FB, dly]
    FB: baud rate of PAM signal, TB=1/FB
    dly: sampling delay for wm(t)->wm[n], fraction of TB sampling times are t=n*TB+t0 where t0=dly*TB
    ptype: pulse type from list {’man’,’rcf’,’rect’,’rrcf’,’sinc’,’tri’}
    pparms = [] for {’man’,’rect’,’tri’}
    pparms = [k, alpha] for {’rcf’,’rrcf’}
    pparms = [k, beta] for {’sinc’}
    k: "tail" truncation parameter for {’rcf’,’rrcf’,’sinc’} (truncates at -k*TB and k*TB)
    alpha: Rolloff parameter for {’rcf’,’rrcf’}, 0<=alpha<=1
    beta: Kaiser window parameter for {’sinc’}
    """
    Fs = sig_rt.get_Fs()
    t0 = sig_rt.get_t0()
    FB, dly = FBparms
    t_dly = dly / FB
    tdiff = sig_rt.timeAxis()[-1] - sig_rt.timeAxis()[0]
    tt = sig_rt.timeAxis() # Time axis for r(t)
    nn0 = int(np.ceil((tt[0]-t_dly)*FB)) # First data index
                                        # Integer multiple of 1/FB
    ixnn0 = np.argmin(abs(tt-(nn0/float(FB)+t_dly)))
    N = int(np.floor((tt[-1]-tt[ixnn0])*FB)) + 1 # Number of data symbols
    ixn = ixnn0 + np.array(np.around(Fs*(np.arange(N))/float(FB)), np.int64) # Sampling indexes
    if rtype == "coh":
        vmi = sig_rt.signal() * 2 * np.cos(2 * np.pi * fcparms[0][0] * sig_rt.timeAxis() + fcparms[1][0] * np.pi / 180)
        sig_vt = comsig.sigWave(vmi, Fs, t0)
        sig_bn, sig_bt, ixn = pamrcvr10(sig_vt, FBparms=FBparms, ptype=ptype, pparms=pparms)
        L = len(sig_bn.signal())
        wvn = np.zeros(shape = (M, L))
        wv = []
        for i in range(M):
            vmi = sig_rt.signal() * 2 * np.cos(2 * np.pi * fcparms[0][i] * sig_rt.timeAxis() + fcparms[1][i] * np.pi / 180)
            sig_vt = comsig.sigWave(vmi, Fs, t0)
            sig_bn, sig_bt, ixn = pamrcvr10(sig_vt, FBparms=FBparms, ptype=ptype, pparms=pparms)
            wvn[i] = sig_bn.signal()
            wit = sig_bt.signal().real
            wqt = sig_bt.signal().imag
            wv.append(wit + 1j * wqt)
        sig_bnd = np.argmax(wvn, axis = 0)
        sig_bn = comsig.sigSequ(sig_bnd, FB)
        sig_wt = comsig.sigWave(wv, Fs, t0)
    elif rtype == "noncoh":
        vmi = sig_rt.signal() * 2 * np.cos(2 * np.pi * fcparms[0] * sig_rt.timeAxis())
        sig_vt = comsig.sigWave(vmi, Fs, t0)
        sig_bn, sig_bt, ixn = pamrcvr10(sig_vt, FBparms=FBparms, ptype=ptype, pparms=pparms)
        L = len(sig_bn.signal())
        wvn = np.zeros(shape = (M, L))
        wv = []
        for i in range(M):
            vmi =   sig_rt.signal() * 2 * np.cos(2 * np.pi * fcparms[i] * sig_rt.timeAxis())
            vmq = - sig_rt.signal() * 2 * np.sin(2 * np.pi * fcparms[i] * sig_rt.timeAxis())

            sig_vti = comsig.sigWave(vmi, Fs, t0)
            sig_vtq = comsig.sigWave(vmq, Fs, t0)
            _, sig_bti, _ = pamrcvr10(sig_vti, FBparms=FBparms, ptype=ptype, pparms=pparms)
            _, sig_btq, _ = pamrcvr10(sig_vtq, FBparms=FBparms, ptype=ptype, pparms=pparms)

            wi = sig_bti.signal().real
            wq = sig_btq.signal().real
            bt = (wi ** 2 + wq ** 2) ** 0.5
            wvn[i] = bt[ixn]

            wv.append(wi + 1j * wq)
        sig_bnd = np.argmax(wvn, axis = 0)
        sig_bn = comsig.sigSequ(sig_bnd, FB)
        sig_wt = comsig.sigWave(wv, Fs, t0)
    else:
        raise NotImplementedError("rtype deve ser 'coh' ou 'noncoh'")
    return sig_bn, sig_wt, ixn



def fskxmtr(M,sig_dn,Fs,ptype,pparms,xtype,fcparms):
    """ M-ary Frequency Shift Keying (FSK) Transmitter for Choherent (’coh’) and Non-coherent (’noncoh’) FSK Signals
    >>>>> sig_xt = fskxmtr(M,sig_dn,Fs,ptype,pparms,xtype,fcparms) <<<<<
    where
    sig_xt: waveform from class sigWave
    sig_xt.signal(): transmitted FSK signal, sampling rate Fs
    sig_xt.timeAxis(): time axis for x(t), starts at t=-TB/2
    M: number of distinct symbol values in d[n]
    xtype: Transmitter type from set {’coh’,’noncoh’}
    sig_dn: sequence from class sigSequ sig_dn.signal() = [dn] for [’coh’]
    sig_dn.signal() = [[dn],[thetacn]] for [’noncoh’]
    dn: M-ary (0,1,..,M-1) N-symbol DT input sequence d_n
    thetacn: N-symbol DT sequence theta_c[n] in degrees, used instead of thetac0..thetacM-1 for {’noncoh’} FSK
    sig_dn.get_FB(): baud rate of d_n (and theta_c[n]), TB=1/FB
    Fs: sampling rate of x(t)
    ptype: pulse type from set {’man’,’rcf’,’rect’,’rrcf’,’sinc’,’tri’}
    pparms = [] for {’man’,’rect’,’tri’}
    pparms = [k alpha] for {’rcf’,’rrcf’}
    pparms = [k beta] for {’sinc’}
    k: "tail" truncation parameter for {’rcf’,’rrcf’,’sinc’}
    (truncates p(t) to -k*TB <= t < k*TB)
    alpha: Rolloff parameter for {’rcf’,’rrcf’}, 0<=alpha<=1
    beta: Kaiser window parameter for {’sinc’}
    fcparms = [[fc0,fc1,...,fcM-1],[thetac0,thetac1,...,thetacM-1]] for {’coh’}
    fcparms = [fc0,fc1,...,fcM-1] for {’noncoh’}
    fc0,fc1,...,fcM-1: FSK (carrier) frequencies for {’coh’,’noncoh’}
    thetac0,thetac1,...,thetacM-1: FSK (carrier) phases in deg (0: cos, -90: sin) for {'coh'}
    """

    FB = sig_dn.get_FB()
    if xtype == 'coh':
        vec = np.where(sig_dn.signal() == 0, 1, 0)
        smi = pam12(comsig.sigSequ(vec, FB), Fs, ptype, pparms)

        xf = np.zeros(shape = (len(smi.signal()),))
        for i in range(M):
            fci, thetai = fcparms[0][i], fcparms[1][i]
            vec = np.where(sig_dn.signal() == i, 1, 0)
            smi = pam12(comsig.sigSequ(vec, FB), Fs, ptype, pparms)
            xm = smi.signal() * np.cos(2 * np.pi * fci * smi.timeAxis() + thetai * np.pi / 180)
            xf += xm
    elif xtype == 'noncoh':
        vec = np.where(sig_dn.signal() == 0, 1, 0)
        smi = pam12(comsig.sigSequ(vec, FB), Fs, ptype, pparms)

        L = len(sig_dn.signal())
        xf = np.zeros(shape = (len(smi.signal()),))
        theta_vec = 360 * np.random.rand(L)
        ntheta = np.repeat(theta_vec, int(Fs / FB))
        for i in range(M):
            fci = fcparms[i]
            vec = np.where(sig_dn.signal() == i, 1, 0)
            smi = pam12(comsig.sigSequ(vec, FB), Fs, ptype, pparms)
            xm = smi.signal() * np.cos(2 * np.pi * fci * smi.timeAxis() + ntheta * np.pi / 180)
            xf += xm
    elif xtype == 'fixed_noncoh':
        vec = np.where(sig_dn.signal() == 0, 1, 0)
        smi = pam12(comsig.sigSequ(vec, FB), Fs, ptype, pparms)

        L = len(sig_dn.signal())
        xf = np.zeros(shape = (len(smi.signal()),))
        theta_vec = fcparms[1]
        ntheta = np.repeat(theta_vec, int(Fs / FB))
        for i in range(M):
            fci = fcparms[0][i]
            vec = np.where(sig_dn.signal() == i, 1, 0)
            smi = pam12(comsig.sigSequ(vec, FB), Fs, ptype, pparms)
            xm = smi.signal() * np.cos(2 * np.pi * fci * smi.timeAxis() + ntheta * np.pi / 180)
            xf += xm
    else:
        raise NotImplementedError("xtype deve ser 'coh' ou 'noncoh'")

    return comsig.sigWave(xf, Fs, t0 = - 1 / (2 * FB))


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
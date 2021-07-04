import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from Resources import comsig


def pamhRt(sps, ptype, pparms=[]):
    """
    PAM normalized matched filter (MF) receiver filter h_R(t) = h_R(n*TB/sps) generation
    >>>>> hRt = pamhRt(sps, ptype, pparms) <<<<<
        where
            sps: samples per symbol
            ptype: pulse type from list (’man’, ’rcf’, ’rect’, ’rrcf’, ’sinc’, ’tri’)
            pparms not used for ’man’, ’rect’, ’tri’
            pparms = [k, alpha] for ’rcf’, ’rrcf’
            pparms = [k, beta] for ’sinc’
            k: "tail" truncation parameter for ’rcf’, ’rrcf’, ’sinc’ (truncates p(t) to -k*sps <= n < k*sps)
            alpha: Rolloff parameter for ’rcf’, ’rrcf’, 0 <= alpha <= 1
            beta: Kaiser window parameter for 'sinc'
            hRt: Matched Filter impulse response h_R(t) at t = n*TB/sps
        Note: sps = Fs / FB
    """
    # time reversed and normalized
    pt = pampt(sps, ptype, pparms)
    ht = pt[::-1]
    hRt = ht / np.sum(np.power(pt,2.0))
    return hRt



def pampt(sps, ptype, pparms=[]):
    """
    PAM pulse p(t) = p(n*TB/sps) generation
    >>>>> pt = pampt(sps, ptype, pparms) <<<<<
    where sps:
    ptype: pulse type (’rect’, ’sinc’, ’tri’, 'man', 'rcf', 'rrcf')
    pparms not used for ’rect’, ’tri’, 'man'
    pparms = [k, beta] for sinc
    pparms = [k, alpha] for rcf and rrcf
    k:
    "tail" truncation parameter for ’sinc’
    (truncates p(t) to -k*sps <= n < k*sps)
    beta: Kaiser window parameter for ’sinc’
    pt:
    pulse p(t) at t=n*TB/sps
    Note: In terms of sampling rate Fs and baud rate FB,
    """

    if ptype == "rect":
        pt = np.ones(shape=(sps,), dtype=np.float32)
    elif ptype == "tri":
        def tri_pulse(size):
            nt = size - 1
            p1 = np.arange(nt // 2) / (nt / 2)
            p2 = 1 - np.arange(nt - nt // 2 + 1) / (nt - nt // 2)
            return np.concatenate((p1, p2[:-1]))
        pt = tri_pulse(2 * sps + 1)
    elif ptype == "sinc":
        k, beta = pparms
        # -k a k (definição anterior)? -2k a 2k (padding a esquerda e a direita)?
        tt = np.arange(-k * 1 * sps, k * 1 * sps) / sps
        pt = np.sinc(tt)
        pwt = pt * np.kaiser(pt.size, beta)
        pt = pwt
    elif ptype == "man":
        pt = np.ones(shape=(sps,), dtype=np.float32)
        pt[sps//2:] = -1
    elif ptype == "rcf":
        k, alpha = pparms
        tt = np.arange(-k * 1 * sps, k * 1 * sps) / sps
        pt = np.sinc(tt) * np.cos(np.pi*alpha*tt)
        for i in range(len(tt)):
            vl = 1 - ((2 * alpha * tt[i]) ** 2)
            if vl == 0:
                pt[i] = 0
            else:
                pt[i] /= vl
    elif ptype == "rrcf":
        k, alpha = pparms
        ttp = np.arange(-k * 1 * sps, k * 1 * sps) / sps
        pt = np.empty(shape=(ttp.size,))
        Fb = 1
        for idx in range(len(ttp)):
            if ttp[idx] == 0:
                pt[idx] = 1 - alpha + (4 * alpha) / np.pi
            elif abs(ttp[idx]) == 1 / (4 * alpha * Fb):
                pt[idx] = (alpha / np.sqrt(2)) * ((1 + 2 / np.pi) * np.sin(np.pi / (4 * alpha)) + (1 - 2 / np.pi) * np.cos(np.pi / (4 * alpha)))
            else:
                pt[idx] = (1 / (Fb * np.pi)) * (np.sin((1 - alpha)*np.pi*ttp[idx]*Fb) + (4*alpha*ttp[idx]*Fb) * np.cos((1+alpha)*np.pi*ttp[idx]*Fb))
                pt[idx] /= ((1 - (4 * alpha * ttp[idx] * Fb) ** 2) * ttp[idx])
    else:
        raise NotImplementedError("p(t) not implemented: ", ptype)
    return pt


def pamrcvr10(sig_rt, FBparms, ptype, pparms=[]):
    """
    Pulse amplitude modulation receiver with matched filter:
    r(t) -> b(t) -> bn.
    V1.0 for 'man', 'rcf', 'rect', 'rrcf', 'sinc', and 'tri'
    pulse types.
    >>>>> sig_bn, sig_bt, ixn = pamrcvr10(sig_rt, FBparms, ptype, pparms) <<<<<
        where
            sig_rt: waveform from class sigWave
            sig_rt.signal(): received (noisy) PAM signal r(t)
            sig_rt.timeAxis(): time axis for r(t)
            FBparms: = [FB, dly]
            FB: Baud rate of PAM signal, TB=1/FB
            dly: sampling delay for b(t) -> b_n as a fraction of TB sampling times are t=n*TB+t_dly where t_dly = dly*TB
            ptype: pulse type from list (’man’,’rcf’,’rect’,’rrcf’,’sinc’,’tri’)
            pparms not used for ’man’,’rect’,’tri’
            pparms = [k, alpha] for ’rcf’,’rrcf’
            pparms = [k, beta] for ’sinc’
            k: "tail" truncation parameter for ’rcf’,’rrcf’,’sinc’ (truncates p(t) to -k*TB <= t < k*TB)
            alpha: rolloff parameter for (’rcf’,’rrcf’), 0<=alpha<=1
            beta: Kaiser window parameter for ’sinc’
            sig_bn: sequence from class sigSequ
            sig_bn.signal(): received DT sequence after sampling at t=n*TB+t0
            sig_bt: waveform from class sigWave
            sig_bt.signal(): received PAM signal b(t) at output of matched filter
            ixn: indexes where b(t) is sampled to obtain b_n
    """
    if type(FBparms)==int or type(FBparms)==float:
        FB, t_dly = FBparms, 0 # Get FBparms parameters
    else:
        FB, t_dly = FBparms[0], 0
        if len(FBparms) > 1:
            t_dly = FBparms[1] / float(FB)

    Fs = sig_rt.get_Fs() # Sampling rate
    rt = sig_rt.signal() # Received signal r(t)
    tt = sig_rt.timeAxis() # Time axis for r(t)
    nn0 = int(np.ceil((tt[0]-t_dly)*FB)) # First data index
                                         # Integer multiple of 1/FB
    ixnn0 = np.argmin(abs(tt-(nn0/float(FB)+t_dly)))
    N = int(np.floor((tt[-1]-tt[ixnn0])*FB)) + 1 # Number of data symbols

    # ***** Set up matched filter response h_R(t) *****
    ptype = ptype.lower() # Convert ptype to lowercase
                          # Set left/right limits for p(t)
    if (ptype=='rect'): # Rectangular p(t)
        kL = -0.5; kR = -kL
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
    elif ptype == "rrcf":
        assert(len(pparms) == 2)
        k, alpha = pparms
        kL = -k
        kR = k
    else:
        kL = -1.0
        kR = -kL
    ixpL = int(np.ceil(Fs*kL/float(FB))) # Left index for p(t) time axis
    ixpR = int(np.ceil(Fs*kR/float(FB))) # Right index for p(t) time axis
    ttp = np.arange(ixpL,ixpR)/float(Fs) # Time axis for p(t)
    pt = np.zeros(ttp.size) # Initialize pulse p(t)
    Fb = FB
    if (ptype=='rect'): # Rectangular p(t)
        ix = np.where(np.logical_and(ttp>=kL/float(FB), ttp<kR/float(FB)))[0]
        # print(ix, ix.shape)
        pt[ix] = 1
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
        pt[ix] = np.sinc(ttp[ix] * Fb) * np.cos(np.pi*alpha*Fb*ttp[ix]) / (1 - ((2*alpha*Fb*ttp[ix]) ** 2))
    elif ptype == "rrcf":
        ix = np.where(np.logical_and(ttp >= kL / Fb, ttp < kR / Fb))[0]
        for idx in ix:
            if ttp[idx] == 0:
                pt[idx] = 1 - alpha + (4 * alpha) / np.pi
            elif abs(ttp[idx]) == 1 / (4 * alpha * Fb):
                pt[idx] = (alpha / np.sqrt(2)) * ((1 + 2 / np.pi) * np.sin(np.pi / (4 * alpha)) + (1 - 2 / np.pi) * np.cos(np.pi / (4 * alpha)))
            else:
                pt[idx] = (1 / (Fb * np.pi)) * (np.sin((1 - alpha)*np.pi*ttp[idx]*Fb) + (4*alpha*ttp[idx]*Fb) * np.cos((1+alpha)*np.pi*ttp[idx]*Fb))
                pt[idx] /= ((1 - (4 * alpha * ttp[idx] * Fb) ** 2) * ttp[idx])
    else:
        print(f"ptype {ptype} is not recognized")

    hRt = pt[::-1] # h_R(t) = p(-t)
    hRt = Fs/np.sum(np.power(pt,2.0))*hRt # h_R(t) normalized
    # ***** Filter r(t) with matched filter h_R(t) *****
    bt = np.convolve(rt,hRt) / float(Fs) # Matched filter b(t)=r(t)*h_R(t)
    bt = bt[-ixpL:len(tt)-ixpL] # Trim b(t)
    # ***** Sample b(t) at t=n*TB+t0 to obtain b_n *****
    ixn = ixnn0 + np.array(np.around(Fs*(np.arange(N))/float(FB)), np.int64) # Sampling indexes
                                                                           # DT sequence sampled at t=n*TB+t_dly
    bn = bt[ixn]
    return comsig.sigSequ(bn,FB,nn0), comsig.sigWave(bt,Fs,tt[0]), ixn
    



def pam12(sig_an, Fs, ptype, pparms=[]):
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
                pt[idx] = 0
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
    return comsig.sigWave(st, Fs, t0)



def trapfilt_taps(N, phiL, alfa):
    """
    Returns taps for order N FIR LPF with trapezoidal frequency
    response, normalized cutoff frequency phiL = fL/Fs, and rolloff
    parameter alfa.
    >>>>> hLn = trapfilt_taps(N, phiL, alfa) <<<<<
    where
        N: filter order
        phiL: normalized cutoff frequency (-6 dB)
        alfa: frequency rolloff parameter, linear rolloff over range (1-alfa)phiL <= |f| <= (1+alfa)phiL
    """
    # fazendo algo similar a função trapfilt, mas agora usando coo parâmetro de entrada a ordem do filtro (o filtro é implementado agora em função de parâmetros discretos) (parecido com pampt)
    tt = np.arange(N) - N / 2
    assert(tt.size == N)
    if alfa == 0:
        ht_num =  np.sin(2 * np.pi * phiL * tt)
        ht_den = (np.pi * tt)
    else:
        ht_num =  np.sin(2 * np.pi * phiL * tt) * np.sin(2 * np.pi * alfa * phiL * tt)
        ht_den = (np.pi * tt) *  (2 * np.pi * alfa * phiL * tt)

    for s in np.where(ht_den == 0):
        ht_num[s] = 2 * phiL
        ht_den[s] = 1
        # fazendo com que t = 0 h[t] = 2 * fL

    ht = ht_num / ht_den
    return ht


def trapfilt(sig_xt, fL, k, alfa):
    """
    Delay compensated FIR LPF/BPF filter with trapezoidal frequency response.
    >>>>> sig_yt, n = trapfilt(sig_xt, fL, k, alfa) <<<<<
    where
        sig_yt: waveform from class sigWave
            sig_yt.signal(): filter output y(t), samp rate Fs
            n: filter order
        sig_xt: waveform from class sigWave
            sig_xt.signal(): filter input x(t), samp rate Fs
            sig_xt.get_Fs(): sampling rate for x(t), y(t)
        fL: LPF cutoff frequency (-6 dB) in Hz
        k: h(t) is truncated to |t| <= k/(2*fL)
        alfa: frequency rolloff parameter, linear rolloff over range (1-alfa)fL <= |f| <= (1+alfa)fL
    """
    xt = sig_xt.signal() # Input signal
    Fs = sig_xt.get_Fs() # Sampling rate
    ixk = round(Fs*k/float(2*fL)) # Tail cutoff index
    tth = np.arange(-ixk,ixk+1)/float(Fs) # Time axis for h(t)
    n = len(tth)-1 # Filter order
    ### 
    # ***** Generate impulse response ht here *****
    if alfa == 0:
        ht_num =  np.sin(2 * np.pi * fL * tth)
        ht_den = (np.pi * tth)
    else:
        ht_num =  np.sin(2 * np.pi * fL * tth) * np.sin(2 * np.pi * alfa * fL * tth)
        ht_den = (np.pi * tth) *  (2 * np.pi * alfa * fL * tth)

    for s in np.where(ht_den == 0):
        ht_num[s] = 2 * fL
        ht_den[s] = 1
        # fazendo com que t = 0 h[t] = 2 * fL

    ht = ht_num / ht_den
    # ht[tth > (k / (2 * fL))] = 0
    # ht[tth < (- k / (2 * fL))] = 0

    ###
    yt = lfilter(ht, 1, np.hstack((xt, np.zeros(ixk))))/float(Fs) # Compute filter output y(t)
    yt = yt[ixk:] # Filter delay compensation

    yt *= Fs
    return comsig.sigWave(yt, Fs, sig_xt.get_t0()), n # Return y(t) and filter order
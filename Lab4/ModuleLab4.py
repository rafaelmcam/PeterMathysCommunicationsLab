import numpy as np
import matplotlib.pyplot as plt
from Resources import comsig

def showeye(sig_rt, FB, NTd=50, dispparms=[]):
    """
    Display eye diagram of digital PAM signal r(t)
    >>>>> showeye(sig_rt, FB, NTd, dispparms) <<<<<
    where
    sig_rt: waveform from class sigWave
    sig_rt.signal(): received PAM signal r(t)=sum_n a_n*q(t-nTB)
    sig_rt.get_Fs(): sampling rate for r(t)
    FB: Baud rate of DT sequence a_n, TB = 1/FB
    NTd: Number of traces displayed
    dispparms = [delay, width, ylim1, ylim2]
    delay: trigger delay (in TB units, e.g., 0.5
     width: display width (in TB units, e.g., 3)
     ylim1: lower display limit, vertical axis
     ylim2: upper display limit, vertical axis
     """
    rt = sig_rt.signal() # Get r(t)
    Fs = sig_rt.get_Fs() # Sampling rate
    t0 = dispparms[0]/float(FB) # Delay in sec
    tw = dispparms[1]/float(FB) # Display width in sec
    dws = int(np.floor(Fs*tw)) # Display width in samples
    tteye = np.arange(dws)/float(Fs) # Time axis for eye
    trix = np.array(np.around(Fs*(t0+np.arange(NTd)/float(FB))), int)
    ix = np.where(np.logical_and(trix>=0, trix<=len(rt)-dws))[0]
    trix = trix[ix] # Trigger indexes within r(t)
    TM = rt[trix[0]:trix[0]+dws] # First trace
    for tr in range(1, NTd):
        TM = np.vstack((TM, rt[trix[tr]:trix[tr]+dws])) # Second trace
    plt.figure()
    plt.title(r"Eye Diagram for r(t) with $F_B$ = {:.2f} Baud, $t_0$ = {} * $T_B$, #Traces = {}".format(FB,dispparms[0],NTd))
    plt.xlabel(r't/$T_B$')
    plt.ylabel('r(t)')
    plt.ylim([dispparms[2],dispparms[3]])

    plt.plot(FB*tteye, TM.T, '-b') # Plot transpose of TM
    plt.grid()
    plt.show()


def pam11(sig_an, Fs, ptype, pparms=[]):
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
    else:
        raise NotImplementedError("Pulse type not recognized!") 

    st = np.convolve(ast, pt) / Fs
    st = st[-ixpL:ixR-ixL-ixpL]
    return comsig.sigWave(st, Fs, t0)

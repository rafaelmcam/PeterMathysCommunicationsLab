import numpy as np
import matplotlib.pyplot as plt
from Resources import comsig


def pam10(sig_an, Fs, ptype, pparms=[]):
    """ Pulse amplitude modulation: 
        a_n -> s(t), -TB/2<=t<(N-1/2)*TB, 
        V1.0 for ’rect’, ’sinc’, and ’tri’ pulse types. >>>>> 
        sig_st = pam10(sig_an, Fs, ptype, pparms) <<<<< 
        where   sig_an: sequence from class sigSequ 
                sig_an.signal(): N-symbol DT input sequence a_n, 0 <= n < N 
                sig_an.get_FB(): Baud rate of a_n, TB=1/FB 
                Fs: sampling rate of s(t) 
                ptype: pulse type (’rect’,’sinc’,’tri’) 
                pparms not used for ’rect’,’tri’ pparms = [k, beta] for ’sinc’ 
                k: "tail" truncation parameter for ’sinc’ (truncates p(t) to -k*TB <= t < k*TB) 
                beta: Kaiser window parameter for ’sinc’ (0 to 8, 0 corresponds to rectangular window)
                sig_st: waveform from class sigWave 
                sig_st.timeAxis(): time axis for s(t), starts at -TB/2 
                sig_st.signal(): CT output signal s(t), -TB/2<=t<(N-1/2)*TB, with sampling rate Fs 
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
    else:
        raise NotImplementedError("Pulse type not recognized!") 

    st = np.convolve(ast, pt) / Fs
    st = st[-ixpL:ixR-ixL-ixpL]
    return comsig.sigWave(st, Fs, t0)


def showft(sig_xt, ff_lim):
    """
    Plot (DFT/FFT approximation to) Fourier transform of waveform x(t)
    Displays magnitude |X(f)| either linear and absolute or normalized
    (wrt maximum value) in dB. Phase of X(f) is shown in degrees.
    >>>>> showft(sig_xt, ff_lim) <<<<<
    where  sig_xt:   waveform from class sigWave
           sig_xt.timeAxis(): time axis for x(t)
           sig_xt.signal():   sampled CT signal x(t)
           ff_lim = [f1, f2, llim]
           f1:       lower frequency limit for display
           f2:       upper frequency limit for display
           llim = 0: display |X(f)| linear and absolute
           llim > 0: same as llim = 0 but phase is masked
                     for |X(f)| < llim
           llim < 0: display 20*log_{10}(|X(f)|/max(|X(f)|))
                     in dB with lower display limit llim dB,
                     phase is masked (set to zero) for X(f)
                     with magnitude (dB, normalized) < llim
    """
    # ***** Prepare x(t), swap pos/neg parts of time axis *****
    N = len(sig_xt)           # blocklength of DFT/FFT
    Fs = sig_xt.get_Fs()      # sampling rate
    tt = sig_xt.timeAxis()    # get time axis for x(t)
    ixp = np.where(tt>=0)[0]  # indexes for t>=0
    ixn = np.where(tt<0)[0]   # indexes for t<0
    xt = sig_xt.signal()      # get x(t)
    xt = np.hstack((xt[ixp], xt[ixn]))
                              # swap pos/neg time axis parts
    # ***** Compute X(f), make frequency axis *****
    Xf = np.fft.fft(xt)/float(Fs)   # DFT/FFT of x(t),
                              # scaled for X(f) approximation
    Df = Fs/float(N)          # frequency resolution
    ff = Df*np.arange(N)      # frequency axis [0...Fs)

    f1, f2, llim = ff_lim
    nff = ff.copy()
    nxf = Xf.copy()
    if f1 < 0:
        # swap freqs
        Clower = -N // 2 + (1 if N % 2 == 1 else 0)
        Cupper = N // 2 + (1 if N % 2 == 1 else 0)
        nff = (Fs / N) * np.arange(Clower, Cupper)

        assert(nxf.size == N)
        nxf = nxf[[((i + (N // 2 + (1 if N % 2 == 1 else 0))) % N) for i in range(N)]]
    idxs = np.where((nff <= f2) & (nff >= f1))[0]
    
    nff = nff[idxs]
    Xf = nxf

    # ***** Compute |X(f)|, arg[X(f)] *****
    absXf = np.abs(Xf)[idxs]        # magnitude |X(f)|
    argXf = np.angle(Xf)[idxs]      # phase arg[X(f)]

    if llim > 0:
        argXf[np.where(absXf < llim)] = 0
    elif llim < 0:
        mx = np.max(absXf)
        normalized = absXf / mx
        # mask apenas para não ter problemas com log10 de 0
        delete_mask = normalized < 10 ** ((llim - 1) / 20)
        normalized[delete_mask] = 1
        absXf = 20 * np.log10(normalized)
        argXf[np.where(absXf < llim)] = 0
        argXf[delete_mask] = 0
        absXf[delete_mask] = llim - 1
        absXf[np.where(absXf < llim)] = llim - 1

    # ***** Plot magnitude/phase *****
    f1 = plt.figure()
    af11 = f1.add_subplot(211)
    # af11.stem(nff, absXf, use_line_collection = True)  # plot magnitude (linear)
    af11.plot(nff, absXf, '-b')  # plot magnitude (linear)
    if llim < 0:
        af11.set_ylim([llim, 0])
    strt = 'FT Approximation, $F_s$={:.2f} Hz'.format(Fs)
    strt = strt + ', $N$={}'.format(N)
    strt = strt + ', $\Delta_f$={:3.2f} Hz'.format(Df)
    af11.set_title(strt)
    if llim < 0:
        af11.set_ylabel('20$log_{10}(|X(f)|)$ [dB]')
    else:
        af11.set_ylabel('$|X(f)|$')
    af11.grid()
    af12 = f1.add_subplot(212)
    af12.plot(nff, (180/np.pi*argXf), '-b')  # plot phase in degrees
    af12.set_yticks([-180, -100, 0, 100, 180])
    af12.set_ylabel('$\\angle X(f)$ [deg]')
    af12.set_xlabel('$f$ [Hz]')
    af12.grid()
    plt.tight_layout()
    plt.show()
    ## retornando valores do plot (para abs(Xf))
    return nff, absXf, argXf
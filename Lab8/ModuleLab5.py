import numpy as np
import matplotlib.pyplot as plt
from Resources import comsig


def showpsd(sig_xt, ff_lim, N):
    """
    Plot (DFT/FFT approximation to) power spectral density (PSD) of x(t).
    Displays S_x(f) either linear and absolute or normalized in dB.
    >>>>> showpsd(sig_xt, ff_lim, N) <<<<<
    where
    sig_xt: waveform from class sigWave
    sig_xt.signal(): sampled CT signal x(t)
    sig_xt.get_Fs(): sampling rate of x(t)
    ff_lim = [f1,f2,llim]
    f1: lower frequency limit for display
    f2: upper frequency limit for display
    llim = 0: display S_x(f) linear and absolute
    llim < 0: display 10*log_{10}(S_x(f)/max(S_x(f))) in dB with lower display limit llim dB
    N: blocklength
    """

    # ***** Determine number of blocks, prepare x(t) *****
    xt = sig_xt.signal() # Get x(t)
    Fs = sig_xt.get_Fs() # Sampling rate of x(t)
    N = int(min(N, len(xt))) # N <= length(xt) needed
    NN = int(np.floor(len(xt)/float(N))) # Number of blocks of length N
    xt = xt[0:N*NN] # Truncate x(t) to NN blocks
    xNN = np.reshape(xt,(NN,N)) # NN row vectors of length N
    # ***** Compute DFTs/FFTs, average over NN blocks *****
    Sxf = np.power(abs(np.fft.fft(xNN)), 2.0) # NN FFTs, mag square


    if NN > 1:
        Sxf = np.sum(Sxf, axis=0)/float(NN)
    Sxf = Sxf/float(N*Fs) # Correction factor DFT -> PSD
    Sxf = np.reshape(Sxf,np.size(Sxf))
    ff = Fs*np.array(np.arange(N),np.int64)/float(N) # Frequency axis
    if ff_lim[0] < 0: # Negative f1 case
        ixp = np.where(ff<0.5*Fs)[0] # Indexes of pos frequencies
        ixn = np.where(ff>=0.5*Fs)[0] # Indexes of neg frequencies
        ff = np.hstack((ff[ixn]-Fs,ff[ixp])) # New freq axis
        Sxf = np.hstack((Sxf[ixn],Sxf[ixp])) # Corresponding S_x(f)
    
    if ff_lim[2] > 0:
        raise AssertionError("Documentação permite apenas llim <= 0")

    px = sum(Sxf)
    ixf = np.where(np.logical_and(ff>=ff_lim[0], ff<ff_lim[1]))[0]
    lpx = sum(Sxf[ixf])
    ff = ff[ixf] # Trim to ff_lim specs
    if ff_lim[2] < 0:
        absXf = np.abs(Sxf)
        mx = np.max(absXf)
        normalized = absXf / mx
        # mask apenas para não ter problemas com log10 de 0
        delete_mask = normalized < 10 ** ((ff_lim[2] - 1) / 10)
        normalized[delete_mask] = 1
        absXf = 10 * np.log10(normalized)
        absXf[delete_mask] = ff_lim[2] - 1
        absXf[np.where(absXf < ff_lim[2])] = ff_lim[2] - 1
        Sxf = absXf
    Sxf = Sxf[ixf]
    
    df = Fs / float(N)

    strgy = r"PSD: $S_x(f)$" # ylabel string
    # ***** Plot PSD *****
    strgt = r"$P_x = ${:.2}, $P_x(f_1, f_2)=${:.2}".format(px, lpx)
    strgt = strgt + ", PSD Approximation, $F_s=${:d} Hz".format(Fs)
    strgt = strgt + ", $\\Delta_f=${:.3g} Hz".format(df)
    strgt = strgt + ", $NN=${:d}, $N=${:d}".format(NN, N)
    f1 = plt.figure()
    af1 = f1.add_subplot(111)
    if ff_lim[2] < 0:
        strgt = r"$P_x = ${:.2}, $P_x(f_1, f_2)=${:.2f}%".format(px, 100 * lpx/px)
        strgt = strgt + ", PSD Approximation, $F_s=${:d} Hz".format(Fs)
        strgt = strgt + ", $\\Delta_f=${:.3g} Hz".format(df)
        strgt = strgt + ", $NN=${:d}, $N=${:d}".format(NN, N)
        strgy = '10$log_{10}(|X(f)|)$ [dB]'
        af1.set_ylim([ff_lim[2], 0])
    af1.plot(ff, Sxf, "-b")
    af1.grid()
    af1.set_xlabel("f [Hz]")
    af1.set_ylabel(strgy)
    af1.set_title(strgt)
    plt.show()
    return ff, Sxf


def pampt(sps, ptype, pparms=[]):
    """
    PAM pulse p(t) = p(n*TB/sps) generation
    >>>>> pt = pampt(sps, ptype, pparms) <<<<<
    where sps:
    ptype: pulse type (’rect’, ’sinc’, ’tri’)
    pparms not used for ’rect’, ’tri’
    pparms = [k, beta] for sinc
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
                pt[i] = np.sinc(tt) * (np.pi / 4)
            else:
                pt[i] /= vl
    else:
        raise NotImplementedError("p(t) not implemented")
    return pt
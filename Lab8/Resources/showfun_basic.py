# File: showfun_basic.py
# Defines "show" functions like showft, showpsd, etc
import numpy as np
import matplotlib.pyplot as plt

def showft(sig_xt, ff_lim):
    # This version only implements the most basic functionality
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
    # ***** Compute |X(f)|, arg[X(f)] *****
    absXf = np.abs(Xf)        # magnitude |X(f)|
    argXf = np.angle(Xf)      # phase arg[X(f)]
    # ***** Plot magnitude/phase *****
    f1 = plt.figure()
    af11 = f1.add_subplot(211)
    af11.plot(ff, absXf, '-b')  # plot magnitude (linear)
    strt = 'FT Approximation, $F_s$={} Hz'.format(Fs)
    strt = strt + ', $N$='.format(N)
    strt = strt + ', $\Delta_f$={:3.2f} Hz'.format(Df)
    af11.set_title(strt)
    af11.set_ylabel('$|X(f)|$')
    af11.grid()
    af12 = f1.add_subplot(212)
    af12.plot(ff, 180/np.pi*argXf, '-b')  # plot phase in degrees
    af12.set_ylabel('$\\angle X(f)$ [deg]')
    af12.set_xlabel('$f$ [Hz]')
    af12.grid()
    plt.tight_layout()
    plt.show()    
    
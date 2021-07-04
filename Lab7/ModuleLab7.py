import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from Resources import comsig
import ModuleLab1


def e3c(fc_list=[2000, 6000, 10000, 14000, 18000]):
    Fs, rt = ModuleLab1.wavread("Files/amsig720.wav")
    sig = comsig.sigWave(rt, Fs)
    for i, fc in enumerate(fc_list):
        rcv = amrcvr(sig, 'coh', [fc, 0], [3000, 15, 0.05], [], dcblock=False)
        xf, _ = trapfilt_cc(rcv, [4000, 2000], 10, 0.5)
        ModuleLab1.wavwrite(f"e3c_module-{i + 1}.wav", Fs, 1 * xf.signal().real)
    print("Arquivos gravados")
    return


def qamrcvr(sig_rt, fcparms, fmparms=[]):
    """
    Quadrature Amplitude Modulation (QAM) Receiver with real-valued input and complex-valued output signals
    >>>>> sig_mthat = qamrcvr(sig_rt, fcparms, fmparms) <<<<<
    where   sig_mthat: waveform from class sigWave
            sig_mthat.signal(): complex-valued demodulated message signal
            sig_mthat.timeAxis(): time axis for mhat(t) sig_rt: waveform from class sigWave
            sig_rt.signal(): received QAM signal (real-valued)
            sig_rt.timeAxis(): time axis for r(t)
            fcparms = [fc, thetaci, thetacq]
            fc: carrier frequency
            thetaci: in-phase (cos) carrier phase in deg
            thetacq: quadrature (sin) carrier phase in deg
            fmparms = [fm, km, alfam] for LPF at fm parameters no LPF at fm if fmparms = []
            fm: highest message frequency (-6 dB)
            km: h(t) is truncated to |t| <= km/(2*fm)
            alfam: frequency rolloff parameter, linear rolloff over range (1-alfam)*fm <= |f| <= (1+alfam)*fm
    """
    # input is real valued, output is complex
    Fs, t0 = sig_rt.get_Fs(), sig_rt.get_t0()
    def filt(s):
        s = comsig.sigWave(s, Fs, t0)
        if len(fmparms) == 3:
            mx, _ = trapfilt(s, fmparms[0], fmparms[1], fmparms[2])
        elif fmparms == []:
            mx = s
        else:
            raise AssertionError("Error at input")
        return mx.signal()
    
    fc, thetaci, thetacq = fcparms

    xi = sig_rt.signal().copy()
    tth = sig_rt.timeAxis().copy()
    vi = xi * np.cos(2 * np.pi * fc * tth + thetaci * np.pi / 180)
    mi = filt(vi)

    xq = sig_rt.signal().copy()
    vq = - xq * np.sin(2 * np.pi * fc * tth + thetacq * np.pi / 180)
    mq = filt(vq)

    y = np.zeros(shape=xi.shape, dtype=np.complex)
    y.real = mi
    y.imag = mq
    return comsig.sigWave(y, Fs, t0)


def qamxmtr(sig_mt, fcparms, fmparms=[]):
    """
    Quadrature Amplitude Modulation (QAM) Transmitter with complex-valued input and real-valued output signals
    >>>>> sig_xt = qamxmtr(sig_mt, fcparms, fmparms) <<<<<
    where   sig_xt: waveform from class sigWave
            sig_xt.signal(): real-valued QAM signal
            sig_xt.timeAxis(): time axis for x(t)
            sig_mt.signal(): complex-valued (wideband) message signal
            sig_mt.timeAxis(): time axis for m(t)
            fcparms = [fc, thetaci, thetacq]
            fc: carrier frequency
            thetaci: in-phase (cos) carrier phase in deg
            thetacq: quadrature (sin) carrier phase in deg
            fmparms = [fm, km, alfam] for LPF at fm parameters no LPF/BPF at fm if fmparms = []
            fm: highest message frequency (-6dB)
            km: h(t) is truncated to |t| <= km/(2*fm)
            alfam: frequency rolloff parameter, linear rolloff over range (1-alfam)*fm <= |f| <= (1+alfam)*fm
    """
    if len(fmparms) == 3:
        xl, _ = trapfilt_cc(sig_mt, fmparms[0], fmparms[1], fmparms[2])
    elif fmparms == []:
        xl = sig_mt
    else:
        raise AssertionError("Error at input")
    fc, thetaci, thetacq = fcparms
    Ac = 1
    tth = xl.timeAxis()
    yi = xl.signal().real * Ac * np.cos(2 * np.pi * fc * tth + thetaci * np.pi / 180)
    yq = xl.signal().imag * Ac * np.cos(2 * np.pi * fc * tth + np.pi / 2 + thetacq * np.pi / 180)
    return comsig.sigWave(yi + yq, xl.get_Fs(), xl.get_t0())



def trapfilt_cc(sig_xt, fparms, k, alfa):
    """
    Delay compensated FIR LPF/BPF filter with trapezoidal frequency response,
    complex-valued input/output and complex-valued filter coefficients.
    >>>>> sig_yt, n = trapfilt_cc(sig_xt, fparms, k, alfa) <<<<<
    where   sig_yt: waveform from class sigWave
            sig_yt.signal(): complex filter output y(t), samp rate Fs
            n: filter order
            sig_xt: waveform from class sigWave
            sig_xt.signal(): complex filter input x(t), samp rate Fs
            sig_xt.get_Fs(): sampling rate for x(t), y(t)
            fparms = fL for LPF
            fL: LPF cutoff frequency (-6 dB) in Hz
            fparms = [fBW, fBc] for BPF
            fBW: BPF -6dB bandwidth in Hz
            fBc: BPF center frequency (pos/neg) in Hz
            k: h(t) is truncated to |t| <= k/(2*fL) for LPF |t| <= k/fBW for BPF
            alfa: frequency rolloff parameter,
             linear rolloff over range (1-alfa)*fL <= |f| <= (1+alfa)*fL for LPF
             (1-alfa)*fBW/2 <= |f| <= (1+alfa)*fBW/2 for BPF
    """
    lpf = True
    if isinstance(fparms, int):
        # caso for LPF
        fL = fparms
    else:
        # caso for BPF
        fBw, fc = fparms
        fL = fBw / 2
        lpf = False
    

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
    if not lpf:
        ht = 2 * ht * np.exp(1j * 2 * np.pi * fc * tth)

    ###
    yt = lfilter(ht, 1, np.hstack((xt, np.zeros(ixk))))/float(Fs) # Compute filter output y(t)
    yt = yt[ixk:] # Filter delay compensation

    return comsig.sigWave(yt, Fs, sig_xt.get_t0()), n # Return y(t) and filter order



def trapfilt(sig_xt, fparms, k, alfa):
    """
    Delay compensated FIR LPF/BPF filter with trapezoidal frequency response.
    >>>>> sig_yt, n = trapfilt(sig_xt, fparms, k, alfa) <<<<<
    where   sig_yt: waveform from class sigWave
            sig_yt.signal(): filter output y(t), samp rate Fs
            n: filter order
            sig_xt: waveform from class sigWave
            sig_xt.signal(): filter input x(t), samp rate Fs
            sig_xt.get_Fs(): sampling rate for x(t), y(t)
            fparms = fL for LPF
            fL: LPF cutoff frequency (-6 dB) in Hz
            fparms = [fBW, fc] for BPF
            fBW: BPF -6dB bandwidth in Hz
            fc: BPF center frequency in Hz
            k: h(t) is truncated to
                |t| <= k/(2*fL) for LPF
                |t| <= k/fBW for BPF
            alfa: frequency rolloff parameter, linear rolloff over range
                (1-alfa)fL <= |f| <= (1+alfa)fL for LPF
                (1-alfa)fBW/2 <= |f| <= (1+alfa)fBW/2 for BPF
    """
    lpf = True
    if isinstance(fparms, int):
        # caso for LPF
        fL = fparms
    else:
        # caso for BPF
        fBw, fc = fparms
        fL = fBw / 2
        lpf = False
    

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
    if not lpf:
        ht *= 2 * np.cos(2 * np.pi * fc * tth)

    ###
    yt = lfilter(ht, 1, np.hstack((xt, np.zeros(ixk))))/float(Fs) # Compute filter output y(t)
    yt = yt[ixk:] # Filter delay compensation

    return comsig.sigWave(yt, Fs, sig_xt.get_t0()), n # Return y(t) and filter order


def amrcvr(sig_rt, rtype, fcparms, fmparms=[], fBparms=[], dcblock=False):
    """
    Amplitude Modulation Receiver for coherent (’coh’) reception, or absolute value (’abs’),
    or squaring (’sqr’) demodulation, or I-Q envelope (’iqabs’) detection, or I-Q phase (’iqangle’)
    detection.
    >>>>> sig_mthat = amrcvr(sig_rt, rtype, fcparms, fmparms, fBparms, dcblock) <<<<<
    where   sig_mthat: waveform from class sigWave
            sig_mthat.signal(): demodulated message signal
            sig_mthat.timeAxis(): time axis mhat(t)
            sig_rt: waveform from class sigWave
            sig_rt.signal(): received AM signal
            sig_rt.timeAxis(): time axis for r(t)
            rtype: Receiver type from list ’abs’ (absolute value envelope detector),
            ’coh’ (coherent), ’iqangle’ (I-Q rcvr, angle or phase),
            ’iqabs’ (I-Q rcvr, absolute value or envelope), ’sqr’ (squaring envelope detector)
            fcparms = [fc, thetac]
            fc: carrier frequency
            thetac: carrier phase in deg (0: cos, -90: sin)
            fmparms = [fm, km, alfam] LPF at fm parameters no LPF at fm if fmparms = []
            fm: highest message frequency
            km: LPF h(t) truncation to |t| <= km/(2*fm)
            alfam: LPF at fm frequency rolloff parameter, linear rolloff over range 2*alfam*fm
            fBparms = [fBW, fcB, kB, alfaB] BPF at fcB parameters no BPF if fBparms = []
            fBW: -6 dB BW of BPF
            fcB: center freq of BPF
            kB: BPF h(t) truncation to |t| <= kB/fBW
            alfaB: BPF frequency rolloff parameter, linear rolloff over range alfaB*fBW
            dcblock: remove dc component from mthat if true
    """
    if rtype not in ['abs', 'coh', 'iqangle', 'iqabs', 'sqr']:
        raise AssertionError("rtype not from list")

    if fBparms == []:
        ss = sig_rt
    else:
        ss = trapfilt(sig_rt, [fBparms[0], fBparms[1]], fBparms[2], fBparms[3])

    tt = ss.timeAxis()
    rt = ss.signal()
    Fs = ss.get_Fs()
    t0 = ss.get_t0()

    if len(fcparms) == 3:
        fc, thetac, alfa = fcparms
    else:
        fc, thetac = fcparms

    thetac_rad = thetac * np.pi / 180

    def fmfilter(x):
        if fmparms == []:
            pass
        else:
            x, _ = trapfilt(x, fmparms[0], fmparms[1], fmparms[2])
        return x


    if rtype == 'coh':
        y = 2 * np.cos(2 * np.pi * fc * tt + thetac_rad) * rt
        sd = comsig.sigWave(y, Fs, t0)
        sd = fmfilter(sd)
    elif rtype == 'abs':
        y = abs(rt)
        sd = comsig.sigWave(y, Fs, t0)
        sd = fmfilter(sd)
        dcblock = True
    elif rtype == 'sqr':
        y = rt ** 2
        sd = comsig.sigWave(y, Fs, t0)
        sd = fmfilter(sd)
        y = np.sqrt(abs(sd.signal()))
        sd = comsig.sigWave(y, Fs, t0)
        dcblock = True
    elif rtype == 'iqangle':
        vi = 2 * np.cos(2 * np.pi * fc * tt) * rt
        svi = comsig.sigWave(vi, Fs, t0)
        svi = fmfilter(svi)
        vq = - 2 * np.sin(2 * np.pi * fc * tt) * rt
        svq = comsig.sigWave(vq, Fs, t0)
        svq = fmfilter(svq)
        y = np.arctan(svq.signal() / svi.signal())
        sd = comsig.sigWave(y, Fs, t0)
    elif rtype == 'iqabs':
        vi = 2 * np.cos(2 * np.pi * fc * tt) * rt
        svi = comsig.sigWave(vi, Fs, t0)
        svi = fmfilter(svi)
        vq = - 2 * np.sin(2 * np.pi * fc * tt) * rt
        svq = comsig.sigWave(vq, Fs, t0)
        svq = fmfilter(svq)
        y = (svi.signal() ** 2 + svq.signal() ** 2) ** 0.5
        sd = comsig.sigWave(y, Fs, t0)

    if dcblock:
        _ = sd.signal()
        sig_mthat = comsig.sigWave(_ - np.mean(_), Fs, t0)
    else:
        sig_mthat = sd

    return sig_mthat


def amxmtr(sig_mt, xtype, fcparms, fmparms=[], fBparms=[]):
    """
    Amplitude Modulation Transmitter for suppressed (’sc’) and transmitted (’tc’) carrier AM signals
    >>>>> sig_xt = amxmtr(sig_mt, xtype, fcparms, fmparms, fBparms) <<<<<
    where       sig_xt: waveform from class sigWave
                sig_xt.signal(): transmitted AM signal
                sig_xt.timeAxis(): time axis for x(t)
                sig_mt: waveform from class sigWave
                sig_mt.signal(): modulating (wideband) message signal
                sig_mt.timeAxis(): time axis for m(t)
                xtype: ’sc’ or ’tc’ (suppressed or transmitted carrier)
                fcparms = [fc, thetac] for ’sc’
                fcparms = [fc, thetac, alfa] for ’tc’
                fc: carrier frequency
                thetac: carrier phase in deg (0: cos, -90: sin)
                alfa: modulation index 0 <= alfa <= 1
                fmparms = [fm, km, alfam] LPF at fm parameters no LPF at fm if fmparms = []
                fm: highest message frequency
                km: LPF h(t) truncation to |t| <= km/(2*fm)
                alfam: LPF at fm frequency rolloff parameter, linear rolloff over range 2*alfam*fm
                fBparms = [fBW, fcB, kB, alfaB] BPF at fcB parameters no BPF if fBparms = []
                fBW: -6 dB BW of BPF
                fcB: center freq of BPF
                kB: BPF h(t) truncation to |t| <= kB/fBW
                alfaB: BPF frequency rolloff parameter, linear rolloff over range alfaB*fBW
    """

    Ac = 1
    tt = sig_mt.timeAxis()

    if fmparms == []:
        mt = sig_mt
    else:
        mt, _ = trapfilt(sig_mt, fmparms[0], fmparms[1], fmparms[2])

    if xtype == "sc":
        fc, thetac = fcparms
        thetac_rad = thetac * np.pi / 180
        y = Ac * mt.signal() * np.cos(2 * np.pi * fc * tt + thetac_rad)
    elif xtype == "tc":
        fc, thetac, alfa = fcparms
        thetac_rad = thetac * np.pi / 180
        y = Ac * (1 + alfa * mt.signal()) * np.cos(2 * np.pi * fc * tt + thetac_rad)
    else:
        raise NotImplementedError("xtype tem que ser SC ou TC")
    x = comsig.sigWave(y, sig_mt.get_Fs(), t0 = mt.get_t0())

    if fBparms == []:
        xb = x
    else:
        xb = trapfilt(x, [fBparms[0], fBparms[1]], fBparms[2], fBparms[3])

    return xb
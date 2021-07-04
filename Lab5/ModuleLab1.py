import numpy as np
import scipy.io.wavfile as sio_wav
from ast import literal_eval


def sine100(Fs):
    """ Asks for sampling frequency Fs and then returns tt, st, Fs of 5 periods of a 100 Hz sinewave with sampling rate Fs """
    # Fs = literal_eval(input('Enter sampling rate Fs in Hz: '))
    f0 = 100 # Frequency of sine
    tlen = 5e-2 # Signal duration in sec
    tt = np.arange(round(tlen*Fs))/float(Fs) # Time axis
    st = np.sin(2*np.pi*f0*tt) # Sinewave, frequency f0
    return tt, st


def wavread(fname):
    """
    Read N-channel 16-bit PCM wav-file
    >>>>> Fs, rt = wavread(fname) <<<<<
    where fname : file name of wav-file
          Fs    : sample rate of wav-file
          rt    : data read from wav-file, N channels, Nsamples data samples per channel, (Nsamples x N) numpy array of type np.float32, data samples normalized to range -1 ... +1
    """ 
    Fs, rt = sio_wav.read(fname)
    if rt.dtype is np.dtype(np.int16):
        rt = rt / float(2 ** 15 - 1)
        rt = np.array(rt, np.float32)
    else:
        print("Not a 16-bit PCM wav-file")
        rt = []
    return Fs, rt


def wavwrite(fname, Fs, xt):
    """
    Write N-channel 16-bit PCM wav-file
    >>>>> wavwrite(fname, Fs, xt) <<<<<
    where fname : file name of wav-file
          Fs    : sample rate of wav-file
          xt    : data to be written to wav-file (Nsamples x N) numpy array of floats normalized to range -1...+1 N channels, Nsamples data samples per channel
    """
    # convert to np.int16 data type
    xt = np.array((2 ** 15 - 1) * xt, np.int16)
    sio_wav.write(fname, Fs, xt)
    return


def sinc_ipol(Fs, fL, k):
    """
    sinc interpolation function, cutoff frequency fL,
    taillength k/(2*fL) seconds
    >>>>> tth, ht = sinc_ipol(Fs, fL, k) <<<<<
    where Fs    sampling rate
          fL    cutoff frequency in Hz
          k     taillength in terms of zero crossings of sinc
          tth   time axis for h(t)
          ht    truncated sinc pulse h(t)
    """
    # create time axis
    ixk = int(np.round(Fs*k/float(2*fL)))
    tth = np.arange(-ixk, ixk+1)/float(Fs)
    # sinc pulse
    ht = 2*fL*np.sinc(2*fL*tth)
    return tth, ht


def ftpam01(txt, Fb, Fs):
    """
    Function that accepts an ASCII text string as input and produces a corresponding binary unipolar flat-top PAM signal s(t) with bit rate Fb and sampling rate Fs.
    >>>>> tt, st = ftpam01(txt, Fb, Fs) <<<<<
    where tt: time axis for PAM signal s(t) (starting at -Tb/2)
          st: flat-top PAM signal s(t) s(t) = dn, (n-1/2)*Tb <= t < (n+1/2)*Tb
          txt: ASCII text string, 8 bits/symbol, converted to LSB-first bitstream dn
          Fb: bit rate of dn, Tb=1/Fb
          Fs: sampling rate of s(t)
     """
    bits = 8 # Bits per ASCII symbol # >> Convert txt to bitstream dn here, LSB-first <<

    # using LSB-first (bits > 0)
    dn = asc2bin(txt, bits = bits)

    
    N = len(dn)
    Tb = 1 / Fb
    ixL = np.round(-0.5 * Fs * Tb)
    ixR = np.round((N - 0.5) * Fs * Tb)
    tt = np.arange(ixL, ixR) / Fs

    diff = np.diff(dn, prepend = 0) * Fs
    st = np.zeros(shape = tt.shape, dtype = np.float32)

    # decidindo onde botar os deltas, ver definição da documentação (intervalo fechado do lado direito, aberto no esquerdo)
    last_ni = -1
    idx = 0
    for i in range(st.size):
        # primeiro idx a receber o ni é delta_i = piso(t/Tb + 1/2) pois nesse idx t >= (n - 1/2)Tb
        ni = int(np.floor(tt[i] / Tb + 1 / 2))
        if ni != last_ni:
            # print(f"pick i: {i}, idx: {idx}, tti: {tt[i]}")
            last_ni = ni
            st[i] = diff[idx]
            idx += 1
    assert(idx == diff.size)
    st = np.cumsum(st) / Fs
    return tt, st


def ftpam_bitstring(dn, Fb, Fs):
    """
    Tx data
    """

    N = len(dn)
    Tb = 1 / Fb
    ixL = np.round(-0.5 * Fs * Tb)
    ixR = np.round((N - 0.5) * Fs * Tb)
    tt = np.arange(ixL, ixR) / Fs

    diff = np.diff(dn, prepend = 0) * Fs
    st = np.zeros(shape = tt.shape, dtype = np.float32)

    # decidindo onde botar os deltas, ver definição da documentação (intervalo fechado do lado direito, aberto no esquerdo)
    last_ni = -1
    idx = 0
    for i in range(st.size):
        ni = int(np.floor(tt[i] / Tb + 1 / 2))
        if ni != last_ni:
            last_ni = ni
            st[i] = diff[idx]
            idx += 1
    assert(idx == diff.size)
    st = np.cumsum(st) / Fs
    return tt, st


def asc2bin(txt, bits=8):
    """
    ASCII message to serial binary conversion
    >>>>> dn = asc2bin(txt, bits) <<<<<
    where txt       :ASCII message (text string)
          abs(bits) :bits per character, default: 8
          bits > 0  :LSB first parallel to serial conv
          bits < 0  :MSB first parallel to serial conv
          dn        :binary output DT sequence
    """
    txtnum = np.array([ord(c) for c in txt], np.int16)
    
    if bits > 0:
        p2 = np.array(np.power(2.0, -np.arange(bits)), np.float32)
    else:
        p2 = np.array(np.power(2.0, np.arange(bits + 1, 1)), np.float32)
    
    # 2-dim array of bits, one row per character in txt
    B = np.array(np.mod(np.floor(np.outer(txtnum, p2)), 2), np.int8)
    return np.reshape(B, -1)

def bin2asc(dn, bits=8, flg=1):
    """
    Serial binary to ASCII text conversion
    >>>>> txt = bin2asc(dn, bits, flg) <<<<<
    where dn    : binary input sequence
          abs(bits): bits per char, default=8
          bits > 0: LSB first parallel to serial
          bits < 0: MSB first parallel to serial
          flg != 0: limit range to [0...127]
          txt     : output text string
    """
    if flg:
        raise NotImplementedError("Comportamento indefinido no momento")
    
    abits = np.abs(bits)
    p2 = np.array(np.power(2, np.arange(abits)), dtype = np.int16)
    if bits < 0:
        p2 = np.flip(p2)
    
    N = len(dn)
    assert(N % abits == 0)
    cnt = N // abits
    txt = ""
    for w in range(cnt):
        inc = p2.dot(dn[w * abits : (w + 1) * abits])
        txt += chr(inc)
    return txt


def ftpam_rcvr01(tt, rt, Fbparms):
    """
    Binary unipolar Flat-top PAM sampling receiver for input signal r(t) with bitrate Fb and sampling rate Fs. The PAM signal rt with associated time axis tt (starting at -0.5*Tb) is sampled at times t = n*Tb + dly*Tb, where 0<=dly<1 is a delay parameter, to obtain a DT sequence rn.
    >>>>> rn, ixn = ftpam_rcvr01(tt, rt, Fbparms) <<<<<
    where rn    : sampled DT sequence
          ixn   : sampling time indexes
          tt    : time axis for r(t)
          rt    : received (noisy) PAM signal r(t)
          Fbparms: = [Fb, dly]
          Fb    : Bit rate of PAM signal, Tb=1/Fb
          dly   : sampling delay for r(t) -> r_n as a fraction of T
    """
    if type(Fbparms) == int:
        Fb, dly = Fbparms, 0
    else:
        Fb, dly = Fbparms[0], 0
        if len(Fbparms) > 1:
            dly = Fbparms[1]
    Fs = (len(tt) - 1) / (tt[-1] - tt[0])

    Tb = 1 / Fb
    timespan = (tt[-1] - tt[0])

    last_ni = -1
    idx = 0
    qtd_bits = int(np.ceil(timespan * Fb))

    ni = np.floor((tt - dly * Tb) / Tb).astype(int)
    nid = np.diff(ni, prepend = ni[0])
    ixn = np.argwhere(nid).ravel()
    rn = rt[ixn]
    assert(len(ixn) == qtd_bits)

    # equivalente a
    # ixn = np.empty(shape=(qtd_bits,), dtype=np.int64)
    # rn = np.empty(shape=ixn.shape, dtype=np.float64)
    # for i in range(rt.size):
    #     ni = int(np.floor((tt[i] - dly * Tb) / Tb))
    #     if ni != last_ni:
    #         last_ni = ni
    #         print(f"pick i: {i}, idx: {idx}, tti: {tt[i]}")
    #         ixn[idx] = i
    #         rn[idx] = rt[i]
    #         idx += 1
    # print(idx, qtd_bits)
    # assert(idx == qtd_bits)
    return rn, ixn



def ftpam_rcvr_th(tt, rt, Fbparms, Th = 0.5):
    """
    Versão com uso de threshold
    """

    rt = np.where(rt > Th, 1, 0)
    return ftpam_rcvr01(tt, rt, Fbparms)



def wav2txt(filename, Fb):
    Fs, rt = wavread(filename)
    ttr = np.arange(rt.size) / Fs - 1 / (2 * Fb)

    Fbparms = [Fb, 0]
    rn, ixn = ftpam_rcvr01(ttr, rt, Fbparms)
    dh = np.round(rn).astype(np.int8)
    st = bin2asc(np.round(rn).astype(int), flg = 0)
    return st



def wav2txt_Th(filename, Fb, Th = 0.5):
    Fs, rt = wavread(filename)
    ttr = np.arange(rt.size) / Fs - 1 / (2 * Fb)

    Fbparms = [Fb, 0]
    rn, ixn = ftpam_rcvr_th(ttr, rt, Fbparms, Th = Th)
    dh = np.round(rn).astype(np.int8)
    st = bin2asc(np.round(rn).astype(int), flg = 0)
    return st


def check_sensible_string(st):
    valid = True
    for c in st:
        co = ord(c)
        valid &= (co >= ord(' ') and co <= ord('z'))
        if not valid:
            return False
    return valid



def mt2pcm(mt, bits=8):
    """
    Message signal mt(t) to binary PCM conversion
    >>>>> dn, dc = mt2pcm(mt, bits) <<<<<
    where mt    : normalized (A = 1) "analog" message signal
          bits  : number of bits used per sample
          dn    : binary output sequence in sign-magnitude form, MSB (sign) first
          dc    : discretized version of mt
    """
    assert(bits > 0)
    N = len(mt)
    nN = N * bits
    dn = np.zeros(shape = (nN,), dtype=np.uint8)
    F = np.power(2, bits - 1)
    mxvalue = F - 1
    offset = 1 / (2 * F)
    disc = np.zeros(shape = (N, ), dtype=np.float32)

    for i in range(N):
        sample = mt[i]
        idx = i * bits
        disc[i] = sample
        signed = False
        if sample < 0:
            dn[idx] = 1
            sample = -sample
            signed = True
        sample *= F
        sample = int(np.floor(sample))
        sample = min(sample, mxvalue)
        disc[i] = sample / F
        disc[i] += offset
        if signed:
            disc[i] = -disc[i]
        bs = format(sample, f'0{bits - 1}b')
        for j, c in enumerate(bs):
            if c == '1':
                dn[idx + j + 1] = 1
    return dn, disc



def pcm2mt(dn, bits = 8):
    """
    Binary PCM to message signal m(t) conversion
    >>>>> mt = pcm2mt(dn, bits) <<<<<
    where dn    : binary output sequence in sign-magnitude form, MSB (sign) first
          bits  : number of bits used per sample
          mt    : normalized (A = 1) "analog" message signal
    """
    assert(bits > 0)
    nN = len(dn)
    # assert(nN % bits == 0)
    N = nN // bits

    F = np.power(2, bits - 1)
    offset = 1 / (2 * F)
    mt = np.zeros(shape = (N, ), dtype=np.float32)

    p2 = np.array(np.power(2, np.arange(bits - 1)), dtype = np.float32)
    # MSB
    p2 = np.flip(p2)

    for i in range(N):
        idx = bits * i
        signed = (dn[idx] == 1)
        curr = dn[idx + 1: idx + 1 + bits - 1]
        sample = curr.dot(p2)
        sample /= F
        sample += offset
        mt[i] = sample

        if signed:
            mt[i] = -mt[i]
    return mt

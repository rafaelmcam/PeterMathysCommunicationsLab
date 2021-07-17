# this module will be imported in the into your flowgraph

import numpy as np

class sigSequ:
    """ Class for 'sequence' (DT) signals """
    type = 'sequence'
    def __init__(self, sig, FB=100, n0=0):
        """
        sig: real- or complex-valued sequence values
        FB:  symbol (or Baud) rate (default 100 Baud)
        n0:  start index of sequence (default 0)
        """
        self._sig = np.asanyarray(sig)
        self._FB = FB
        self._n0 = n0
        
    # Properties
    def __len__(self):
        return len(self._sig)
    def __str__(self):         # String representation of object
        return 'FB={}, n0={}, Nsamp={}'.format(self._FB,self._n0,self._sig.size)
    __repr__ = __str__
    def get_size(self):
        return self._sig.size
    def get_shape(self):
        return self._sig.shape
    def get_FB(self):
        return self._FB
    def get_n0(self):
        return self._n0
    
    # Methods
    def indexAxis(self):
        return self._n0 + np.arange(len(self._sig))
    def signal(self):
        return self._sig
    def copy(self):
        return np.copy(self)
    def scale_and_offset(self, a, b=0):
        """ x[n]_out = a*x[n]_in + b """
        return sigSequ(a*self._sig + b, self._FB, self._n0)


class sigWave:
    """ Class for 'waveform' (pseudo-CT) signals """
    type = 'waveform'
    def __init__(self, sig, Fs=8000, t0=0):
        """
        sig:  real or complex-valued waveform samples
        Fs:   sampling rate (default 8000 samples/sec)
        t0:   start time of waveform in seconds (default 0)
        """
        self._sig = np.asanyarray(sig)
        self._Fs = Fs
        self._t0 = t0
        self._shape = np.shape(self._sig)
        if len(self._shape) > 1:
        	   self._Nsamp = len(self._sig[0])
        else:
        	   self._Nsamp = len(self._sig)
        self._tlen = self._Nsamp/float(self._Fs)
        self._tend = self._t0 + (self._Nsamp-1)/float(self._Fs)

    # Properties
    def __len__(self):
        return self._Nsamp    # Returns length in samples
    def __str__(self):        # String representation of object
        return 'Fs={}, t0={}, tlen={}'.format(self._Fs,self._t0,self._tlen)
    __repr__ = __str__
    def get_shape(self):
    	  return self._shape    # Returns shape of signal array
    def get_Fs(self):
    	  return self._Fs       # Returns sampling rate
    def get_t0(self):
    	  return self._t0       # Returns start time
    def get_tlen(self):
    	  return self._tlen     # Returns length in seconds
    def get_avgpwr(self):     # Returns average power
    	  return np.mean(np.power(np.abs(self._sig),2.0))
    def get_tend(self):
    	  return self._tend     # Returns end time
    def set_t0(self, t0):
    	  self._t0 = t0         # Set new start time
    	  self._tend = self._t0 + (self._Nsamp-1)/float(self._Fs)	  

    # Methods        
    def timeAxis(self):       # Generate time axis
        return self._t0 + np.arange(self._Nsamp)/float(self._Fs) 
    def signal(self):         # Return the waveform
        return self._sig
    def copy(self):           # Make a copy of a sigWave object
        return np.copy(self)
    def normalized(self):     # Normalize the signal to -1,+1 range
        new_sig = 1.0/np.max(abs(self._sig))*self._sig
        return sigWave(new_sig, self._Fs, selt._t0)
    def scale(self, factor):  # Make a scaled copy of a sigWave object
        return sigWave(factor*self._sig, self._Fs, self._t0)
    def pwrx(self, x):        # Raise the signal to power x
        return sigWave(np.power(self._sig, x), self._Fs, self._t0)
    def apwrx(self, x):       # Raise absolute value of signal to power x
        return sigWave(np.power(np.abs(self._sig), x), self._Fs, self._t0)
              
        
         

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
        if alpha == 0:
            alpha += 1e-5
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


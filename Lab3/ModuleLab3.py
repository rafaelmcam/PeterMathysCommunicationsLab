import numpy as np

def generate_signal_E3B(Fs, f1, duty_cycle):
    tt = np.arange(int(np.round(Fs / f1))) / Fs
    T = 1 / f1
    th = T * duty_cycle / 100
    st = np.zeros(shape=tt.shape)
    st = np.where(tt <= th, 1, 0)
    return st

def generate_signal_E3C(Fs, f1):
    size = int(np.round(Fs / f1))
    st = np.empty(shape=(size,))
    oq = size // 4
    sz1 = oq
    sz2 = size//2 - sz1
    sz3 = st[:-size//4].size - sz1 - sz2
    sz4 = size - sz1 - sz2 - sz3
    st[:size//4] = np.linspace(1, 0.5, sz1, endpoint = False)
    st[size//4:size//2] = np.linspace(-0.5, -1, sz2, endpoint=False)
    st[size//2:-size//4] = np.linspace(-1, -0.5, sz3, endpoint = False)
    st[-size//4:] = np.linspace(0.5, 1, sz4, endpoint=False)
    return st

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
    else:
        raise NotImplementedError("p(t) not implemented")
    return pt

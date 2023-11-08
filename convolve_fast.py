import scipy
import numpy as np

def convolve_fast(y, time, fs):
    print('Convolving window of length: %s ms.' % time)
    samples = int((time/(10**3)) * fs)
    weights = (1/samples) * np.ones(samples)
    smooth = scipy.signal.fftconvolve(y,weights,'same')
    return smooth
import scipy
import numpy as np
from pydub import AudioSegment


def convolve_fast(audio_path, time):
    signal = AudioSegment.from_file(file = audio_path, format = "flac")
    y = np.array(signal.get_array_of_samples())
    y_abs = abs(y)
    fs = signal.frame_rate

    print(f"Convolving signal with window of length: {time} ms.")
    samples = int((time/(10**3)) * fs) # Time must be in ms
    weights = (1/samples) * np.ones(samples)
    smooth = scipy.signal.fftconvolve(y_abs,weights,'same')
    
    return smooth

'''
def convolve_fast(y, time, fs):
    print('Convolving window of length: %s ms.' % time)
    samples = int((time/(10**3)) * fs)
    weights = (1/samples) * np.ones(samples)
    smooth = scipy.signal.fftconvolve(y,weights,'same')
    return smooth
'''
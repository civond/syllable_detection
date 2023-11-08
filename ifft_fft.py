import numpy as np
from pydub import AudioSegment
import timeit
import scipy


# Moving Average Window Parameters
time_short = 50 # ms
time_long = 250 # ms

# Audio File Parameters
#audio_path = 'D:\\Dorian\\My_Scripts\\30Label_filtered.wav'
audio_path = 'C:\\Users\\doria\\OneDrive\\Desktop\\Storage\\Coding projects\\finch\\Audio_Filtered\\long.wav'
signal = AudioSegment.from_file(file = audio_path, 
                             format = "wav")
duration = len(signal)/1000 
y = np.array(signal.get_array_of_samples())
y_abs = abs(y)
fs = signal.frame_rate
dt = 1/fs
t = np.arange(0,duration,dt)
print(len(y))
def standard_conv():
    # Convolution, consider implmenting ifft-fft
    #print('Standard Convolving Short Window.')
    #short_samples = int((time_short/(10**3)) * fs)
    #short_weights = (1/short_samples) * np.ones(short_samples)
    #short_smooth = np.convolve(y_abs,short_weights,mode='same')

    print('Convolving Long Window.')
    long_samples = int((time_long/(10**3)) * fs)
    long_weights = (1/long_samples) * np.ones(long_samples)
    long_smooth = np.convolve(y_abs,long_weights,mode='same')

    print('Finished Convolving Smooth Filters.')


pad_length = 2**26
def ifft_conv():
    print('IFFT Convolving Long Window.')
    y_padded = np.pad(y_abs, (0, (pad_length) - len(y_abs)%(pad_length)), 'constant')

    long_samples = int((time_short/(10**3)) * fs)
    long_weights = (1/long_samples) * np.ones(long_samples)
    long_weights_padded = np.pad(long_weights, (0, (pad_length) - len(long_weights)%(pad_length)), 'constant')

    #long_weights = np.convolve(y_abs,long_weights,mode='same')
    #long_smooth = np.fft.ifft(np.fft.fft(long_weights_padded) * np.fft.fft(y_padded))
    long_smooth = scipy.signal.fftconvolve(y,long_weights,'same')
    print(len(long_smooth))
    print(len(y))
    #print(len(y_padded))
    #print(len(short_weights_padded))
    #print(len(D))
n = 3


#result = timeit.timeit(stmt='standard_conv()', globals=globals(), number=n)
#print(f"Execution time is {result / n} seconds")

result = timeit.timeit(stmt='ifft_conv()', globals=globals(), number=n)
print(f"Execution time is {result / n} seconds")
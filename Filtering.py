import scipy
#from scipy.io import wavfile
import numpy as np
import soundfile as sf
from pydub import AudioSegment
import matplotlib.pyplot as plt

# Get audio paramaters
audio_path = 'D:\\Dorian\\syllable_detection\\Audio\\long.flac'
#audio_path = 'D:\\Dorian\\ZebraFinch_data\\30cut\\01Label.wav'
file_name = audio_path.split('\\')[-1]
wav = AudioSegment.from_file(file = audio_path, 
                             format = "flac")
duration = len(wav)/1000 # Pydub does things in ms
print(len(wav))
print(duration)
y = np.array(wav.get_array_of_samples())
fs = wav.frame_rate
print(fs)
dt = 1/fs
t = np.arange(0,duration,dt)

# Filter parameters
cutoff_freq = 350 # Hz
minimum_attenuation = 30 # dB
order = 8
#[b, a] = scipy.signal.butter(8,cutoff_freq,fs=fs,btype="high")
[b, a] = scipy.signal.cheby2(order,
                             minimum_attenuation,
                             cutoff_freq,
                             fs=fs,
                             btype="high")

#[b,a] = scipy.signal.butter(order, [lowcut], fs=fs, btype='high')
#[b, a] = scipy.signal.cheby2(4,40,Wn,btype="high")
[w, h] = scipy.signal.freqz(b, a,fs=fs,worN=2000)
y_filtered = scipy.signal.filtfilt(b,a,y)

scaled = np.int16(y_filtered / np.max(np.abs(y_filtered)) * 32767)
#wavfile.write("test_later.flac", fs, scaled)
sf.write("test_later.flac",scaled, fs,format='flac')
#y_filtered.export(out_f="test.wav",format="wav")

# Plotting signals
plt.figure(1)
plt.title("%s Audio Waveform"% file_name)
plt.plot(t,y,
         linewidth='1', 
         color='g')
plt.plot(t,y_filtered,
         linewidth=0.5,
         linestyle='--',
         color='b')
plt.legend(['Original', 'Filtered'])
plt.grid(True)
plt.xlabel("Time (s)")
#plt.xlim(0,max(t))
#plt.xlim(23.5,26)
#plt.ylim(-0.5*10**9,0.5*10**9)
plt.ylabel("Amplitude")
plt.show()

# Frequency Response
plt.figure(2)
plt.plot(w,20 * np.log10(abs(h)), 
         linewidth=1,
         color='b')
#plt.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)], '--')
plt.plot([0, 0.5 * fs], [-minimum_attenuation, -minimum_attenuation], 
         '--', 
         linewidth=0.8,
         color='r')
plt.plot([cutoff_freq, cutoff_freq], [-60,0], 
         '--',
         linewidth=0.8,
         color='g')
plt.legend(['Magnitude Response','Minimum Attenuation','Cutoff Frequency'])
plt.title('HP Magnitude Response')
plt.xlabel('Hz')
plt.xlim(0,1000)
plt.ylabel('Magnitude (dB)')
plt.grid(True)
plt.show()

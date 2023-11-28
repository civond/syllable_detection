# Imports
import numpy as np
from pydub import AudioSegment
from scipy.io.wavfile import write
import matplotlib.pyplot as plt

# Custom scripts
from update_overlap import *
from remove_short_overlaps import *
from convolve_fast import *
from clump import *
from back_extension import *
from filter_overlap import *
from amplitude_power_filt import *

# Audio File Parameters
#audio_path = 'D:\\Dorian\\syllable_detection\\Audio_Filtered\\long2_filtered.wav'
#audio_path = 'D:\\Dorian\\syllable_detection\\Audio_Filtered\\2hr_filtered.flac'
#audio_path = 'D:\\Dorian\\syllable_detection\\Audio_Filtered\\longflac_filtered.flac'
audio_path = 'D:\\Dorian\\syllable_detection\\Audio_Filtered\\30Label_filtered.wav'

signal = AudioSegment.from_file(file = audio_path, format = "flac")
duration = len(signal)/(1000) 
y = np.array(signal.get_array_of_samples())
y_abs = abs(y)
fs = signal.frame_rate
dt = 1/fs
t = np.arange(0,duration,dt)

# Convolution
time_short = 50 # ms
time_long = 250 # ms
short_smooth = convolve_fast(y_abs,time_short,fs)
long_smooth = convolve_fast(y_abs,time_long,fs)

# Overlap
overlap_threshold = 30
min_time = 40 # ms
min_samples = (min_time/1000) * fs
time_threshold = .4 # seconds
threshold_samples = time_threshold * fs

overlap = filter_overlap(short_smooth,long_smooth,overlap_threshold)
print(f"Dropping overlaps under: {min_time} ms.")
noshort = remove_short_overlaps(overlap,min_samples)
test = np.array(update_overlap(y,noshort,threshold_samples))

# Filtering by amplitude and power spectrum
noise_threshold = 8000
target_frequency = 4000
power_threshold = 100
test = amplitude_power_filt(test,fs,noise_threshold,target_frequency,power_threshold)

# Back extension
back_time = 100 # ms
back = back_extension(test,y,back_time) # Refactor this pls.
cut = clump(back)

# Writing audio files
start_indices = np.where(~np.isnan(test) & ~np.roll(~np.isnan(test), 1))[0]
chunk_lengths = np.diff(np.append(start_indices, len(test)))
folder = "cut_audio/"
for index, region in enumerate(cut):
    cut_file_name = folder + audio_path.split('\\')[-1].split('.')[0] + "_" + str(start_indices[index]) + ".wav"
    print(f"Writing: {cut_file_name}")
    scaled = np.int16((region/np.max(np.abs(y))) * 32767) # scaling according to original file
    write(cut_file_name, fs, scaled)
    
    

print(f"after: {test}")

#plt.plot(y_abs, color='c')
#plt.plot(overlap,color='r')
#plt.plot(noshort,color='k')
#plt.show()

plt.figure(1)
plt.plot(t,y,color='b')
plt.plot(t,test,color='g')
plt.grid(True)
plt.title(audio_path.split('\\')[-1])
plt.ylabel('Amplitude')
plt.xlabel('Time (s)')
plt.xlim(0,t[-1])
plt.plot([0,2000], [8000, 8000], color='r', linestyle='--', linewidth=0.8)
plt.plot([0,2000], [6000, 6000], color='cyan', linestyle='--', linewidth=0.8)
plt.plot([0,2000], [-8000, -8000], color='r', linestyle='--', linewidth=0.8)
plt.plot([0,2000], [-6000, -6000], color='cyan', linestyle='--', linewidth=0.8)
plt.legend(['Original','Cut','Threshold','Typical g_max'])
plt.tight_layout()

plt.figure(2)
plt.plot(t,y,color='b')
plt.plot(t,back,color='r')
#plt.plot(t,test,color='g')
plt.grid(True)
plt.title(audio_path.split('\\')[-1])
plt.ylabel('Amplitude')
plt.xlabel('Time (s)')
#plt.xlim(25,30)
plt.xlim(0,t[-1])
plt.plot([0,2000], [8000, 8000], color='r', linestyle='--', linewidth=0.8)
plt.plot([0,2000], [6000, 6000], color='cyan', linestyle='--', linewidth=0.8)
plt.plot([0,2000], [-8000, -8000], color='r', linestyle='--', linewidth=0.8)
plt.plot([0,2000], [-6000, -6000], color='cyan', linestyle='--', linewidth=0.8)
plt.legend(['Original','Cut','Threshold','Typical g_max'])
plt.tight_layout()

helpme = np.empty(len(y)) # Preallocate zeros to temp
helpme[:] = np.nan
for i in range(len(short_smooth)):
    if short_smooth[i]-overlap_threshold > long_smooth[i]:
        helpme[i] = short_smooth[i]


plt.figure(3)
plt.title('Smoothing Filter Overlaps')
plt.plot(t, long_smooth,color='b')
plt.plot(t, short_smooth, color='g')
plt.plot(t, helpme, color='r')
plt.ylabel('Moving Average Magnitude')
plt.xlabel('Time (s)')
plt.xlim(25,30)
plt.legend([f"Long {time_long} ms", f"Short {time_short} ms", 'overlap'])
plt.grid(True)
#plt.show()



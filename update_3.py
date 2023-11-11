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

# Audio File Parameters
#audio_path = 'D:\\Dorian\\syllable_detection\\Audio_Filtered\\long2_filtered.wav'
#audio_path = 'D:\\Dorian\\syllable_detection\\30Label_Filtered.wav'
audio_path = 'D:\\Dorian\\syllable_detection\\Audio_Filtered\\longflac_filtered.flac'

#audio_path = 'D:\\Dorian\\syllable_detection\\30Label_filtered.wav'
signal = AudioSegment.from_file(file = audio_path, 
                             format = "flac")
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
print(f"Calculating the overlap with min threshold value: {overlap_threshold}")
overlap = np.empty(len(y)) # Preallocate zeros to temp
overlap[:] = np.nan
temp = short_smooth - long_smooth
for i in range(len(temp)):
    if temp[i] > overlap_threshold:
        overlap[i] = temp[i]

min_time = 40 # ms
min_samples = (min_time/1000) * fs


#plt.plot(y_abs, color='c')
#plt.plot(overlap,color='r')

print(f"Dropping overlaps under: {min_time} ms.")
print('# points before drop: ' + str(np.count_nonzero(~np.isnan(overlap))))
noshort = remove_short_overlaps(overlap,min_samples)
print('# points after drop: ' + str(np.count_nonzero(~np.isnan(noshort))))
#plt.plot(noshort,color='k')

time_threshold = .4 # seconds
threshold_samples = time_threshold * fs

test = np.array(update_overlap(y,noshort,threshold_samples))

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
#plt.show()

####################################
start_indices = np.where(~np.isnan(test) & ~np.roll(~np.isnan(test), 1))[0]

# Find the lengths of consecutive non-NaN chunks
chunk_lengths = np.diff(np.append(start_indices, len(test)))

# Print out each section of non-NaN values without trailing NaNs

print(f"before: {test}")
noise_threshold = 8000
target_frequency = 4000
power_threshold = 100
folder = "cut_audio/"

for start, length in zip(start_indices, chunk_lengths):
    section = test[start:start + length]
    section_without_nans = section[~np.isnan(section)]
    if not np.isnan(section[0]):
        #print(f"Section: {section_without_nans}")
        #print(len(section_without_nans))
        
        #if len(section_without_nans) <= 3:
        #    test[start:start + length] = np.nan
        
        max_region_value = np.max(np.abs(section_without_nans))
        if max_region_value > noise_threshold:
            print("Section exceeded amplitude threshold, dropping.")
            test[start:start + length] = np.nan
        
        #print(f"Performing Fourier transform on each section")
        temp_fft = np.fft.fft(section_without_nans)
        power_spectrum = np.abs(temp_fft) ** 2
        freq = np.fft.fftfreq(len(power_spectrum), 1 / fs)
        closest_index = np.argmin(np.abs(freq - target_frequency))
        power_at_target_frequency = 10 * np.log10(power_spectrum[closest_index])

        frequency_range = 10  # Adjust as needed
        indices_in_range = np.where((freq >= target_frequency - frequency_range) & (freq <= target_frequency + frequency_range))

        average_power_in_range = 10 * np.log10(np.mean(power_spectrum[indices_in_range]))
        
        if average_power_in_range > power_threshold:
            #cut_file_name = folder + audio_path.split('\\')[-1].split('.')[0] + "_" + str(index) + ".wav"
            #print(f"section_without_nans {index} met threshold requirements. \n Writing {cut_file_name}")
            #scaled = np.int16((section_without_nans/np.max(np.abs(y))) * 32767) # scaling according to original file
            #write(cut_file_name, fs, scaled)
            continue
        else: 
            #print(f"Power Spectrum of Region {index} did not meet threshold of {power_threshold} at ~{target_frequency} Hz... skipping." )
            #print('help')
            test[start:start + length] = np.nan
back_time = 100 # ms
print(f"Adding back extension: {back_time} ms.")
back = back_extension(test,y,back_time)
cut = clump(back)
for index, region in enumerate(cut):
    cut_file_name = folder + audio_path.split('\\')[-1].split('.')[0] + "_" + str(index) + ".wav"
    scaled = np.int16((region/np.max(np.abs(y))) * 32767) # scaling according to original file
    write(cut_file_name, fs, scaled)
    
    

print(f"after: {test}")
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
plt.show()



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

# Audio File Parameters
#audio_path = 'D:\\Dorian\\My_Scripts\\30Label_filtered.wav'
audio_path = 'D:\\Dorian\\syllable_detection\\Audio_Filtered\\long2_filtered.wav'
signal = AudioSegment.from_file(file = audio_path, 
                             format = "wav")
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

# Converting array to chunks
help_pls = clump(test)


# Writing Audio
total_threshold = 0.5 * fs #second * sample rate
noise_threshold = 8000
target_frequency = 4000
power_threshold = 100
folder = "cut_audio/"
print('Number of regions found: %s ' % len(help_pls))

for index, region in enumerate(help_pls):
    if len(region) < total_threshold:
        print(f"Region {index} did not meet the minimum length threshold. Skipping...")
        continue
    max_region_value = np.max(np.abs(region))
    if max_region_value > noise_threshold:
        print(f"Region {index} exceeded the noise threshold ({noise_threshold}). Skipping...")
        continue

    temp_fft = np.fft.fft(region)
    power_spectrum = np.abs(temp_fft) ** 2
    freq = np.fft.fftfreq(len(power_spectrum), 1 / fs)
    closest_index = np.argmin(np.abs(freq - target_frequency))
    power_at_target_frequency = 10 * np.log10(power_spectrum[closest_index])

    frequency_range = 10  # Adjust as needed
    indices_in_range = np.where((freq >= target_frequency - frequency_range) & (freq <= target_frequency + frequency_range))

    average_power_in_range = 10 * np.log10(np.mean(power_spectrum[indices_in_range]))
    
    if average_power_in_range > power_threshold:
                cut_file_name = folder + audio_path.split('\\')[-1].split('.')[0] + "_" + str(index) + ".wav"
                print(f"Region {index} met threshold requirements. \n Writing {cut_file_name}")
                scaled = np.int16((region/np.max(np.abs(y))) * 32767) # scaling according to original file
                write(cut_file_name, fs, scaled)
    else: 
        print(f"Power Spectrum of Region {index} did not meet threshold of {power_threshold} at ~{target_frequency} Hz... skipping." )
        continue
        
'''
for index, region in enumerate(help_pls):
    if len(region) < total_threshold:
        print('Region %s did not meet minimum length threshold. Skiping...' % index)
        pass
    else:
        if np.max(abs(region)) > noise_threshold:
            print('Region %s exceeded noise threshold (= %s). Skipping...' % (index, noise_threshold))
            pass
        else:
            temp_fft = np.fft.fft(region)
            power_spectrum = np.abs(temp_fft) ** 2
            freq = np.fft.fftfreq(len(power_spectrum), 1 / fs)
            closest_index = np.argmin(np.abs(freq - target_frequency))
            power_at_target_frequency = 10 * np.log10(power_spectrum[closest_index])
            frequency_range = 10  # Adjust as needed
            indices_in_range = np.where((freq >= target_frequency - frequency_range) & (freq <= target_frequency + frequency_range))

            # Calculate the average power within the specified frequency range
            average_power_in_range = 10 * np.log10(np.mean(power_spectrum[indices_in_range]))
            if average_power_in_range > power_threshold:
                cut_file_name = folder + audio_path.split('\\')[-1].split('.')[0] + "_" + str(index) + ".wav"
                print('Region %s met threshold requirements. \n Writing %s' % (index, cut_file_name))
                scaled = np.int16((region/np.max(np.abs(y))) * 32767) # scaling according to original file
                write(cut_file_name, fs, scaled)
            else: 
                print('Power Spectrum of Region %s did not meet threshold of %s at ~%s Hz... skipping.' %(index, target_frequency,power_threshold))
                pass
'''
print('Writing Long cut file: ')
test[np.isnan(test)] = 0
scaled = np.int16(test / np.max(np.abs(y)) * 32767)
write('long_cutttt.wav', fs, scaled)
'''
plt.figure(1)
plt.plot(y)
plt.plot(test)
plt.plot(overlap,color='k',linewidth=3)
plt.plot(noshort, color='c',linewidth=3)

plt.legend(['Original','Cut', 'Overlap_noshort','Overlap'])
plt.show()

#print(np.count_nonzero(overlap))
#print(np.count_nonzero(test))

#print(test)

#plt.plot(test)
#plt.show()



#plt.plot(noshort)
#plt.show()
'''
# Imports
import numpy as np
from pydub import AudioSegment
from scipy.io.wavfile import write
import matplotlib.pyplot as plt

# Custom scripts
from update_overlap import *
from remove_short_overlaps import *
from convolve_fast import *
from for_back_extension import *
from filter_overlap import *
from amplitude_power_filt import *
from comparison import *
from clump import *
from write_audio import *

# Audio File Parameters
audio_path = 'D:\\Dorian\\syllable_detection\\Audio\\2hr.flac'
filtered_audio_path = 'D:\\Dorian\\syllable_detection\\Audio_Filtered\\2hr_filtered.flac'
#audio_path = 'D:\\Dorian\\syllable_detection\\Audio\\30Label.wav'
#filtered_audio_path = 'D:\\Dorian\\syllable_detection\\Audio_Filtered\\30Label_filtered.wav'


# Convolution
time_short = 50 # ms
time_long = 250 # ms
short_smooth = convolve_fast(filtered_audio_path, 
                             time_short);
long_smooth = convolve_fast(filtered_audio_path, 
                            time_long);

#signal = np.array(AudioSegment.from_file(
#            file = filtered_audio_path, 
#            format = "flac").get_array_of_samples());
fs = 30000; # Sampling rate

# Calculate overlapping sections
overlap_threshold = 30
min_time = 40 # ms

min_samples = (min_time / 1000) * fs
time_threshold = .4 # seconds
threshold_samples = time_threshold * fs

overlap = filter_overlap(short_smooth,long_smooth,overlap_threshold)
print(f"Dropping overlaps under: {min_time} ms.")
noshort = remove_short_overlaps(overlap,min_samples)

cut_signal = update_overlap(filtered_audio_path,noshort,threshold_samples)

# Filtering by amplitude and power spectrum
noise_threshold = 8000
target_frequency = 4000
power_threshold = 100

# Comparison frequencies
low_upper_limit = 1000 # Hz
high_upper_limit = [3500,5000] # Hz

#cut_signal = amplitude_power_filt(cut_signal,fs,noise_threshold,target_frequency,power_threshold)
cut_signal = comparison(cut_signal, audio_path, low_upper_limit, high_upper_limit, noise_threshold)

# Backwards extension
back_time = 100 # ms
back = for_back_extension(cut_signal,filtered_audio_path,back_time)
cut_sections = clump(back)

# Write audio files
write_folder = "cut_audio/"
write_audio(back,
            cut_sections,
            filtered_audio_path,
            write_folder)
print(f"Total sections: {len(cut_sections)} ")
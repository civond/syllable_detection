# Imports
import numpy as np
from pydub import AudioSegment

# Filter sections via amplitude threshold, and power spectrum
def amplitude_power_filt(cut_signal,fs,noise_threshold,target_frequency,power_threshold):
    start_indices = np.where(~np.isnan(cut_signal) & ~np.roll(~np.isnan(cut_signal), 1))[0]
    chunk_lengths = np.diff(np.append(start_indices, len(cut_signal)))

    for start, length in zip(start_indices, chunk_lengths):
        # Define Section
        nan_count = np.sum(np.isnan(cut_signal[start:start+length]));
        end = start+length-nan_count;
        section = cut_signal[start:end];
        
        # Amplitude Thresholding
        max_region_value = np.max(np.abs(section))
        if max_region_value > noise_threshold:
            cut_signal[start:start + length] = np.nan;
        
        # FFT
        temp_fft = np.fft.fft(section)
        power_spectrum = np.abs(temp_fft) ** 2
        freq = np.fft.fftfreq(len(power_spectrum), 1 / fs)
        closest_index = np.argmin(np.abs(freq - target_frequency))
        power_at_target_frequency = 10 * np.log10(power_spectrum[closest_index])

        frequency_range = 10  # Adjust as needed
        indices_in_range = np.where((freq >= target_frequency - frequency_range) & (freq <= target_frequency + frequency_range))

        average_power_in_range = 10 * np.log10(np.mean(power_spectrum[indices_in_range]))
        
        if average_power_in_range > power_threshold:
            print(f"\tSection {start} accepted.")
            continue
        else: 
            cut_signal[start:start + length] = np.nan
    return cut_signal

# Forwards and backwards extension in time (to avoid cutting in the middle of something)
def for_back_extension(cut_signal, audio_path,extension_length):
    signal = AudioSegment.from_file(file = audio_path, format = "flac")
    fs = signal.frame_rate
    y = np.array(signal.get_array_of_samples())
    back = cut_signal.copy()
    extension_samples = round((extension_length / 1000) * fs)
    print(f"Adding forwards and backwards extension: {extension_length} ms ({extension_samples} samples).")
    
    start_indices = np.where(~np.isnan(back) & ~np.roll(~np.isnan(back), 1))[0]
    chunk_lengths = np.diff(np.append(start_indices, len(back)))
    for start, length in zip(start_indices, chunk_lengths):
        nan_count = np.sum(np.isnan(back[start:start+length])) # Count of how many NaN's in each chunk
        lower_limit = start-extension_samples
        upper_limit = start+length+extension_samples-nan_count
        
        back[lower_limit:upper_limit] = y[lower_limit:upper_limit]
    return back

# Main function
def get_valid_regions(cut_signal, config):
    filtered_audio_path = config['Directories']['filtered_audio_path'];
    threshold_noise= config['Main']['threshold_noise'];
    target_frequency = config['Main']['target_frequency'];
    threshold_power = config['Main']['threshold_power'];
    fs = config['Main']['fs'];
    extension_time = config['Main']['time_extension'];
    
    cut_signal = amplitude_power_filt(cut_signal, fs, threshold_noise, target_frequency, threshold_power);
    cut_signal = for_back_extension(cut_signal, filtered_audio_path, extension_time)
    
    return cut_signal
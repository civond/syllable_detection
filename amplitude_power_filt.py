import numpy as np

def amplitude_power_filt(test,fs,noise_threshold,target_frequency,power_threshold):
    print(f"before: {test}")
    
    start_indices = np.where(~np.isnan(test) & ~np.roll(~np.isnan(test), 1))[0]
    chunk_lengths = np.diff(np.append(start_indices, len(test)))

    for start, length in zip(start_indices, chunk_lengths):
        section = test[start:start + length]
        section_without_nans = section[~np.isnan(section)]
        if not np.isnan(section[0]):
            max_region_value = np.max(np.abs(section_without_nans))
            if max_region_value > noise_threshold:
                print("\tSection exceeded amplitude threshold, dropping.")
                test[start:start + length] = np.nan
            
            temp_fft = np.fft.fft(section_without_nans)
            power_spectrum = np.abs(temp_fft) ** 2
            freq = np.fft.fftfreq(len(power_spectrum), 1 / fs)
            closest_index = np.argmin(np.abs(freq - target_frequency))
            power_at_target_frequency = 10 * np.log10(power_spectrum[closest_index])

            frequency_range = 10  # Adjust as needed
            indices_in_range = np.where((freq >= target_frequency - frequency_range) & (freq <= target_frequency + frequency_range))

            average_power_in_range = 10 * np.log10(np.mean(power_spectrum[indices_in_range]))
            
            if average_power_in_range > power_threshold:
                continue
            else: 
                print(f"\tSection failed to reach power threshold ({power_threshold}), dropping.")
                test[start:start + length] = np.nan
    return test
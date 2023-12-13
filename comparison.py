import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment

def comparison(cut_signal, audio_path, low_upper_limit, high_upper_limit, noise_threshold):
    
    # Import original signal
    original_signal = np.array(AudioSegment.from_file(
            file = audio_path, 
            format = "flac").get_array_of_samples());
    fs = 30000
    
    start_indices = np.where(~np.isnan(cut_signal) & ~np.roll(~np.isnan(cut_signal), 1))[0]
    chunk_lengths = np.diff(np.append(start_indices, len(cut_signal)))
    
    # Iterate through sections within cut signal
    for start, length in zip(start_indices, chunk_lengths):
                
        # Specify sections
        nan_count = np.sum(np.isnan(cut_signal[start:start+length]))
        end = start+length-nan_count
        
        original_section = original_signal[start:end]
        filtered_section = original_signal[start:end]
        
        
        #max_value = np.max(np.abs(filtered_section))
        #if max_value > noise_threshold:
        #    filtered_section = np.nan
        
        # FFT
        temp_fft = abs(np.fft.fft(original_section))
        temp_power = temp_fft ** 2
        temp_freq = np.fft.fftfreq(len(temp_fft), 1 / fs)
        
        # Closest corresponding frequency value
        closest_zero = np.argmin(np.abs(temp_freq))
        closest_low = np.argmin(np.abs(temp_freq - low_upper_limit))
        
        closest_high_low = np.argmin(np.abs(temp_freq - high_upper_limit[0]))
        closest_high_high = np.argmin(np.abs(temp_freq - high_upper_limit[1]))
        idx = np.argsort(temp_freq)
        
        # Calculate the integral of power spectrum within specified ranges
        integral_low = np.trapz(temp_power[closest_zero:closest_low], 
                            temp_freq[closest_zero:closest_low])
        
        integral_high = np.trapz(temp_power[closest_high_low:closest_high_high], 
                             temp_freq[closest_high_low:closest_high_high])
        
        plt.plot(temp_freq[closest_zero:closest_low],
                 temp_power[closest_zero:closest_low],
                 color='b')
        plt.plot(temp_freq[closest_high_low:closest_high_high],
                 temp_power[closest_high_low:closest_high_high],
                 color='r')
        plt.title(f"Section {start}")

        # If area of high integral is greater than 3*integral low
        if integral_high > integral_low*3:
            print(f"Section: {start}\n\tLo: {integral_low} \n\tHi: {integral_high}")
            print(f"\tpasses!")
            plt.show()
            continue
        else:
            cut_signal[start:start + length] = np.nan
            #print(f"\trejected.")
    return cut_signal
        #print(temp_freq)
        #print("Area under the curve:", area_under_curve)


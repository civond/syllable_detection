# Imports
import scipy.signal
from pydub import AudioSegment
import numpy as np

# FFT() based convolution
def convolve_fast(audio_path, time):
    print(f"Convolving signal with window of length: {time} ms.");
    signal = AudioSegment.from_file(file = audio_path, format = "flac");
    y = np.array(signal.get_array_of_samples());
    y_abs = abs(y);
    fs = signal.frame_rate;
    samples = int((time/(10**3)) * fs); # Time must be in ms
    weights = (1/samples) * np.ones(samples);
    smooth = scipy.signal.fftconvolve(y_abs,weights,'same');
    
    return smooth

# Calculates overlap between short_smooth and long_smooth
def filter_overlap(short_smooth,long_smooth,overlap_threshold):
    print(f"Calculating the overlap with min threshold value: {overlap_threshold}");
    temp = short_smooth - long_smooth;
    temp_mask = temp < overlap_threshold;
    temp[temp_mask] = np.nan;
    
    return temp

# Remove overlaps under a minimum time threshold
def remove_short_overlaps(overlap, min_consecutive):
    print(f"Removing sections under minimum length threshold ({min_consecutive} samples)");
      
    # Define start indices / chunk lengths
    updated_overlap = overlap.copy();
    start_indices = np.where(~np.isnan(updated_overlap) & ~np.roll(~np.isnan(updated_overlap), 1))[0];
    chunk_lengths = np.diff(np.append(start_indices, len(updated_overlap)));

    # Iterate over start indices
    for start, length in zip(start_indices, chunk_lengths):
        nan_count = np.sum(np.isnan(updated_overlap[start:start+length]));
        if (length-nan_count) < min_consecutive:
            updated_overlap[start:start + length] = np.nan;
    print(f"\t# points before dropping: {np.count_nonzero(~np.isnan(overlap))}");
    print(f"\t# points after dropping: {np.count_nonzero(~np.isnan(updated_overlap))}");
    
    return updated_overlap

def update_overlap(audio_path, overlap, maxZeros):
    print(f"Concating regions within {maxZeros} samples and applying cut operation.");
    signal = AudioSegment.from_file(file = audio_path, format = "flac");
    array = np.array(signal.get_array_of_samples());
    
    # Define start indices / chunk lengths
    start_indices = np.where(~np.isnan(overlap) & ~np.roll(~np.isnan(overlap), 1))[0];
    chunk_lengths = np.diff(np.append(start_indices, len(overlap)));
    
    # Iterate over start indices
    for start, length in zip(start_indices, chunk_lengths):
        end = start+length;
        nan_count = np.sum(np.isnan(overlap[start:start+length]));
        
        if nan_count < maxZeros:
            overlap[start:end] = array[start:end];
        else:
            overlap[start:end-nan_count] = array[start:end-nan_count];
    print(f"Cut operation finished!");
           
    return overlap

# Main function
def calculate_mask(config):
    # Input signal
    filtered_audio_path = config['Directories']['filtered_audio_path'];
    
    # Time values
    time_short = config['Main']['time_short'];
    time_long = config['Main']['time_long'];
    
    # Threshold values
    threshold_overlap = config['Main']['threshold_overlap']; # Threshold value for section
    threshold_minimum_time = config['Main']['threshold_overlap']; # Sections under this time ignored
    threshold_time = config['Main']['threshold_time']; # Merge within this distance
    fs = config['Main']['fs'];
    
    threshold_samples = (threshold_time / 1000) * fs;
    threshold_minimum_samples = (threshold_minimum_time / 1000) * fs;

    # Moving Averages
    short_smooth = convolve_fast(filtered_audio_path, 
                                time_short);
    long_smooth = convolve_fast(filtered_audio_path, 
                                time_long);
    
    # Calculate mask from moving average results
    overlap = filter_overlap(short_smooth,long_smooth,threshold_overlap);
    overlap = remove_short_overlaps(overlap,threshold_minimum_samples);
    
    # Apply mask to input signal
    cut_signal = update_overlap(filtered_audio_path, overlap,threshold_samples);
    
    return cut_signal
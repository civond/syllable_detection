import numpy as np
from pydub import AudioSegment

def update_overlap(audio_path, overlap, maxZeros):
    print(f"Reading overlap mask and applying it to original signal... \n Concating overlaps within {maxZeros} samples.")
    signal = AudioSegment.from_file(file = audio_path, format = "flac")
    array = np.array(signal.get_array_of_samples())
    
    start_indices = np.where(~np.isnan(overlap) & ~np.roll(~np.isnan(overlap), 1))[0]
    chunk_lengths = np.diff(np.append(start_indices, len(overlap)))
    
    for start, length in zip(start_indices, chunk_lengths):
        end = start+length
        nan_count = np.sum(np.isnan(overlap[start:start+length]))
        
        if nan_count < maxZeros:
            overlap[start:end] = array[start:end]
        else:
            overlap[start:end-nan_count] = array[start:end-nan_count]
            
    return overlap

'''
def update_overlap(audio_path, overlap, maxZeros):
    print(f"Reading overlap mask and applying it to original signal... \n Concating overlaps within {maxZeros} samples.")
    signal = AudioSegment.from_file(file = audio_path, format = "flac")
    array = np.array(signal.get_array_of_samples())

    updated_overlap = overlap.copy()  # Create a copy of the overlap array to avoid modifying it in place
    valid_indices = np.where(~np.isnan(overlap))[0]
    updated_overlap[valid_indices] = array[valid_indices]

    after_zeros = np.zeros(len(overlap), dtype=int)
    is_nan = np.isnan(overlap)
    current_zeros = 0

    for i in range(len(overlap) - 1, -1, -1):
        if is_nan[i]:
            current_zeros += 1
        else:
            current_zeros = 0
        after_zeros[i] = current_zeros

    invalid_indices = np.where(is_nan & (after_zeros < maxZeros))[0]
    updated_overlap[invalid_indices] = array[invalid_indices]
    updated_overlap = np.array(updated_overlap) # numpy array
    
    return updated_overlap
'''
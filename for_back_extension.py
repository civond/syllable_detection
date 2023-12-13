import numpy as np
from pydub import AudioSegment

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


# This is the original, unoptimized version

'''
def back_extension(overlap, original,extension_length):
    print(f"Adding back extension: {extension_length} ms.")
    updated_overlap = overlap.copy()
    extension_samples = round((extension_length / 1000) * 30000)
    
    for i in range(len(overlap)-1):
        if not np.isnan(overlap[i]) and np.isnan(overlap[i+1]) :
            updated_overlap[i+1:i+extension_samples+1] = original[i+1:i+extension_samples+1] # Adds backwards extension
    print(f"Finished adding back extension.")
    return updated_overlap
'''
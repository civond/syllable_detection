import numpy as np

def filter_overlap(short_smooth,long_smooth,overlap_threshold):
    print(f"Calculating the overlap with min threshold value: {overlap_threshold}")
    overlap = np.empty(len(long_smooth)) # Preallocate zeros to temp
    overlap[:] = np.nan
    temp = short_smooth - long_smooth
    for i in range(len(temp)):
        if temp[i] > overlap_threshold:
            overlap[i] = temp[i]
    return overlap
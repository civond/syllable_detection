import numpy as np

def filter_overlap(short_smooth,long_smooth,overlap_threshold):
    print(f"Calculating the overlap with min threshold value: {overlap_threshold}")
    temp = short_smooth - long_smooth
    temp_mask = temp < overlap_threshold
    temp[temp_mask] = np.nan
    
    return temp
import numpy as np

def update_overlap(array, overlap, maxZeros):
    print('Reading overlap mask and applying it to original signal... \n Concating overlaps within %s samples.' % maxZeros)
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

    print('Finished')
    return updated_overlap

'''
import numpy as np

def update_overlap(array, overlap, maxZeros):
    updated_overlap = overlap.copy()  # Create a copy of the overlap array to avoid modifying it in place

    for i in range(len(overlap)):
        if not np.isnan(overlap[i]):
            updated_overlap[i] = array[i]
    ####
    # Calculate the number of consecutive zeros or NaN before each element
    before_zeros = [0] * len(overlap)
    current_zeros = 0
    for i in range(len(overlap)):
        if overlap[i] == np.isnan(overlap[i]):
            current_zeros += 1
        else:
            current_zeros = 0
        before_zeros[i] = current_zeros
    ####
        
    # Calculate the number of consecutive zeros or NaN after each element
    after_zeros = [0] * len(overlap)
    current_zeros = 0
    for i in range(len(overlap) - 1, -1, -1):
        if np.isnan(overlap[i]):
            current_zeros += 1
        else:
            current_zeros = 0
        after_zeros[i] = current_zeros

    for i in range(len(overlap)):
        #if (np.isnan(overlap[i])) and before_zeros[i] < maxZeros and after_zeros[i] < maxZeros:
        if (np.isnan(overlap[i])) and after_zeros[i] < maxZeros:
            updated_overlap[i] = array[i]

    return updated_overlap
'''
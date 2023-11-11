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
import numpy as np

def remove_short_overlaps(overlap, min_consecutive):
    print('# points before drop: ' + str(np.count_nonzero(~np.isnan(overlap))))
    
    updated_overlap = overlap.copy()
    start_indices = np.where(~np.isnan(updated_overlap) & ~np.roll(~np.isnan(updated_overlap), 1))[0]
    # Find the lengths of consecutive non-NaN chunks
    chunk_lengths = np.diff(np.append(start_indices, len(updated_overlap)))

    for start, length in zip(start_indices, chunk_lengths):
   
        
        if length < min_consecutive:
            print(f"\tSection did not meet length threshold ({min_consecutive} samples), dropping...")
            updated_overlap[start:start + length] = np.nan
    print('# points after drop: ' + str(np.count_nonzero(~np.isnan(updated_overlap))))
    return updated_overlap
'''
def remove_short_overlaps(overlap, min_consecutive):
    updated_overlap = overlap.copy()

    current_consecutive = 0  # To keep track of the current consecutive non-zero values

    for i in range(len(overlap)):
        if not np.isnan(overlap[i]):
            current_consecutive += 1
        else:
            if current_consecutive > 0 and current_consecutive < min_consecutive:
                for j in range(i - current_consecutive, i):
                    updated_overlap[j] = np.nan
            current_consecutive = 0

    return updated_overlap
'''
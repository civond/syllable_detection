import numpy as np

def remove_short_overlaps(overlap, min_consecutive):
    print('# points before drop: ' + str(np.count_nonzero(~np.isnan(overlap))))
    
    updated_overlap = overlap.copy()
    start_indices = np.where(~np.isnan(updated_overlap) & ~np.roll(~np.isnan(updated_overlap), 1))[0]
    chunk_lengths = np.diff(np.append(start_indices, len(updated_overlap)))

    for start, length in zip(start_indices, chunk_lengths):
        nan_count = np.sum(np.isnan(updated_overlap[start:start+length]))
        
        if (length-nan_count) < min_consecutive:
            print(f"\tSection did not meet length threshold ({min_consecutive} samples), dropping...")
            updated_overlap[start:start + length] = np.nan
    print('# points after drop: ' + str(np.count_nonzero(~np.isnan(updated_overlap))))
    
    return updated_overlap
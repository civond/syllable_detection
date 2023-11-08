import numpy as np

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
'''
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

overlap = np.array([1,2,3,np.nan,np.nan,6,np.nan,np.nan,5,1,2,3,np.nan,np.nan,np.nan])
print(overlap)
help = remove_short_overlaps(overlap,2)
'''
import numpy as np

def remove_short_overlaps(overlap, original, min_consecutive):
    updated_overlap = overlap.copy()

    current_consecutive = 0  # To keep track of the current consecutive non-NaN values

    for i in range(len(overlap)):
        if not np.isnan(overlap[i]):
            current_consecutive += 1
        else:
            if current_consecutive > 0 and current_consecutive < min_consecutive:
                for j in range(i - current_consecutive, i):
                    updated_overlap[j] = np.nan
            elif current_consecutive >= min_consecutive:
                # Add 3 points after each chunk of values that is not NaN
                updated_overlap[i:i+3] = original[i:i+3]
            current_consecutive = 0

    return updated_overlap

overlap = np.array([1, 2, 3, np.nan, np.nan,np.nan, np.nan,np.nan, np.nan, 6, np.nan, np.nan,np.nan, np.nan, 5, 1, 2, 3, np.nan, np.nan, np.nan])
original = np.array([1, 2, 3, 0.2, 0.2,0.2, 0.2,0.2, 0.2, 6, 0.2, 0.2,0.2, 0.2, 5, 1, 2, 3, 0.2, 0.2, 0.2])

#original = np.array(np.ones(len(overlap)))*10
print("Original overlap:")
print(overlap)
print(len(overlap))

help = remove_short_overlaps(overlap, original, 2)
print("\nOverlap after processing:")
print(help)
print(len(help))

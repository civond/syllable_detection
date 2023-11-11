import numpy as np

min_consecutive = 1
def back_extension(overlap, original, extension_length):
    updated_overlap = overlap.copy()
    extension_samples = round((extension_length / 1000) * 30000)

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
                updated_overlap[i:i+extension_samples] = original[i:i+extension_samples]
            current_consecutive = 0

    return updated_overlap
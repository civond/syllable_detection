import numpy as np
'''
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
                updated_overlap[i:i+extension_samples] = original[i:i+extension_samples]
            current_consecutive = 0

    return updated_overlap
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
import numpy as np

def back_extension(overlap, original,extension_length):
    print(f"Adding back extension: {extension_length} ms.")
    updated_overlap = overlap.copy()
    extension_samples = round((extension_length / 1000) * 30000)
    for i in range(len(overlap)-1):
        if not np.isnan(overlap[i]) and np.isnan(overlap[i+1]) :
            updated_overlap[i+1:i+extension_samples+1] = original[i+1:i+extension_samples+1] # Adds backwards extension
    print(f"Finished adding back extension.")
    return updated_overlap
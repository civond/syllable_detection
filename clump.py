import numpy as np

def clump(input):
    return [input[s] for s in np.ma.clump_unmasked(np.ma.masked_invalid(input))]
import numpy as np

overlap = np.array([1, 2, 3, np.nan, np.nan, 6, np.nan, np.nan, 5, 1, 2, 3, np.nan, np.nan, np.nan])

# Find the indices where consecutive non-NaN chunks start
start_indices = np.where(~np.isnan(overlap) & ~np.roll(~np.isnan(overlap), 1))[0]

# Find the lengths of consecutive non-NaN chunks
chunk_lengths = np.diff(np.append(start_indices, len(overlap)))

# Print out each section of non-NaN values without trailing NaNs

print(f"before: {overlap}")

for start, length in zip(start_indices, chunk_lengths):
    section = overlap[start:start + length]
    section_without_nans = section[~np.isnan(section)]
    if not np.isnan(section[0]):
        #print(f"Section: {section_without_nans}")
        #print(len(section_without_nans))
        
        if len(section_without_nans) <= 3:
            overlap[start:start + length] = np.nan
print(f"after: {overlap}")

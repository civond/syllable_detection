# Imports
import toml

# Custom scripts
from filter_audio import * # Preprocessing
from calculate_mask import * # Calculate mask
from get_valid_regions import * # Get valid regions from mask
from write_audio import * # Write .wav files

# Config file in .toml format
with open('config.toml', 'r') as f:
    config = toml.load(f);

# Preprocessing
filter_audio(config);

# Cut the signal
cut_signal = calculate_mask(config); # Generate cut sections
cut_signal = get_valid_regions(cut_signal, config); # Filter cut sections
write_audio(cut_signal,config); # Write audio files
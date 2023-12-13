# Imports
import toml

# Custom scripts
from calculate_mask import *
from get_valid_regions import *
from write_audio import *

# Config file in .toml format
with open('config.toml', 'r') as f:
    config = toml.load(f);

cut_signal = calculate_mask(config); # Generate cut sections
cut_signal = get_valid_regions(cut_signal, config); # Filter cut sections
write_audio(cut_signal,config) # Write audio files
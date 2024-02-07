# Imports
import toml
import os

# Custom scripts
from filter_audio import * # Preprocessing
from calculate_mask import * # Calculate mask
from get_valid_regions import * # Get valid regions from mask
from write_audio import * # Write .wav files

# Config file in .toml format
with open('config.toml', 'r') as f:
    config = toml.load(f);

# High pass audio signal
#filter_audio(config);

# Cut the signal
# Loop over files in ./Filtered_Audio_Directory/
filtered_audio_directory = config["Directories"]["filtered_audio_directory"];
for item in os.listdir(filtered_audio_directory):
    filtered_audio_path = os.path.join(filtered_audio_directory,item);
    
    cut_signal = calculate_mask(filtered_audio_path, config); # Generate cut sections
    cut_signal = get_valid_regions(cut_signal, filtered_audio_path, config); # Filter cut sections
    write_audio(cut_signal, filtered_audio_path, config); # Write audio files


#cut_signal = calculate_mask(config); # Generate cut sections
#cut_signal = get_valid_regions(cut_signal, config); # Filter cut sections
#write_audio(cut_signal, config); # Write audio files
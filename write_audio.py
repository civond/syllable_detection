import numpy as np
import os
from pydub import AudioSegment
from scipy.io.wavfile import write
import matplotlib.pyplot as plt

def clump(input):
    return [input[s] for s in np.ma.clump_unmasked(np.ma.masked_invalid(input))]


def write_audio(cut_signal, filtered_audio_path, config):
    # Parameters from config.toml
    #filtered_audio_path = config["Directories"]["filtered_audio_path"];
    write_directory = config["Directories"]["write_directory"];
    fs = config['Main']['fs'];
    
    # Extract maximum value from original signal to scale
    signal = AudioSegment.from_file(file = filtered_audio_path, format = "flac") #Original signal
    fs = signal.frame_rate
    y = np.array(signal.get_array_of_samples()) 
    
    # Starting indices
    start_indices = np.where(~np.isnan(cut_signal) & ~np.roll(~np.isnan(cut_signal), 1))[0];
    cut_sections = clump(cut_signal);
    print(f"Total sections: {len(cut_sections)} ");
    
    # Check if write directory exists
    if os.path.isdir(write_directory) == False:
        print(f"Write directory not found, creating: {write_directory}");
        os.mkdir(write_directory);
    else: 
        pass
    
    # Write sections
    for index, region in enumerate(cut_sections):
        filtered_audio_filename = filtered_audio_path.split('/')[-1].split('.')[0];
        #temp_num = int(filtered_audio_filename.split('_')[-1]) + start_indices[index];
        temp_num = start_indices[index]
        cut_file_name = filtered_audio_filename + "_" + str(temp_num) + ".wav"
        
        #cut_file_name = filtered_audio_path.split('\\')[-1].split('.')[0] + "_" + str(start_indices[index]) + ".wav" # Name of the cut file
        cut_file_path = os.path.join(write_directory,cut_file_name) # Cut filepath
        
        print(f"Writing: {cut_file_path}")
        scaled = np.int16((region/np.max(np.abs(y))) * 32767) # scale according to original signal
        write(cut_file_path, fs, scaled)
'''
def write_audio(cut, cut_sections,audio_path,write_folder):
    signal = AudioSegment.from_file(file = audio_path, format = "flac") #Original signal
    fs = signal.frame_rate
    y = np.array(signal.get_array_of_samples()) 
    start_indices = np.where(~np.isnan(cut) & ~np.roll(~np.isnan(cut), 1))[0]

    for index, region in enumerate(cut_sections):
        cut_file_name = audio_path.split('\\')[-1].split('.')[0] + "_" + str(start_indices[index]) + ".wav" # Name of the cut file
        cut_file_path = os.path.join(write_folder,cut_file_name) # Cut filepath
        
        print(f"Writing: {cut_file_path}")
        scaled = np.int16((region/np.max(np.abs(y))) * 32767) # scale according to original signal
        write(cut_file_path, fs, scaled)
'''
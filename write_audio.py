import numpy as np
import os
from pydub import AudioSegment
from scipy.io.wavfile import write
import matplotlib.pyplot as plt

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
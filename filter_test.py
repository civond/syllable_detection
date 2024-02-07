import scipy
import soundfile as sf
import librosa
from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt
import os
import toml

# Filter audio signal
def filter_audio(config):
    # Imports from config file
    audio_path = config["Directories"]["audio_path"];
    #audio_path = "Audio/2hr.flac"
    write_dir = config["Directories"]["filtered_audio_directory"];
    audio_name = audio_path.split('/')[1].split('.')[0] + '_filtered.flac';
    destination_path = os.path.join(write_dir,audio_name);
    
    #fs = config["Main"]["fs"];
    
    print(f"Initializing preprocessing on: {audio_path}");
    # Checks if destination path exists, if not, then generate filtered signal.
    #if os.path.exists(destination_path):
    #    print(f"\t{destination_path} already exists. Skipping.");
    #    pass
    
    #else:
        # import signal
    print(f"\t{destination_path} not found, proceeding...");
    print(f"Reading {audio_path}");
    #audio_file = np.array(AudioSegment.from_file(file = audio_path, 
    #                                             format = "flac"));
    #print(len(audio_file))
    
    [audio, fs] = librosa.load(audio_path, sr=None);
    
    print(audio)
    print(len(audio))
    print(fs)
        
    '''
    duration = len(audio_file)/1000; # Pydub does things in ms
    
    print(f"\tLength: {len(audio_file)} samples.");
    print(f"\tDuration: {duration} s.");
    y = np.array(audio_file.get_array_of_samples());
    fs = audio_file.frame_rate;
    print(f"\tSample rate: {fs}");
    dt = 1/fs;
    t = np.arange(0,duration,dt);

    # Filter parameters
    cutoff_freq = 350; # Hz
    minimum_attenuation = 30; # dB
    order = 8;
    [b, a] = scipy.signal.cheby2(order,
                                minimum_attenuation,
                                cutoff_freq,
                                fs=fs,
                                btype="high");

    [w, h] = scipy.signal.freqz(b, a,fs=fs,worN=2000);
    
    # Filter and scaling to max value.
    y_filtered = scipy.signal.filtfilt(b,a,y);
    scaled = np.int16(y_filtered / np.max(np.abs(y_filtered)) * 32767);
    
    # Checks if write directory exists
    if os.path.isdir(write_dir) == False:
        print(f"Write directory not found, creating: {write_dir}");
        os.mkdir(write_dir);
    else: 
        pass
    
    # Write audio
    print(f"Writing to: {destination_path}");
    sf.write(destination_path, 
                scaled, 
                fs, 
                format='FLAC');
    
    #print("Updating config.toml")
    #config["Directories"]["filtered_audio_path"] = destination_path;
    #f = open(config["Directories"]["self"], 'w');
    #toml.dump(config, f);
    #f.close()
    #wavfile.write(destination_path, fs, scaled)
'''
with open('config.toml', 'r') as f:
    config = toml.load(f);
filter_audio(config)

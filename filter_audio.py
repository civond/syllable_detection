import scipy
from scipy.io import wavfile
import soundfile as sf
from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt
import os
import toml

# Filter audio signal
def filter_audio(config):
    # Imports from config file
    audio_path = config["Directories"]["audio_path"];
    write_dir = config["Directories"]["filtered_audio_directory"];
    audio_name = audio_path.split('/')[1].split('.')[0] + '_filtered.flac';
    destination_path = os.path.join(write_dir,audio_name);
    
    print(f"Initializing preprocessing on: {audio_path}");
    # Checks if destination path exists, if not, then generate filtered signal.
    if os.path.exists(destination_path):
        print(f"\t{destination_path} already exists. Skipping.");
        pass
    
    else:
        # import signal
        print(f"\t{destination_path} not found, proceeding...");
        print(f"Reading {audio_path}");
        wav = AudioSegment.from_file(file = audio_path, format = "flac");
        duration = len(wav)/1000; # Pydub does things in ms
        
        print(f"\tLength: {len(wav)} samples.");
        print(f"\tDuration: {duration} s.");
        y = np.array(wav.get_array_of_samples());
        fs = wav.frame_rate;
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
# Plotting signals
plt.figure(1)
plt.title("%s Audio Waveform"% file_name)
plt.plot(t,y,
         linewidth='1', 
         color='g')
plt.plot(t,y_filtered,
         linewidth=0.5,
         linestyle='--',
         color='b')
plt.legend(['Original', 'Filtered'])
plt.grid(True)
plt.xlabel("Time (s)")
#plt.xlim(0,max(t))
#plt.xlim(23.5,26)
#plt.ylim(-0.5*10**9,0.5*10**9)
plt.ylabel("Amplitude")
plt.show()

# Frequency Response
plt.figure(2)
plt.plot(w,20 * np.log10(abs(h)), 
         linewidth=1,
         color='b')
#plt.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)], '--')
plt.plot([0, 0.5 * fs], [-minimum_attenuation, -minimum_attenuation], 
         '--', 
         linewidth=0.8,
         color='r')
plt.plot([cutoff_freq, cutoff_freq], [-60,0], 
         '--',
         linewidth=0.8,
         color='g')
plt.legend(['Magnitude Response','Minimum Attenuation','Cutoff Frequency'])
plt.title('HP Magnitude Response')
plt.xlabel('Hz')
plt.xlim(0,1000)
plt.ylabel('Magnitude (dB)')
plt.grid(True)
plt.show()
'''
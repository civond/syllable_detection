import numpy as np
from pydub import AudioSegment
from scipy.io.wavfile import write
import matplotlib.pyplot as plt


# Moving Average Window Parameters
time_short = 50 # ms
time_long = 250 # ms

# Audio File Parameters
audio_path = 'D:\\Dorian\\My_Scripts\\30Label_filtered.wav'
signal = AudioSegment.from_file(file = audio_path, 
                             format = "wav")
duration = len(signal)/1000 
y = np.array(signal.get_array_of_samples())
y_abs = abs(y)
fs = signal.frame_rate
dt = 1/fs
t = np.arange(0,duration,dt)

# Convolution
short_samples = int((time_short/(10**3)) * fs)
short_weights = (1/short_samples) * np.ones(short_samples)
short_smooth = np.convolve(y_abs,short_weights,mode='same')

long_samples = int((time_long/(10**3)) * fs)
long_weights = (1/long_samples) * np.ones(long_samples)
long_smooth = np.convolve(y_abs,long_weights,mode='same')

overlap = np.zeros(len(y)) # Preallocate zeros to temp
for index , value in enumerate(short_smooth):
    if short_smooth[index] - long_smooth[index] > 30:
        overlap[index] = value

# Extract overlaps from temp
overlap_vals = []
overlap_t = []
temp_val = []
temp_t = []

for index, value in enumerate(overlap):
    if value != 0:
        temp_val.append(value)
        temp_t.append(t[index])
    elif temp_val:
        overlap_vals.append(np.array(temp_val))
        overlap_t.append(np.array(temp_t))
        temp_val = []
        temp_t = []
print(len(overlap_vals))
min_time = 50 # ms
min_samples = (min_time/1000)*fs
print(min_samples)
overlap_vals = [value for value in overlap_vals if len(value) >= min_samples]
overlap_t = [value for value in overlap_t if len(value) >= min_samples]
print(len(overlap_vals))

# Merge groups values
print('Merging Groups: ')
time_threshold = 0.7 # Seconds
result_t = []
result_vals = []
current_group = [overlap_t[0]]
current_group_vals = [overlap_vals[0]]

# I am a fucking idiot. Need to take actual values instead of peak values.
for i in range(1, len(overlap_t)):
    time_difference = overlap_t[i][0] - current_group[-1][-1]
    if time_difference <= time_threshold:
        current_group.append(overlap_t[i])
        current_group_vals.append(overlap_vals[i])
    else:
        result_t.append(np.concatenate(current_group, axis=0))
        result_vals.append(np.concatenate(current_group_vals, axis=0))
        current_group = [overlap_t[i]]
        current_group_vals = [overlap_vals[i]]

# Append the last group
result_t.append(np.concatenate(current_group, axis=0))
result_vals.append(np.concatenate(current_group_vals, axis=0))
    
# Plotting smoothed signal
print('Generating Figure 1: ')
plt.figure(1)
plt.plot(t,short_smooth,
        color='b',
        linewidth=1)
plt.plot(t,long_smooth,
        color='g',
        linewidth=1)

# Plot Overlap
for index, group in enumerate(overlap_vals):
    plt.plot(overlap_t[index], overlap_vals[index],
             color='r',
             linewidth=1)

plt.xlim(0,max(t))
plt.title('Smoothing Filter Overlap')
plt.ylabel('abs(amplitude)')
plt.xlabel('Time (s)')
plt.legend(['Short Smooth',
            'Long Smooth',
            'Short-Long Smooth Overlap'])
plt.grid(True)
plt.savefig('fig1.jpg',dpi='figure')


# Plot regions of interest overlaid onto audio waveform
print('Generating Figure 2: ')
plt.figure(2)
plt.plot(t,y,
         linewidth=1,
         color='b')
for index, group in enumerate(result_t):
    plt.plot([result_t[index][0],result_t[index][-1]], [10000,10000], 
             color='black',
             linewidth=3,
             linestyle='-')
    '''
    plt.plot([result_t[index][0]-0.06,result_t[index][0]], [10000,10000],
             color='red',
             linewidth=5)
    plt.plot([result_t[index][-1],result_t[index][-1]+0.06], [10000,10000],
             color='red',
             linewidth=5)
    '''
plt.grid(True)
plt.title('Regions of Interest in Audio Waveform')
plt.xlabel('Time (s)')
plt.xlim(0,max(t))
plt.ylabel('Amplitude')
plt.legend(['Audio',
            'Region of Interest',
            'Extension (red)'])
plt.savefig('fig2.jpg',dpi='figure')
#plt.show()

# Writing audio
for index, region in enumerate(result_vals):
    folder = "cut_audio/"
    print(region)
    cut_file_name = folder + audio_path.split('\\')[-1].split('.')[0] + "_" + str(index) + ".wav"
    scaled = np.int16(region / np.max(np.abs(region)) * 32767)
    write(cut_file_name, fs, scaled)
    
    
    #rate = 44100
    #data = np.random.uniform(-1, 1, rate) # 1 second worth of random samples between -1 and 1
    #scaled = np.int16(data / np.max(np.abs(data)) * 32767)
    #write('test.wav', rate, scaled)


    print(cut_file_name)
    print(len(region))
    
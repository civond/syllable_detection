import numpy as np
from pydub import AudioSegment
audio_path = 'C:\\Users\\doria\\OneDrive\\Desktop\\Storage\\Coding projects\\finch\\cut_audio\\long_163.wav'
signal = AudioSegment.from_file(file = audio_path, 
                             format = "wav")
fs = signal.frame_rate
duration = len(signal)/(1000) 
audio = np.array(signal.get_array_of_samples())
# Compute the FFT
fft = np.fft.fft(audio)

# Calculate the power spectrum (squared magnitude of the FFT)
power_spectrum = np.abs(fft) ** 2
# Calculate the frequency values
freq = np.fft.fftfreq(len(power_spectrum), 1 / fs)
print(len(power_spectrum))
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(freq, 10 * np.log10(power_spectrum))  # Convert to dB
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power/Frequency (dB/Hz)")
plt.title("Power Spectrum")
plt.xlim(0, fs / 2)  # Only display positive frequencies
plt.grid(True)
plt.show()

target_frequency = 4000  # Replace with the desired frequency in Hertz

# Find the index of the closest frequency bin
closest_index = np.argmin(np.abs(freq - target_frequency))
power_at_target_frequency = 10 * np.log10(power_spectrum[closest_index])
# Define a frequency range around the target frequency (e.g., 10 Hz)
frequency_range = 10  # Adjust as needed

# Find the indices of frequency bins within the range
indices_in_range = np.where((freq >= target_frequency - frequency_range) & (freq <= target_frequency + frequency_range))

# Calculate the average power within the specified frequency range
average_power_in_range = 10 * np.log10(np.mean(power_spectrum[indices_in_range]))
print(average_power_in_range)

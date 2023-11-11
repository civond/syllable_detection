from filter_audio import *
import os

audio_directory = 'D:\\Dorian\\syllable_detection\\Audio'
destination_directory = 'D:\\Dorian\\syllable_detection\\Audio_Filtered'

for audio_file in os.listdir(audio_directory):
    path = os.path.join(audio_directory,audio_file)
    destination = os.path.join(destination_directory, audio_file.split('.')[0]+ '_filtered.wav')
    filter_audio(path,destination)
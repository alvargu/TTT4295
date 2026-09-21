# Assignment 1 - Music Box Sound Source - by Alvar Guddingsmo
# Date: 2026-09-21
# This script is used to visualize the full audio signal of the music box sound source.

import matplotlib.pyplot as plt
import scipy.fft
import scipy.io.wavfile as wav
import numpy as np

# Read the audio file
# Needed to fix the header of the wav file as it was recorded in stereo 
# format which is not supported by scipy.io.wavfile.read().
audioFilePath = "MusicBoxNotes_fixed.wav" 
fs, audioRecording = wav.read(audioFilePath)
# My audio file is stereo, so I will take only one channel for analysis
monoRecording = audioRecording[:, 0]
# Print out some data about the audio file
t = np.linspace(0, len(monoRecording)/fs, len(monoRecording))

# Define the figure for plotting
audioPlot = plt.figure(figsize=(12, 6))

# Plot the original audio signal
plt.plot(t, monoRecording)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Audio Signal")

# Save and display the plot
plt.savefig("audio_signal.png")
plt.show()

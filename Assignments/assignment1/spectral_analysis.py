import matplotlib.pyplot as plt
import scipy.fft
import scipy.io.wavfile as wav
import numpy as np

# Music Box Audio Notes - This array is used to store the audio snippets of the music box notes for analysis.
MB_AudioNotes = [None] * 34
# The positions of the start and end of each note in the audio file. 
# Found by running audio_signal.py and checking the using the samplenumber 
# for the time axis instead of the time in seconds.
MB_AudioNotesPos = [None] * 34

# Used to read multiple audio notes from the wav audio file into one array for ease of analysis.
def read_audio_notes(wavFilePath, snippetsPos):
     notesArray = [None] * len(snippetsPos)
     sampleRate, audioSignal = wav.read(wavFilePath)
     for i in range(len(snippetsPos)):
          notesArray[i] = audioSignal[snippetsPos[i][0]:snippetsPos[i][1]]
     return sampleRate, notesArray

# Compute the FFT for each of the notes with zero-padding.
def multi_fft(audioSignals, n):
     for i in range(len(audioSignals)):
          audioSignalsFFT = scipy.fft.fft(audioSignals[i], n=n)
     return audioSignalsFFT

# Read the audio file
audioFilePath = "MusicBoxNotes_fixed.wav" # Changed based on wich snippet I want to check
fs, MB_AudioNotes = read_audio_notes(audioFilePath, MB_AudioNotesPos)
# Find the length of the longest note for zero-padding
n = len(max(MB_AudioNotes, key=len))
# Compute the FFT for each of the notes
MB_AudioNotesFFT = multi_fft(MB_AudioNotes, n)

### Plotting the FFT of the audio signal
# # Define the figure for plotting
# audioPlot = plt.figure(figsize=(12, 6))
# # Plot the fft of the audio signal
# plt.plot(f, np.abs(audioFFT))
# plt.xlabel("Frequency (Hz)")
# plt.ylabel("Amplitude")
# plt.title("Spectral Analysis")
# # Save and display the plot
# plt.savefig("spectral_analysis.png")
# plt.show()

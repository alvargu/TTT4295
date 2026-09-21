import matplotlib.pyplot as plt
import scipy.fft
import scipy.io.wavfile as wav
import numpy as np

# Music Box Audio Notes - This array is used to store the audio snippets of the music box notes for analysis.
MB_audioNotes = [None] * 34
# The positions of the start and end of each note in the audio file. 
# Found by running audio_signal.py and checking the using the samplenumber 
# for the time axis instead of the time in seconds.
MB_audioNotesPos = [
     [85000, 240000],
     [247000, 403000],
     [512, 1200],
     [1200, 3000],
     [3000, 5000],
     [5000, 7000],
     [7000, 9000],
     [9000, 11000],
     [11000, 13000],
     [13000, 15000],
     [15000, 17000],
     [17000, 19000],
     [19000, 21000],
     [21000, 23000],
     [23000, 25000],
     [25000, 27000],
     [27000, 29000],
     [29000, 31000],
     [31000, 33000],
     [33000, 35000],
     [35000, 37000],
     [37000, 39000],
     [39000, 41000],
     [41000, 43000],
     [43000, 45000],
     [45000, 47000],
     [47000, 49000],
     [49000, 51000],
     [51000, 53000],
     [53000, 55000],
     [55000, 57000],
     [57000, 59000],
     [59000, 61000],
     [61000, 63000]
]

# Compute the FFT for each of the notes with zero-padding.
def multi_fft(audioSignals, n):
     for i in range(len(audioSignals)):
          audioSignalsFFT = scipy.fft.fft(audioSignals[i, :], n=n)
     return audioSignalsFFT

# Generates a fig containing the audiosignal with markers for the start and end of 
# the specific note, as well as the FFT of the audio signal.
def plot_note_params(t, audioSignal, f, audioNoteFFT):
     # Define the figure with its subplots for plotting
     fig, axs = plt.subplots(2, 1, figsize=(24, 12))
     # Plot the audio signal in the time domain subplot
     axs[0].plot(t, audioSignal)
     # Add vertical lines to indicate the start and end of the note in the time domain plot
     axs[0].axvline(x=t[MB_audioNotesPos[0][0]], color='r', 
                    linestyle='--', label='Note Start'
                    )
     axs[0].axvline(x=t[MB_audioNotesPos[0][1]], color='r', 
                    linestyle='--', label='Note End'
                    )
     # Labeling for the axes and the plot itself
     axs[0].set_xlabel("Time (s)")
     axs[0].set_ylabel("Amplitude")
     axs[0].set_title("Audio Signal")

     # Plot the FFT of the audio signal in the frequency domain subplot
     axs[1].plot(f, np.abs(audioNoteFFT[:len(audioNoteFFT)//2 + 1]))
     # Labeling for the axes and the plot itself
     axs[1].set_xlabel("Frequency (Hz)")
     axs[1].set_ylabel("Magnitude")
     axs[1].set_title("Frequency Spectrum")
     # Save and display the plot
     plt.tight_layout()
     plt.savefig("spectral_analysis.png")
     plt.show()
     return

# Read the full audio file of the music box sound source as a mono signal.
audioFilePath = "MusicBoxNotesMono.wav"
fs, MB_audioSignal = wav.read(audioFilePath)
t = np.linspace(0, len(MB_audioSignal)/fs, len(MB_audioSignal))
# Split the audio signal into individual notes based on the positions defined in MB_audioNotesPos.
for i in range(len(MB_audioNotesPos)):
     MB_audioNotes[i] = MB_audioSignal[MB_audioNotesPos[i][0]:MB_audioNotesPos[i][1]]

# Find the length of the longest note for zero-padding
n = len(max(MB_audioNotes, key=len))
# Compute the FFT for each of the notes
MB_audioNotesFFT = multi_fft(MB_audioNotes, n)
f = np.linspace(0, fs/2, len(MB_audioNotesFFT)//2 + 1)

### Using selfdefined function to plot the audio signal and its FFT for 
### the first note to have example for small delivery.
# To quote Obi-wan: "hello there" :)
plot_note_params(t, MB_audioSignal, f, MB_audioNotesFFT[0])

### Scraps
# # Define the figure for plotting
# MB_audioPlot = plt.figure(figsize=(12, 6))
# # Plot the fft of the audio signal
# plt.plot(t, MB_audioSignal)
# plt.axvline(x=t[MB_audioNotesPos[0][0]], color='r', linestyle='--', label='Note Start')
# plt.axvline(x=t[MB_audioNotesPos[0][1]], color='r', linestyle='--', label='Note End')
# plt.xlabel("Time (s)")
# plt.ylabel("Amplitude")
# plt.title("Spectral Analysis")
# # Save and display the plot
# plt.savefig("spectral_analysis.png")
# plt.show()

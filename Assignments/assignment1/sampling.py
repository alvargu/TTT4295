import matplotlib.pyplot as plt
import scipy.fft
import scipy.io.wavfile as wav
import numpy as np

# Read the audio file
audioFilePath = "path/to/your/audiofile.wav"
fs, audioRecording = wav.read(audioFilePath)
t = np.linspace(0, len(audioRecording)/fs, len(audioRecording))

# Compute the FFT and define the frequency axis
# audioFFT = scipy.fft.fft(audioRecording)
# f = np.linspace(0, fs/2, len(audioFFT)//2)

# Define the figure for plotting
audioPlot = plt.figure(figsize=(12, 6))

# Plot the original audio signal
plt.plot(t, audioRecording)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Original Audio Signal")

# Save and display the plot
plt.savefig(audioPlot, "audio_signal.png")
plt.show()

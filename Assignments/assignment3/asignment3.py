import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import freqz, lfilter

# Your deliverable should include the following:
# One plot of the output ”pulse train” signal for one note (e.g., A = 440 Hz) from Task 1, indicating the delay N in samples.
# One audio file of a plucked note using your best version of the synthesizer, combin- ing the fractional-delay filter, the frequency-dependent loop filter, and a noise-burst source signal (Tasks 2, 3 and 5).
# One plot of the FFT spectrum showing suppressed harmonics when the string is excited at the center (Task 4).
# One plot of the extracted source signal from the inverse filtering of TTT4295 Assignment3 soundfile1.mat (Task 8).

fs = 44100  # Sampling frequency
# n = 44100     # Number of samples
ref_co = 0.98  # Reflection coefficient for the digital waveguide

def write_to_wav(waveform, fs=fs, filename='NotAssigned.wav', filepath = 'C:/Users/Alvar/Documents/00_Skole/TTT4295/Assignments/assignment3/'):
     # normalize
     waveform = waveform / np.max(np.abs(waveform))
     wavfile.write(filepath + filename, fs, (waveform * 32767 * 0.9).astype(np.int16))
     return np.void

# Task 1:
def simple_1D_digital_waveguide(f, ref_co=ref_co, fs=fs):
     # Generate tone for the given frequency
     # N samples for full period
     N = int(np.round(fs / f))
     # Amount of samples of the tone needed for 40dB decay
     periods = int(np.ceil(-40 / (20 * np.log10(ref_co))))
     K = periods * N
     
     # Filter parameters
     B = 1.0
     A = np.zeros(N + 1)
     A[0] = 1
     A[N] = -ref_co
     
     t = np.linspace(0, K / fs, K + 1)
     pulse = np.zeros(K + 1)
     pulse[0] = 1
     tone = lfilter(B, A, pulse)
     return t, tone

def pulse_train_plot(f, samplingFrequency=fs):
     # Synthesize a pulse train signal for input frequency f using the digital waveguide model
     t, dwg_signal = simple_1D_digital_waveguide(f, ref_co, samplingFrequency)
     
     plt.figure(figsize=(10, 4))
     plt.plot(t, dwg_signal)
     plt.xlabel('Time [s]')
     plt.ylabel('Amplitude')
     plt.title('Pulse Train Signal')
     plt.grid(True)
     plt.show()
     return np.void

f_A = 440  # Frequency of note A
pulse_train_plot(f_A, ref_co)

# Synthesizing octave notes using the digital waveguide model
def simple_octave_notes_synthesis(samplingFrequency=fs, filename='music_notes_synthesis.wav'):
     space = np.zeros(int(fs/2))
     musical_notes = np.array([])
     # Generate a tone for each semitone
     for i in range(13):
          freq = 440 * 2**(i/12) # Frequency for said tone starting from A_440Hz
          tone = simple_1D_digital_waveguide(freq)
          musical_notes = np.append(musical_notes, tone)
          # Add spaces after the first 12 notes
          if i >= 12: break
          musical_notes = np.append(musical_notes, space)
     
     write_to_wav(musical_notes, filename=filename)
     return np.void

simple_octave_notes_synthesis()

# Task 2:
def fractional_delay_filter(x, delay):
     
     return np.void


# Task 3
def frequency_dependent_loop_filter(x, fs, cutoff_freq):
     return np.void
     

# Task 4
def source_position_filter(x, fs, position):
     return np.void
     

# Task 5
def source_signal_generator(fs, duration, noise_burst_duration):
     return np.void


def octave_notes_synthesis(samplingFrequency=fs, filename='music_notes_synthesis.wav'):
     # Initialize empty array for musical notes and a space of silence between them
     space = np.zeros(int(fs/2))
     musical_notes = np.array([])
     # Generate a tone for each semitone
     for i in range(13):
          freq = 440 * 2**(i/12) # Frequency for said tone starting from A_440Hz
          tone = simple_1D_digital_waveguide(freq)
          musical_notes = np.append(musical_notes, tone)
          # Add spaces after the first 12 notes
          if i >= 12: break
          musical_notes = np.append(musical_notes, space)
     
     write_to_wav(musical_notes, filename=filename)
     return np.void

# Task 6
def loop_filter_delay(x, fs, delay_time):
     return np.void


# Task 7
def loop_filter_decay(x, fs, decay_time):
     return np.void


#Task 8
def source_signal_extraction(y, fs, cutoff_freq):
     return np.void
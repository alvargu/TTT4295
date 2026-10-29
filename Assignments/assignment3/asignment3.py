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

def write_to_wav(waveform, fs=fs, filename='NotAssigned.wav'):
     wavfile.write(filename, fs, (waveform * 32767).astype(np.int16))
     return np.void

# Task 1:
def simple_1D_digital_waveguide(f, ref_co=ref_co, fs=fs):
     # Generate tone for the given frequency
     # N samples for full period
     N = int(np.round(f / fs))
     # Amount of periods of the tone needed for 40dB decay
     K = int(np.ceil(40 / (20 * np.log10(ref_co))) / N) 
     # Filter parameters
     B = 1
     A = np.zeros(N + 1)
     A[0] = 1
     A[N] = -ref_co
     
     t = np.linspace(0, K / fs, K)
     tone = np.linspace(0, N / fs, N)
     tone[0] = 1
     tone = lfilter(B, A, tone)
     return t, tone

def pulse_train_generation(f, samplingFrequency=fs):
     # Synthesize a pulse train signal for input frequency f using the digital waveguide model
     t, dwg_signal = simple_1D_digital_waveguide(f, ref_co, samplingFrequency)
     
     plt.figure(figsize=(10, 4))
     plt.plot(t, np.log(np.abs(dwg_signal)))
     plt.xlabel('Time [s]')
     plt.ylabel('Amplitude')
     plt.title('Pulse Train Signal')
     plt.grid(True)
     plt.show()
     return np.void

f_A = 440  # Frequency of note A
pulse_train_generation(f_A, ref_co)

# Synthesizing octave notes using the digital waveguide model
def octave_notes_synthesis(samplingFrequency=fs, filename='music notes synthesis.wav'):
     space = np.zeros(fs/2)
     musical_notes = np.array([])
     for i in range(13):
          freq = 440 * 2**(i/12)
          tone = simple_1D_digital_waveguide(freq)
          musical_notes = np.append(musical_notes, tone)
          if i >= 12: break
          musical_notes = np.append(musical_notes, space)
     
     write_to_wav(musical_notes, filename=filename)
     return np.void

octave_notes_synthesis()

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


# Task 6
def loop_filter_delay(x, fs, delay_time):
     return np.void


# Task 7
def loop_filter_decay(x, fs, decay_time):
     return np.void


#Task 8
def source_signal_extraction(y, fs, cutoff_freq):
     return np.void
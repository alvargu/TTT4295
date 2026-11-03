from matplotlib.pylab import beta
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile, loadmat
from scipy.signal import freqz, lfilter, correlate

filepath = 'C:/Users/Alvar/Documents/00_Skole/TTT4295/Assignments/assignment3/'

# Your deliverable should include the following:
# One plot of the output ”pulse train” signal for one note (e.g., A = 440 Hz) from Task 1, indicating the delay N in samples.
# One audio file of a plucked note using your best version of the synthesizer, combin- ing the fractional-delay filter, the frequency-dependent loop filter, and a noise-burst source signal (Tasks 2, 3 and 5).
# One plot of the FFT spectrum showing suppressed harmonics when the string is excited at the center (Task 4).
# One plot of the extracted source signal from the inverse filtering of TTT4295 Assignment3 soundfile1.mat (Task 8).

fs = 44100  # Sampling frequency
# n = 44100     # Number of samples
ref_co = 0.98  # Reflection coefficient for the digital waveguide

def write_to_wav(waveform, fs=fs, filename='NotAssigned.wav', folder=filepath):
     # normalize
     waveform = waveform / np.max(np.abs(waveform))
     wavfile.write(filepath + filename, fs, (waveform * 32767).astype(np.int16))
     return np.void

# Task 1:
def simple_1D_digital_waveguide(f, ref_co=ref_co, fs=fs):
     # Generate tone for the given frequency
     # N samples for one full period
     N = int(np.floor(fs / f))
     # Amount of samples of the tone needed for 40dB decay
     periods = int(np.ceil(-40 / (20 * np.log10(ref_co))))
     K = periods * N
     
     # Filter parameters
     B = 1.0
     A = np.zeros(N + 1)
     A[0] = 1
     A[N] = -ref_co
     
     K_out = np.linspace(0, K, K + 1)
     pulse = np.zeros(K + 1)
     pulse[0] = 1
     tone = lfilter(B, A, pulse)
     return K_out, tone

def pulse_train_plot(f, samplingFrequency=fs, periods_shown=10, ref_co=ref_co, folder=filepath):
     # Synthesize a pulse train signal for input frequency f using the digital waveguide model
     N, y = simple_1D_digital_waveguide(f)
     
     # Plot the pulse train signal
     plt.figure(figsize=(10, 4))
     plt.plot(N, y)
     plt.xlabel('Samples'); plt.ylabel('Amplitude')
     plt.title(f'Pulse train, f = {f} Hz, N = {len(N)} samples')
     plt.grid(True)
     plt.savefig(folder + f"pulse_train_{f}Hz.pdf")
     plt.show()
     return np.void

f_A = 440  # Frequency of note A
pulse_train_plot(f_A)

# Synthesizing octave notes using the digital waveguide model
def simple_octave_notes_synthesis(samplingFrequency=fs, filename='music_notes_synthesis_simple.wav'):
     space = np.zeros(int(fs/2))
     musical_notes = np.array([])
     # Generate a tone for each semitone
     for i in range(13):
          freq = 440 * 2**(i/12) # Frequency for said tone starting from A_440Hz
          _, tone = simple_1D_digital_waveguide(freq)
          musical_notes = np.append(musical_notes, tone)
          # Add spaces after the first 12 notes
          if i >= 12: break
          musical_notes = np.append(musical_notes, space)
     
     write_to_wav(musical_notes, filename=filename)
     return np.void

simple_octave_notes_synthesis()

# Task 2:
def fractional_delay_waveguide(f, ref_co=ref_co, fs=fs):
     # Generate tone for the given frequency
     # N samples between the current and next pulse in pulse train
     N_pulse = int(np.floor(fs / f))
     
     # N samples of the tone needed for 40dB decay
     periods = int(np.ceil(-40 / (20 * np.log10(ref_co))))
     N = periods * N_pulse
     # Fractional delay coefficient
     N_pulse_rest = fs / f - N_pulse
     C = (1 - N_pulse_rest) / (1 + N_pulse_rest)
     
     # Filter parameters
     B = [1, C]
     A = np.zeros(N_pulse + 2)
     A[0] = 1
     A[1] = C
     A[N_pulse] = -ref_co*C
     A[N_pulse+1] = -ref_co
     
     pulse = np.zeros(N + 2)
     pulse[0] = 1
     tone = lfilter(B, A, pulse)
     return N, tone


# Task 3
def frequency_dependent_loop_waveguide(f, fc=10000, ref_co=ref_co, fs=fs):
     # Generate tone for the given frequency
     # N samples between the current and next pulse in pulse train
     N_pulse = int(np.floor(fs / f))
     
     # N samples of the tone needed for 40dB decay
     periods = int(np.ceil(-40 / (20 * np.log10(ref_co))))
     N = periods * N_pulse
     # Fractional delay coefficient
     N_pulse_rest = fs / f - N_pulse
     C = (1 - N_pulse_rest) / (1 + N_pulse_rest)
     
     # Coefficient for the first order LP-filter
     a = fs / (np.pi * fc)
     
     # Filter parameters
     B = [(1+a), (C*(1+a)+(1-a)), (C*(1-a))]
     A = np.zeros(N_pulse + 3)
     A[0] = 1+a
     A[1] = (C*(1+a)+(1-a))
     A[2] = (C*(1-a))
     A[N_pulse] = -ref_co*C
     A[N_pulse+1] = -ref_co*(1+C)
     A[N_pulse+2] = -ref_co
     
     pulse = np.zeros(N + 1)
     pulse[0] = 1
     tone = lfilter(B, A, pulse)
     return N, tone
     

# Task 4
def source_position_waveguide(f, beta=0.33, fc=10000, ref_co=ref_co, fs=fs):
     # Coefficient for the first order LP-filter
     a = fs / (np.pi * fc)
     
     # Total loop delay, minus the ~a/2 samples the LP-filter adds
     N = fs / f - a / 2
     # N samples between the current and next pulse in pulse train
     N_pulse = int(np.floor(N))
     # Fractional delay coefficient
     N_pulse_rest = N - N_pulse
     C = (1 - N_pulse_rest) / (1 + N_pulse_rest)
     
     # N samples of the tone needed for 40dB decay
     periods = int(np.ceil(-40 / (20 * np.log10(ref_co))))
     
     # Filter parameters
     B = [(1+a), (C*(1+a)+(1-a)), (C*(1-a))]
     A = np.zeros(N_pulse + 3)
     A[0] = 1+a
     A[1] = (C*(1+a)+(1-a))
     A[2] = (C*(1-a))
     A[N_pulse] = -ref_co*C
     A[N_pulse+1] = -ref_co*(1+C)
     A[N_pulse+2] = -ref_co
     
     # Adjustment of the number of samples for the pulse train based on the source position beta
     Ne = int(round(beta * (N_pulse+N_pulse_rest) / 2))
     Np = 2 * Ne - 1
     
     L = int(np.ceil(periods * (N_pulse+N_pulse_rest))) + Np
     pulse = np.zeros(L)
     pulse[0] = 1
     pulse[Np] = -1
     tone = lfilter(B, A, pulse)
     return Np, tone

def source_position_fft_plot(f, pos=0.5, samplingFrequency=fs, n_harmonics=20, folder=filepath):
     # Synthesize the tone with the source position filter
     Np, tone = source_position_waveguide(f, beta=pos)
     
     # FFT (positive frequencies only), in dB relative to the strongest peak
     nfft = 2**18
     tone_fft = np.abs(np.fft.rfft(tone, nfft))
     freqs = np.fft.rfftfreq(nfft, 1 / samplingFrequency)
     tone_fft_db = 20 * np.log10(tone_fft / np.max(tone_fft) + 1e-12)
     
     # Plot the spectrum against harmonic number
     plt.figure(figsize=(10, 4))
     plt.plot(freqs / f, tone_fft_db)
     plt.xlim(0, n_harmonics + 0.5); plt.ylim(-60, 3)
     plt.xticks(range(1, n_harmonics + 1))
     plt.xlabel('Harmonic number (f / f$_0$)'); plt.ylabel('Magnitude [dB]')
     plt.title(f'FFT of waveguide with source position {pos}·l on string, f = {f} Hz')
     plt.grid(True)
     plt.savefig(folder + f"source_position_{pos}_{f}Hz.pdf")
     plt.show()

source_position_fft_plot(f_A, pos=0.5)


# Task 5
def source_signal_generator(fs, duration, noise_burst_duration, source='consum', seed=1):
     # Total number of samples, and samples in the noise burst
     L = int(np.ceil(duration * fs))
     L_burst = int(round(noise_burst_duration * fs))
     signal = np.zeros(L)
     
     if source == 'cumsum':
          # Low-pass filtered noise burst. Removing the mean first makes the
          # cumsum end at 0, so no DC step is left after the burst
          rng = np.random.default_rng(seed)
          burst = rng.standard_normal(L_burst)
          burst = np.cumsum(burst - np.mean(burst))
          signal[:L_burst] = burst / np.max(np.abs(burst))
     else:
               # Single pulse, as in Task 1-4
               signal[0] = 1
     return signal


def source_signal_waveguide(f, source='consum', noise_burst_duration=100/fs, fc=5000, ref_co=ref_co, fs=fs):
     # Coefficient for the first order LP-filter
     a = fs / (np.pi * fc)
     
     # Total loop delay, minus the ~a/2 samples the LP-filter adds
     N = fs / f - a / 2
     # N samples between the current and next pulse in pulse train
     N_pulse = int(np.floor(N))
     # Fractional delay coefficient
     N_pulse_rest = N - N_pulse
     C = (1 - N_pulse_rest) / (1 + N_pulse_rest)
     
     # Filter parameters
     B = [(1+a), (C*(1+a)+(1-a)), (C*(1-a))]
     A = np.zeros(N_pulse + 3)
     A[0] = 1+a
     A[1] = (C*(1+a)+(1-a))
     A[2] = (C*(1-a))
     A[N_pulse] -= ref_co*C
     A[N_pulse+1] -= ref_co*(1+C)
     A[N_pulse+2] -= ref_co
     
     # Duration needed for 40dB decay (+ the length of the noise burst)
     periods = int(np.ceil(-40 / (20 * np.log10(ref_co))))
     duration = periods / f + noise_burst_duration
     
     # Source signal in, tone out
     excitation = source_signal_generator(fs, duration, noise_burst_duration, source=source)
     tone = lfilter(B, A, excitation)
     return excitation, tone


def octave_notes_synthesis(samplingFrequency=fs, source='consum', filename='music_notes_synthesis.wav'):
     # Initialize empty array for musical notes and a space of silence between them
     space = np.zeros(int(fs/2))
     musical_notes = np.array([])
     # Generate a tone for each semitone
     for i in range(13):
          freq = 440 * 2**((i - 9)/12) # i = 9 is A_440Hz
          _, tone = source_signal_waveguide(freq, source=source)
          musical_notes = np.append(musical_notes, tone)
          # Add spaces after the first 12 notes
          if i >= 12: break
          musical_notes = np.append(musical_notes, space)
     
     write_to_wav(musical_notes, filename=filename)
     return np.void

octave_notes_synthesis(f_A)

# Task 6
# Needed to load the soundfile with matlab format
def load_soundfile(filename='TTT4295_Assignment3_soundfile1.mat', folder=filepath):
     # Load the signal and sampling frequency from the .mat file
     data = loadmat(folder + filename)
     sig = data['sig'].flatten()              # (n, 1) -> (n,)
     fs_sig = float(np.squeeze(data['fs']))   # [[fs]] -> fs
     return sig, fs_sig

def find_loop_delay(sig, min_lag=20):
     # : the autocorrelation peaks at the loop delay N
     r = correlate(sig, sig, mode='full')[len(sig)-1:]   # lags 0, 1, 2, ...
     N = int(np.argmax(r[min_lag:]) + min_lag)          # skip the peak at lag 0
     return N, r

# Task 7
def find_loop_gain(sig, N, floor_db=-60):
     # Task 7: largest |sig| in each round trip of N samples, in dB
     rounds = len(sig) // N
     peaks_db = np.array([20 * np.log10(np.max(np.abs(sig[k*N:(k+1)*N]))) for k in range(rounds)])
     # Only use rounds above the noise floor, then fit a straight line
     k = np.arange(rounds)
     keep = peaks_db > np.max(peaks_db) + floor_db
     slope_db, _ = np.polyfit(k[keep], peaks_db[keep], 1)    # dB lost per round trip
     R = 10**(slope_db / 20)
     return R

# Task 8
def inverse_filter_plot(samples_shown=300, folder=filepath):
     sig, fs_sig = load_soundfile()
     N, _ = find_loop_delay(sig)
     R = find_loop_gain(sig, N)
     
     # inverse filter is A(z)/1
     A = np.zeros(N + 1)
     A[0] = 1
     A[N] = -R
     source = lfilter(A, [1], sig)
     
     # Plot the extracted source signal
     n = np.arange(samples_shown)
     plt.figure(figsize=(10, 4))
     plt.plot(n, source[:samples_shown])
     plt.xlabel('Samples'); plt.ylabel('Amplitude')
     plt.title(f'Extracted source signal')
     plt.grid(True)
     plt.savefig(folder + "extracted_source.pdf", bbox_inches="tight")
     plt.show()
     return N, R, source

N, R, source = inverse_filter_plot()
print(f'N = {N} samples, R = {R:.4f}')
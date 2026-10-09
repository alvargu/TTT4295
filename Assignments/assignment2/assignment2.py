import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

from scipy.signal import freqz, lfilter

fs = 44100     # Sampling frequency
T = 1/fs       # Sampling period
c = 343        # Speed of sound in m/s
a = 0.09       # Head radius in m
# Variables for simplified HRTF model
beta = 2*c/a
theta = -60/180*np.pi #np.linspace(-np.pi/2, np.pi/2, 1000) 
def alpha_LR(theta): return 1 - np.sin(theta), 1 + np.sin(theta)
# Brown and Dauda (1997) simplified HRTF model
def H_analog(alpha, f): jw = 1j*2*np.pi*f; return (alpha*jw + beta)/(jw + beta)
# Derived digital IIR filter
def H_digital(b, a, f): return freqz(b, a, worN=2*np.pi*f/fs)[1]
# Derived digital IIR filter coefficients
def H_digital_coefficients(alpha):
     B0 = (beta*T + 2*alpha) / (beta*T + 2)
     B1 = (beta*T - 2*alpha) / (beta*T + 2)
     A1 = (beta*T - 2)       / (beta*T + 2)
     return [B0, B1], A1

# Task 2
def delta_t_samples(theta): return np.round(a/c*(theta + np.sin(theta))*fs)  # Time delay between ears

# Delivery plot: Impulse response of one L/R channel for -60 degrees
def plot_impulse_response(theta):
     # Calculate alpha for left and right ears
     alpha_L, alpha_R = alpha_LR(theta)
     #
     # Get digital filter coefficients for left and right ears
     b_L, a_L = H_digital_coefficients(alpha_L)
     b_R, a_R = H_digital_coefficients(alpha_R)
     #
     # Integer sample delays: shadow ear later, sunny ear earlier.
     # Constant offset N0 (same for both ears) keeps the delays non-negative.
     N0 = int(np.ceil(delta_t_samples(np.pi/2)))   # largest possible delay (at 90 deg)
     d = int(np.round(delta_t_samples(theta)))     # positive = source to the right
     delay_L = N0 + d
     delay_R = N0 - d
     #
     # Put each impulse at its delay
     impulse_L = np.zeros(1024); impulse_L[delay_L] = 1
     impulse_R = np.zeros(1024); impulse_R[delay_R] = 1
     #
     # Full IIR filter: numerator b and denominator [1, A1]
     h_L = lfilter(b_L, [1, a_L], impulse_L)
     h_R = lfilter(b_R, [1, a_R], impulse_R)
     #
     # Plot the impulse responses
     plt.figure(figsize=(12, 6))
     plt.plot(h_L, label='Left Ear', color='b')
     plt.plot(h_R, label='Right Ear', color='r')
     plt.title('Impulse Response - Left Ear (-60 degrees)')
     plt.xlabel('Samples')
     plt.ylabel('Amplitude')
     plt.xlim(0, 100)  # Limit x-axis to first 100 samples for better visibility
     plt.grid()
     plt.legend()
     #
     plt.show()

#plot_impulse_response(theta)

def pink_noise(N):
     # Generate white noise
     white_noise = np.random.randn(N)
     #
     # Apply a simple filter to approximate pink noise
     b = [0.049922035, 0.095993537, 0.050612699, -0.004408786]
     a = [1, -2.494956002, 2.017265875, -0.522189400]
     pink_noise = lfilter(b, a, white_noise)[:N]
     #
     return pink_noise

def moving_source_sound_file(step_deg=30, burst_s=0.25, gap_s=0.10, filename='dem1.wav'):
     # Noise bursts that step around the head in increments of step_deg,
     # starting straight ahead (0 deg) and going once around (0, 30, ..., 330 deg).
     # Azimuth: 0 = front, +90 = right, 180 = behind, 270 = left.
     azimuths = np.arange(0, 360, step_deg)
     #
     N_burst = int(burst_s * fs)
     N_slot = int((burst_s + gap_s) * fs)          # time between burst starts
     N_pad = 2 * 1024                              # extra room for delay + filter tail
     N0 = int(np.ceil(delta_t_samples(np.pi/2)))   # same constant offset for all angles
     #
     # Short fade in/out on every burst to avoid clicks
     n_fade = int(0.01 * fs)
     window = np.ones(N_burst)
     window[:n_fade] = np.linspace(0, 1, n_fade)
     window[-n_fade:] = np.linspace(1, 0, n_fade)
     #
     stereo_signal = np.zeros((len(azimuths) * N_slot + N_pad, 2))
     #
     for k, az in enumerate(azimuths):
          # The model only covers -90..+90 deg (left/right), so front and back
          # positions get the same filters: theta = arcsin(sin(azimuth))
          theta_k = np.arcsin(np.sin(np.radians(az)))
          alpha_L, alpha_R = alpha_LR(theta_k)
          b_L, a_L = H_digital_coefficients(alpha_L)
          b_R, a_R = H_digital_coefficients(alpha_R)
          #
          # Integer sample delays (shadow ear later, sunny ear earlier)
          d = int(np.round(delta_t_samples(theta_k)))
          delay_L = N0 + d
          delay_R = N0 - d
          #
          # One noise burst, followed by zeros so the delay and filter tail are not cut off
          burst = pink_noise(N_burst) * window
          x = np.concatenate([burst, np.zeros(N_pad)])
          #
          # IIR filter, then delay by shifting the signal
          y_L = np.concatenate([np.zeros(delay_L), lfilter(b_L, [1, a_L], x)])[:len(x)]
          y_R = np.concatenate([np.zeros(delay_R), lfilter(b_R, [1, a_R], x)])[:len(x)]
          #
          # Add the burst into the output at its time slot
          start = k * N_slot
          stereo_signal[start:start + len(x), 0] += y_L
          stereo_signal[start:start + len(x), 1] += y_R
     #
     # Normalize the signal to prevent clipping
     stereo_signal /= np.max(np.abs(stereo_signal))
     #
     # Save the stereo signal as a WAV file
     wavfile.write(filename, fs, (stereo_signal * 32767).astype(np.int16))
     return stereo_signal

moving_source_sound_file()

# ---------------------------------------------------------------------------
# Task 4: Occlusion
# ---------------------------------------------------------------------------
# Analog occlusion filter: H_occ(s) = beta_occ / (s + beta_occ), beta_occ = 2*pi*fc
def H_occlusion_analog(fc, f): jw = 1j*2*np.pi*f; b_occ = 2*np.pi*fc; return b_occ/(jw + b_occ)

# Digital filter from the bilinear transform: B0 = B1 = bT/(bT+2), A1 = (bT-2)/(bT+2)
def occlusion_coefficients(fc):
     bT = 2*np.pi*fc*T
     B0 = bT / (bT + 2)
     B1 = bT / (bT + 2)
     A1 = (bT - 2) / (bT + 2)
     return [B0, B1], A1

# Delivery plot: frequency response of the occlusion filter
def plot_occlusion_response(fcs=(500, 2000)):
     f = np.logspace(np.log10(20), np.log10(20000), 1000)
     #
     plt.figure(figsize=(8, 5))
     for fc, color in zip(fcs, ['g', 'm', 'c', 'y']):
          b, a1 = occlusion_coefficients(fc)
          plt.semilogx(f, 20*np.log10(np.abs(H_occlusion_analog(fc, f))), color=color, lw=2, label=f'Analog, fc = {fc} Hz')
          plt.semilogx(f, 20*np.log10(np.abs(H_digital(b, [1, a1], f))), 'k--', lw=1, label='Digital' if fc == fcs[0] else None)
          plt.axvline(fc, color=color, alpha=0.3)
     plt.title('Occlusion filter frequency response')
     plt.xlabel('Frequency [Hz]')
     plt.ylabel('Magnitude [dB]')
     plt.ylim(-40, 3)
     plt.grid(True, which='both', alpha=0.3)
     plt.legend()
     plt.savefig('occlusion_frequency_response.png', dpi=150)
     plt.show()

# Delivery sound: Demonstration 2 (source 2 m in front + reflection from the same direction
# with a 0.5 m longer path), with the DIRECT sound occluded. fc=None gives the unoccluded reference.
# occlude_reflection=True occludes the reflection too (a much more clearly muffled result).
def occlusion_sound_file(fc=500, filename='occlusion_demo.wav', duration_s=3, occlude_reflection=False, source=None, save=True):
     r_direct, r_refl = 2.0, 2.5                      # path lengths in m
     N0 = int(np.ceil(delta_t_samples(np.pi/2)))      # same constant offset as elsewhere
     #
     # HRIR for a source straight ahead (theta = 0): same filter and delay for both ears
     alpha_L, alpha_R = alpha_LR(0.0)
     b_L, a_L = H_digital_coefficients(alpha_L)
     b_R, a_R = H_digital_coefficients(alpha_R)
     impulse = np.zeros(256); impulse[N0] = 1
     h_L = lfilter(b_L, [1, a_L], impulse)
     h_R = lfilter(b_R, [1, a_R], impulse)
     #
     source = pink_noise(duration_s * fs) if source is None else source
     #
     # Occlude the source signal before it goes through the direct-path HRIR/delay
     source_refl = source
     if fc is None:
          source_direct = source
     else:
          b_occ, a_occ = occlusion_coefficients(fc)
          source_direct = lfilter(b_occ, [1, a_occ], source)
          source_refl = source_direct if occlude_reflection else source
     #
     # Time of flight (samples) and 1/r amplitude for the two paths
     d_direct = int(np.round(r_direct / c * fs))
     d_refl = int(np.round(r_refl / c * fs))
     #
     N_out = len(source) + d_refl + len(h_L) - 1
     stereo_signal = np.zeros((N_out, 2))
     for ch, h in enumerate([h_L, h_R]):
          y_direct = np.convolve(source_direct, h) / r_direct       # direct (occluded)
          y_refl = np.convolve(source_refl, h) / r_refl             # reflection
          stereo_signal[d_direct:d_direct + len(y_direct), ch] += y_direct
          stereo_signal[d_refl:d_refl + len(y_refl), ch] += y_refl
     #
     stereo_signal /= np.max(np.abs(stereo_signal))
     wavfile.write(filename, fs, (stereo_signal * 32767).astype(np.int16))
     return stereo_signal

def occlusion_comparison_file(fc=500, filename='occlusion_comparison.wav', duration_s=3, gap_s=1, occlude_reflection=True):
     # Same noise in both parts, and one common normalization, so the level
     # and spectral differences caused by the occlusion are preserved
     source = pink_noise(duration_s * fs)
     reference = occlusion_sound_file(fc=None, duration_s=duration_s, source=source, save=False)
     occluded = occlusion_sound_file(fc=fc, duration_s=duration_s, occlude_reflection=occlude_reflection, source=source, save=False)
     #
     gap = np.zeros((int(gap_s * fs), 2))
     stereo_signal = np.concatenate([reference, gap, occluded])
     stereo_signal /= np.max(np.abs(stereo_signal))
     wavfile.write(filename, fs, (stereo_signal * 32767).astype(np.int16))
     return stereo_signal

plot_occlusion_response()
occlusion_comparison_file(fc=500, filename='occlusion_demo.wav', occlude_reflection=True)
occlusion_sound_file(fc=None, filename='occlusion_demo_reference.wav')
#occlusion_sound_file(fc=500, filename='occlusion_demo_fc500.wav')
#occlusion_sound_file(fc=500, filename='occlusion_demo_fc500_both.wav', occlude_reflection=True)
#occlusion_sound_file(fc=2000, filename='occlusion_demo_fc2000.wav')

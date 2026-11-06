import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

f_0 = 10_000 # cutoff frequency for the low-pass filter
f_s = 48_000 # sampling frequency

B = f_0 / (f_0 + f_s/np.pi)
A_1 = (np.pi*f_0 - f_s) / (np.pi*f_0 + f_s)

f, h_digital = freqz([B, B], [1, A_1], fs=f_s)

h_analog = 1 / (1 + 1j * f / f_0)

plt.plot(f, 20 * np.log10(np.abs(h_digital)), label='Digital Filter', color='blue')
plt.plot(f, 20 * np.log10(np.abs(h_analog)), label='Analog Filter', color='red', linestyle='--')
plt.xlabel('Frequency [Hz]'); plt.ylabel('Magnitude [dB]')
plt.xscale('log'); plt.xlim(1_000, f_s/2);  plt.ylim(-30, 5)
plt.title('Low-Pass Filter: Digital vs Analog Frequency Response')
plt.grid(True); plt.legend()
plt.savefig('Exercises/exercise4/digital_LPF_FR.pdf'); plt.show()

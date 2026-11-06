import numpy as np
from numpy.random import randn 
import matplotlib.pyplot as plt
from scipy.signal import freqz

# Number of iterations for the LMS filter
N = 1000
# True filter coefficients
h_true = np.array([1, 0.2])

# Function definition for the LMS filter
# I use some predefined h since it gets adjusted on the go. alpha 0.5 was starting point
def LMS_filter(x, y_true, h=np.array([0.0, 0.0], dtype=float), alpha=0.5):
     N = len(y_true)
     error_history = np.zeros(N)
     
     # Initialize the first error and update the first filter coefficient
     error_history[0] = y_true[0] - h[0]*x[0]
     h[0] += alpha * error_history[0] * x[0]
     for n in range(1,N):
          x_prev = x[n-1] 

          # Calculate prediction of y with the current coefficients
          y_pred = h[0]*x[n] + h[1]*x_prev

          # Add error to error_history for this sample
          error_history[n] = y_true[n] - y_pred

          # Calculate updated h_0 adn h_1 using that error and the same inputs
          h[0] += alpha * error_history[n] * x[n]
          h[1] += alpha * error_history[n] * x_prev
     return error_history

# Generate random input and output signals
x = randn(1, N)[0, :]
y_true = np.convolve(x, h_true)[:len(x)]
print(x[2], h_true.shape, y_true.shape)
# Get the error history from the LMS filter
error_history = LMS_filter(x, y_true, alpha=0.5)

# Plot the error history
plt.plot(range(N), np.abs(error_history))
plt.title('Error History'); plt.xlabel('Iteration'); plt.ylabel('Error Magnitude')
plt.grid(True); plt.savefig('Exercises/exercise4/LMS_error_history_too_high_alpha.pdf')
plt.show()
import librosa
import pywt
import numpy as np
from scipy.io.wavfile import write

# Load audio file
file_path = './../orig_audio/loudnoise.wav'  
data, fs = librosa.load(file_path, sr=None)

def wavelet_denoise(data, wavelet='db4', level=3):
    # Perform wavelet decomposition
    coeff = pywt.wavedec(data, wavelet, mode='per', level=level)

    # Estimate noise using the median absolute deviation on the smallest detail coefficients
    sigma = np.median(np.abs(coeff[-level])) / 0.6745
    uthresh = sigma * np.sqrt(2 * np.log(len(data)))

    # Apply soft thresholding to detail coefficients only (skip the approximation coefficients)
    denoised_coeff = [coeff[0]]  # Keep the approximation coefficients (first element) unmodified
    denoised_coeff += [pywt.threshold(c, value=uthresh, mode='soft') for c in coeff[1:]]

    # Reconstruct the signal from the thresholded coefficients
    denoised_signal = pywt.waverec(denoised_coeff, wavelet, mode='per')

    # Ensure the reconstructed signal has the same length as the original signal
    if len(denoised_signal) > len(data):
        denoised_signal = denoised_signal[:len(data)]
    elif len(denoised_signal) < len(data):
        padding = np.zeros(len(data) - len(denoised_signal))
        denoised_signal = np.concatenate([denoised_signal, padding])
    
    return denoised_signal

# Apply wavelet denoising
denoised_data = wavelet_denoise(data, wavelet='db4', level=3)

# Save the denoised signal to a new WAV file
output_path = 'denoised_loud_heart_sound.wav'
write(output_path, fs, (denoised_data * 32767).astype(np.int16))  # Rescale to 16-bit PCM format

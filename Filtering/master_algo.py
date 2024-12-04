import requests
url = "http://esp32fs.local/download"
response = requests.get(url)
with open("recording.raw", "wb") as f:
    f.write(response.content)

print("received raw file")

import numpy as np
import wave

rawfname = "recording.raw"
wav_savefname = "recording.wav"
sr = 16000

def read_raw_audio(file_path):
    with open(file_path, 'rb') as raw_file:
        raw_data = raw_file.read()
    return np.frombuffer(raw_data, dtype=np.int16)

def save_wav_audio(audio_data, sample_rate, output_path):
    with wave.open(output_path, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono channel
        wav_file.setsampwidth(2)  # 16-bit samples
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.astype(np.int16).tobytes())

audio = read_raw_audio(rawfname)
save_wav_audio(audio, sr, wav_savefname)

print("converted to wav")

import librosa
import pywt
import soundfile as sf
from scipy.signal import butter, lfilter
import noisereduce as nr
from scipy.io.wavfile import write

# Sample rate and cutoff frequencies 
fs = 16000.0
lowcut = 200.0
highcut = 800.0

input_file_path = 'recording.wav'
data, sr = librosa.load(input_file_path, sr=None, mono=True)

# Butterworth bandpass filter
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Apply bandpass filter
filtered_data = butter_bandpass_filter(data, lowcut, highcut, fs, order=6)

def wavelet_denoise(data, wavelet='db4', level=3):
    coeff = pywt.wavedec(data, wavelet, mode='per', level=level)
    sigma = np.median(np.abs(coeff[-level])) / 0.6745
    uthresh = sigma * np.sqrt(2 * np.log(len(data)))
    denoised_coeff = [coeff[0]]
    denoised_coeff += [pywt.threshold(c, value=uthresh, mode='soft') for c in coeff[1:]]
    denoised_signal = pywt.waverec(denoised_coeff, wavelet, mode='per')

    if len(denoised_signal) > len(data):
        denoised_signal = denoised_signal[:len(data)]
    elif len(denoised_signal) < len(data):
        padding = np.zeros(len(data) - len(denoised_signal))
        denoised_signal = np.concatenate([denoised_signal, padding])

    return denoised_signal

# Apply wavelet denoising
denoised_data = wavelet_denoise(filtered_data, wavelet='db4', level=3)

def spectral_gating(data, sr):
    reduced_noise_signal = nr.reduce_noise(y=data, sr=sr)
    return reduced_noise_signal

# Apply spectral gating
noise_reduced_data = spectral_gating(denoised_data, sr)

# Amplification
amplification_factor = 10
amplified_data = noise_reduced_data * amplification_factor

# Ensure that the values don't exceed the valid range [-1, 1]
final_output = np.clip(amplified_data, -1.0, 1.0)

output_file_path = 'recording_filtered_output.wav'
sf.write(output_file_path, final_output, sr)

print(f"Final filtered and amplified audio saved to: {output_file_path}")

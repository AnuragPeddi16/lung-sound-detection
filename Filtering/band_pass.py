from scipy.signal import butter, lfilter

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

import numpy as np
import librosa
import soundfile as sf

# Sample rate and desired cutoff frequencies (in Hz).
fs = 16000.0
lowcut = 100.0
highcut = 1000.0

noise, samplerate = librosa.load('loudnoise.wav', sr=None) # input filename

y = butter_bandpass_filter(noise, lowcut, highcut, fs, order=6)
print(len(y))
print(y)

sf.write('loud.wav', y, samplerate=samplerate) # output filename

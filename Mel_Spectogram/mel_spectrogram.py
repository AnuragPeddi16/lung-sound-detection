import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

file_path = 'denoised_medium_heart_sound.wav'  
data, sr = librosa.load(file_path, sr=None)

# the Mel spectrogram
S = librosa.feature.melspectrogram(y=data, sr=sr, n_mels=128, fmax=8000)

# Convert to dB (log scale)
S_dB = librosa.power_to_db(S, ref=np.max)

# Plot the Mel spectrogram
plt.figure(figsize=(10, 6))
librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel', fmax=8000, cmap='coolwarm')
plt.colorbar(format='%+2.0f dB')
plt.title('Mel Spectrogram')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.tight_layout()
# plt.show()

plt.savefig('mel_spectrogram.png')

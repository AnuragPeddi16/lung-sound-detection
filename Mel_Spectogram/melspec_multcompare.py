import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def plot_mel_spectrogram(ax, data, sr, title, fmax=8000):
    # Compute the Mel spectrogram
    S = librosa.feature.melspectrogram(y=data, sr=sr, n_mels=128, fmax=fmax)
    # Convert to dB (log scale)
    S_dB = librosa.power_to_db(S, ref=np.max)
    
    # Plot the Mel spectrogram
    img = librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel', fmax=fmax, cmap='coolwarm', ax=ax)
    ax.set_title(title)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')
    ax.label_outer()

    return img

# Load audio files accordingly
file_path1 = './../orig_audio/loudnoise.wav'  
file_path2 = './../wavelet_transform/denoised_loud_heart_sound.wav'  
file_path3 = './../bandpass/loud_filtered.wav'
file_path4 = './../spectral_gating/gated_output_loud.wav'

data1, sr1 = librosa.load(file_path1, sr=None)
data2, sr2 = librosa.load(file_path2, sr=None)
data3, sr3 = librosa.load(file_path3, sr=None)
data4, sr4 = librosa.load(file_path4, sr=None)

# Create a figure with four subplots
fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(20, 6), sharex=True, sharey=True)

# Plot Mel spectrograms for all four audio files
img1 = plot_mel_spectrogram(ax1, data1, sr1, 'Mel Spectrogram - Medium Noisy')
img2 = plot_mel_spectrogram(ax2, data2, sr2, 'Mel Spectrogram - Wavelet Filtered')
img3 = plot_mel_spectrogram(ax3, data3, sr3, 'Mel Spectrogram - Bandpass Filtered')
img4 = plot_mel_spectrogram(ax4, data4, sr4, 'Mel Spectrogram - Spectral gating Filtered')

# Adjust the space between the plots and the right edge of the figure
plt.subplots_adjust(right=0.85)

# Add a colorbar on the extreme right
cbar_ax = fig.add_axes([0.87, 0.15, 0.03, 0.7])  # [left, bottom, width, height]
fig.colorbar(img1, cax=cbar_ax, format='%+2.0f dB')

# Save the figure as a PNG file
plt.savefig('comparison_mel_spectrogram_loud.png')

# Optionally display the plot
# plt.show()

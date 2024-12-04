import librosa
import noisereduce as nr
from scipy.io.wavfile import write

def load_audio(file_path):
    y, sr = librosa.load(file_path, sr=None) 
    return y, sr

def save_audio(file_path, audio_data, sr):
    write(file_path, sr, (audio_data * 32767).astype('int16'))

def process_audio_spectral_gating(input_file, output_file):
    y, sr = load_audio(input_file)

    reduced_noise_signal = nr.reduce_noise(y=y, sr=sr)

    save_audio(output_file, reduced_noise_signal, sr)
    print(f"Processed audio saved to {output_file}")

# Example usage
input_file = 'loudnoise.wav'
output_file = 'gated_output_loud.wav'

process_audio_spectral_gating(input_file, output_file)

import numpy as np
import librosa
from tensorflow.keras.models import load_model  # Updated import path for TensorFlow 2.x

def extract_mel_spectrogram(file_path):
    y, sr = librosa.load(file_path, sr=None)
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    log_mel_spectrogram = librosa.power_to_db(mel_spectrogram)
    return log_mel_spectrogram

def pad_spectrogram(mel_spectrogram, max_len):
    if mel_spectrogram.shape[1] < max_len:
        pad_width = max_len - mel_spectrogram.shape[1]
        mel_spectrogram = np.pad(mel_spectrogram, ((0, 0), (0, pad_width)), mode='constant')
    else:
        mel_spectrogram = mel_spectrogram[:, :max_len]
    return mel_spectrogram

class_mapping = {
    'Normal': 0,
    'Wheezing': 1,
    'Crackling': 2,
    'Both': 3
}
reverse_class_mapping = {v: k for k, v in class_mapping.items()}

def predict_class_cnn(file_path, max_len=250):
    # Load the saved model
    model = load_model('./lung_sound_cnn_model.h5')

    # Process the audio file
    mel_spec = extract_mel_spectrogram(file_path)
    padded_mel_spec = pad_spectrogram(mel_spec, max_len)
    padded_mel_spec = np.expand_dims(padded_mel_spec, axis=-1)  # Add channel dimension
    padded_mel_spec = np.expand_dims(padded_mel_spec, axis=0)   # Add batch dimension

    # Make prediction
    predictions = model.predict(padded_mel_spec)
    predicted_class_index = int(np.argmax(predictions, axis=1)[0])  # Ensure int type
    predicted_class = str(reverse_class_mapping[predicted_class_index])  # Ensure str type
    confidence = float(predictions[0][predicted_class_index])  # Convert to float for JSON
    confidence *= 100  # Convert to percentage
    confidence = np.floor(confidence)  # Round down to nearest integer
    return [predicted_class, confidence]


if __name__ == "__main__":
    # Example usage
    new_audio_file_path = '/home/karthik/lung_sound_recorder/SVM_Model/AudioFiles/BP1_Asthma,I E W,P L L,70,M.wav'
    predicted_label = predict_class_cnn(new_audio_file_path)

    print(f"The predicted label for the audio file is: {predicted_label[0]} with confidence {predicted_label[1]:.2f}")

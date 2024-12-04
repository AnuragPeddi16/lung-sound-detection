import os
import numpy as np
import librosa
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

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

# Directory containing your audio files
data_dir = './Audio_Files' 
labels = []
mel_spectrograms = []

class_mapping = {
    'Normal': 0,
    'Wheezing': 1,
    'Crackle': 2,
    'Both': 3
}

count1 = 0
count2 = 0
count3 = 0
count4 = 0


# Load data
for file in os.listdir(data_dir):
    if file.endswith('.wav'):
        file_path = os.path.join(data_dir, file)
        mel_spec = extract_mel_spectrogram(file_path)
        mel_spectrograms.append(mel_spec)
        
        # Determine the label based on the file name
        
        label = "Normal"
        if "W," in file_path or ' W' in file_path:
            if "C," in file_path or 'C ' in file_path:
                label = "Both"
                count4 = count4 + 1
                print(file_path)
                
            else:
                label = "Wheezing"
                count3 = count3 + 1
        elif "C," in file_path or 'C ' in file_path:
            label = "Crackle"
            count2 = count2 + 1
        else:
            count1 = count1 + 1
        labels.append(class_mapping[label])



# Prepare data for training
max_len = 250
mel_spectrograms_padded = [pad_spectrogram(mel_spec, max_len) for mel_spec in mel_spectrograms]
X_padded = np.array(mel_spectrograms_padded)[..., np.newaxis]  # Add channel dimension
y = np.array(labels)

# Split into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X_padded, y, test_size=0.2, random_state=32)

# Create CNN model
def create_cnn_model(input_shape, num_classes):
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    return model

input_shape = (X_padded.shape[1], X_padded.shape[2], 1)
num_classes = len(class_mapping)

model = create_cnn_model(input_shape, num_classes)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=10, batch_size=32)

# Evaluate the model
loss, accuracy = model.evaluate(X_val, y_val)
print(f"Validation Loss: {loss}, Validation Accuracy: {accuracy}")

# Predictions
y_pred = model.predict(X_val)
y_pred_classes = np.argmax(y_pred, axis=1)

# Check unique classes in validation set
unique_classes = np.unique(y_val)
target_names = [list(class_mapping.keys())[i] for i in unique_classes]
print("Unique classes in y_val:", np.unique(y_val))

# Classification Report
print("\nClassification Report:")
print(classification_report(y_val, y_pred_classes, labels=unique_classes, target_names=target_names))

# Confusion Matrix
conf_matrix = confusion_matrix(y_val, y_pred_classes, labels=unique_classes)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=target_names, yticklabels=target_names)
plt.title('Confusion Matrix')
plt.xlabel('Predicted Class')
plt.ylabel('True Class')
plt.show()

print(count1)
print(count2)
print(count3)
print(count4)


# Save the trained model
model.save('lung_sound_cnn_model.h5')
print("Model saved as lung_sound_cnn_model.h5")

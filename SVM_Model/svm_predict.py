import librosa
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder

import pickle

# Function to extract MFCC features from an audio file
def extract_features(audio_file, max_length):
    y, sr = librosa.load(audio_file, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
    zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y=y))
    
    if mfccs.shape[1] < max_length:
        pad_width = max_length - mfccs.shape[1]
        mfccs = np.pad(mfccs, ((0, 0), (0, pad_width)), mode='constant')
    else:
        mfccs = mfccs[:, :max_length]
        
    return np.concatenate((mfccs.flatten(), [spectral_centroid, spectral_bandwidth, zero_crossing_rate]))

def predict_class_svm(file_path):

    mfcc_features = extract_features(file_path, 7500)
    X = np.array([mfcc_features])

    path = '../SVM_Model/'

    with open(path + 'svm_model.pkl', 'rb') as f:
        model = pickle.load(f)

    class_mapping = {
    'Normal': 0,
    'Wheezing': 1,
    'Crackling': 2,
    'Both': 3
    }

    """ class_mapping = {
    'Normal': 1,
    'Wheezing': 2,
    'Crackling': 0,
    'Both': 3
    } """
    reverse_class_mapping = {v: k for k, v in class_mapping.items()}

    y_pred = model.predict(X)
    y = reverse_class_mapping[y_pred[0]]

    confidence = model.predict_proba(X).max()
    confidence *= 100
    confidence = np.floor([confidence])[0]

    return [y, confidence]

if __name__ == "__main__":
    print(predict_class_svm('./AudioFiles/BP1_Asthma,I E W,P L L,70,M.wav'))

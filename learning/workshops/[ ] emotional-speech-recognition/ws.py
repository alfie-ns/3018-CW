from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import numpy as np
import os
import glob
import librosa
import kagglehub
import soundfile

path = kagglehub.dataset_download("uwrfkaggler/ravdess-emotional-speech-audio")

emotions = { # dict of different emotions
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'
}

observed_emotions = ['calm', 'happy', 'fearful', 'disgust']

def extract_features(file_name, mfcc=True, chroma=True, mel=True): 
    with soundfile.SoundFile(file_name) as sound_file: # extract files from read sound file
        X = sound_file.read(dtype='float32') # convert sound file to float32
        sample_rate = sound_file.samplerate # extract sample rate from sound file
        if len(X.shape) > 1: # if the sound file has more than one channel, take the mean of the channels to convert it to mono (single channel)
            X = np.mean(X, axis=1) # convert to mono by taking the mean of the channels/columns

        result = np.array([]) # init result array
        stft = None # init stft variable as nothing; used for chroma features, which require the short-time Fourier transform (STFT) of the audio signal

        #Extract all average features and concatenate them into 'result' array
        '''
        chroma_stft: capture intensity of each of the 12 different pitch classes (C, C#, D, D#, E, F, F#, G, G#, A, A#, B) in the audio signal; capture harmonic and melodic characteristics of music and speech
        mfcc: Mel-frequency Cepstral Coefficients: capture broad spectral characteristics of audio signals to capture broad 
        melspectrogram: capture how energy is distributed across meaningful frequency bands
        '''
        if chroma:
            stft = np.abs(librosa.stft(X))

        if mfcc:
            mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            result = np.hstack((result, mfccs))

        if chroma:
            chroma_features = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
            result = np.hstack((result, chroma_features))

        if mel:
            mel_features = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T, axis=0)
            result = np.hstack((result, mel_features))

    return result

def load_data(test_size=0.25):
    x, y = [], []

    pattern = os.path.join(path, '**', '*.wav') # match ANY subdirectory (**) .wav files in the dataset directory and its subdirectories

    for file_name in glob.glob(pattern, recursive=True): # glob.glob() returns a list of file paths that match the specified pattern; recursive=True allows for searching through subdirectories
        base_name = os.path.basename(file_name)
        parts = base_name.split('-')

        if len(parts) < 3:
            continue

        emotion_code = parts[2] # extract emotion code from third part of the file name
        emotion = emotions.get(emotion_code)

        if emotion not in observed_emotions: 
            continue

        feature = extract_features(file_name, mfcc=True, chroma=True, mel=True) # extract features from the audio file using the extract_features function; specify which features to extract (MFCC, chroma, and mel spectrogram)
        x.append(feature)
        y.append(emotion)

    return train_test_split(np.array(x), y, test_size=test_size, random_state=9) # split the dataset into training and testing sets; test_size=0.25 means 25% of the data will be used for testing; random_state=9 ensures reproducibility of the split

X_train, X_test, y_train, y_test = load_data(test_size=0.25)

print(f'Training samples: {len(X_train)}')
print(f'Test samples: {len(X_test)}') 

model = MLPClassifier( # create MLPClassifier model with specified parameters
    alpha=0.01, # prevent overfitting due to penalty term 
    batch_size=256, # size of mini-batches for stochastic optimizers
    epsilon=1e-08, # term added to improve numerical stability
    hidden_layer_sizes=(300,), # number of neurons in the hidden layers
    learning_rate='adaptive', # learning rate schedule for weight updates
    max_iter=500 # maximum number of iterations
)

model.fit(X_train, y_train) # train the model on the training data (X_train; y_train)

y_pred = model.predict(X_test) # store x_test predictions in y_pred

accuracy = accuracy_score(y_true=y_test, y_pred=y_pred) # accuracy = number of correct predictions / total number of predictions
cm = confusion_matrix(y_test, y_pred) # confusion matrix = table used to describe the performance of a classification model

print(f'Correctly classified: {accuracy * 100:.4f}% of {len(y_test)} samples') # output 4-decimal accuracy score
# print(f'Confusion matrix: \n {cm}') output confusion matrix

labels = model.classes_

print("\nConfusion matrix:")
print("Actual \\ Predicted ->", labels)
print("Note in the confusion")

for i, row in enumerate(cm):
    print(f"{labels[i]:<10} {row}")
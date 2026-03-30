"""
Train the speech emotion MLP (WS-08) and save it for GAZE.

Run once to produce speech_emotion_model.pkl, which gaze.py loads at startup.
Uses the RAVDESS dataset via kagglehub and the same feature pipeline from WS-08.
"""

# stdlib
import os, glob

# data
import numpy as np
import soundfile as sf
import librosa

# ML
import joblib
import kagglehub
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

# ── emotion mapping (RAVDESS filename convention) ──

EMOTIONS = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised',
}

OBSERVED = ['calm', 'happy', 'fearful', 'disgust']

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "speech_emotion_model.pkl")


# ── feature extraction (identical to WS-08) ──

def extract_features(file_name: str):
    """Extract MFCC (40) + chroma (12) + mel spectrogram (128) = 180 features."""
    with sf.SoundFile(file_name) as sound_file:
        audio = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate

    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    n_fft = 2048
    if len(audio) < n_fft:
        return None

    stft   = np.abs(librosa.stft(audio, n_fft=n_fft))
    mfccs  = np.mean(librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40).T, axis=0).flatten()
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0).flatten()
    mel    = np.mean(librosa.feature.melspectrogram(y=audio, sr=sample_rate).T, axis=0).flatten()

    return np.concatenate([mfccs, chroma, mel])


# ── data loading ──

def load_data(dataset_path: str):
    X, y = [], []
    for file in glob.glob(dataset_path):
        parts = os.path.basename(file).split("-")
        if len(parts) < 3:
            continue
        emotion = EMOTIONS.get(parts[2])
        if emotion not in OBSERVED:
            continue
        features = extract_features(file)
        if features is None:
            continue
        if X and features.shape != X[0].shape:
            continue
        X.append(features)
        y.append(emotion)
    return np.array(X), y


# ── main ──

if __name__ == "__main__":
    print("Downloading RAVDESS dataset...")
    dataset_dir = kagglehub.dataset_download("uwrfkaggler/ravdess-emotional-speech-audio")
    dataset_path = os.path.join(dataset_dir, "**", "Actor_*", "*.wav")

    # fallback: try without the extra nesting
    if not glob.glob(dataset_path, recursive=True):
        dataset_path = os.path.join(dataset_dir, "Actor_*", "*.wav")

    print(f"Dataset pattern: {dataset_path}")
    print("\nExtracting features...")
    X, y = load_data(dataset_path)
    print(f"  Samples: {len(y)}  |  Features: {X.shape[1] if len(X) else 0}")
    print(f"  Labels: { {e: y.count(e) for e in OBSERVED} }")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    print(f"\nTraining MLP ({len(X_train)} train / {len(X_test)} test)...")
    model = MLPClassifier(
        alpha=0.01,
        batch_size=256,
        epsilon=1e-08,
        hidden_layer_sizes=(300,),
        learning_rate='adaptive',
        max_iter=500,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {acc * 100:.2f}%")
    print(f"Confusion matrix:\n{confusion_matrix(y_test, y_pred, labels=OBSERVED)}")

    joblib.dump(model, OUTPUT_PATH)
    print(f"\nModel saved to {OUTPUT_PATH}")
    print("gaze.py will load this automatically on next run.")

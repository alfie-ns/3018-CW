#!/usr/bin/env bash
# Run gaze.py in local mode (no Pepper required).
# Uses Mac webcam, mic, and TTS instead.

set -euo pipefail
cd "$(dirname "$0")"

export GAZE_LOCAL_MODE=true
export GAZE_LOCAL_CAMERA=true

# load .env for OPENAI_API_KEY
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

# override back to local mode (in case .env has false)
export GAZE_LOCAL_MODE=true
export GAZE_LOCAL_CAMERA=true

if [ -z "${OPENAI_API_KEY:-}" ]; then
    echo "ERROR: OPENAI_API_KEY is not set. Add it to .env"
    exit 1
fi

# check speech model exists
if [ ! -f speech_emotion_model.pkl ]; then
    echo "Speech emotion model not found. Training it now..."
    python train_speech_model.py
fi

python gaze.py

#!/usr/bin/env bash
# Run gaze.py in local mode (no Pepper required).
# Uses Mac webcam, mic, and TTS instead.

cd "$(dirname "$0")"
rm -rf __pycache__

export GAZE_LOCAL_MODE=true
export GAZE_LOCAL_CAMERA=true

if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

export GAZE_LOCAL_MODE=true
export GAZE_LOCAL_CAMERA=true

if [ -z "${OPENAI_API_KEY:-}" ]; then
    echo "ERROR: OPENAI_API_KEY is not set. Add it to .env"
    exit 1
fi

if [ ! -f speech_emotion_model.pkl ]; then
    echo "Speech emotion model not found. Training it now..."
    python "[ ]-gaze-train_speech_model.py"
fi

cleanup() {
    pkill -9 -f "python.*gaze" 2>/dev/null
    pkill -9 -f "test-gaze" 2>/dev/null
    echo ""
    echo "GAZE killed."
    exit 0
}
trap cleanup INT TERM

python -u gaze.py &
wait $!

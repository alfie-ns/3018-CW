#!/usr/bin/env bash
# Run gaze.py in local mode (no Pepper required).
# Uses Mac webcam, mic, and TTS instead.

cd "$(dirname "$0")"
rm -rf __pycache__

# resolve the Semester 2 .venv regardless of where the script lives
VENV_PYTHON="$(cd ../../../.. && pwd)/.venv/bin/python"
if [ ! -x "$VENV_PYTHON" ]; then
    echo "ERROR: cannot find .venv python at $VENV_PYTHON"
    exit 1
fi

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
    "$VENV_PYTHON" train_speech_model.py
fi

cleanup() {
    pkill -9 -f "python.*gaze" 2>/dev/null
    pkill -9 -f "test-gaze" 2>/dev/null
    echo ""
    echo "GAZE killed."
    exit 0
}
trap cleanup INT TERM

"$VENV_PYTHON" -u gaze.py &
wait $!

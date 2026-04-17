#!/usr/bin/env bash
# Run gaze.py in local mode (no Pepper required).
# Uses Mac webcam, mic, and TTS instead.

cd "$(dirname "$0")"
rm -rf __pycache__

exec > >(tee test-run.log) 2>&1

# find Python: local .venv -> repo-level .venv -> system python3
if [ -x ".venv/bin/python" ]; then
    VENV_PYTHON=".venv/bin/python"
elif [ -x "$(cd ../../../.. 2>/dev/null && pwd)/.venv/bin/python" ]; then
    VENV_PYTHON="$(cd ../../../.. && pwd)/.venv/bin/python"
elif command -v python3 &>/dev/null; then
    VENV_PYTHON="python3"
else
    echo "ERROR: No Python found. Create a venv: python3 -m venv .venv"
    exit 1
fi

echo "Using Python: $VENV_PYTHON"

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

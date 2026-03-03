"""
TODO

- [X] thershold for when to respond like if its loud enough
- [X] can be interrupted 
- [X] get connected to openai api
- [X] make web-search capabilities
- [X] make vision capabilities  
- [X] capability to fetch time and date if the AI determines its useful, encode this ability into system prompt 
- [X] eye contact when it speak, face recognition 
- [X] move hand to wave
- [X] make remember what someone likes 
- [X] allow to be cut off when spoken 
- [X] fix the timeout issue
- [X] stop talking for 0.5 sec if go onto new line 
- [X] utilise code for lights, animations, etc from Choerograph
- [X] only turn off just if googbye is said or said first 
- [X] configure to be able to change make based on what tge user says it is
- [X] when you say it's name it looks like you
"""


import os
import json
import time
import wave
import struct
import base64
import tempfile
import threading
import datetime
import paramiko
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

## Configuration ##

NAO_IP       = os.getenv("NAO_IP", "ROBOT's IP ADDRESS")
NAO_USER     = "nao"
NAO_PASS     = "nao"
RECORD_SECS  = 5
REMOTE_WAV   = "/var/persistent/home/nao/input.wav"
REMOTE_IMG   = "/var/persistent/home/nao/capture.jpg"
LOCAL_WAV    = os.path.join(tempfile.gettempdir(), "nao_input.wav")
LOCAL_IMG    = os.path.join(tempfile.gettempdir(), "nao_capture.jpg")
MEMORY_FILE  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "robot_memory.json")
VOLUME_THRESHOLD = 500   # rms energy threshold (increases ignores more background noise)
SSH_TIMEOUT  = 10 # seconds for the initial ssh handshake
CMD_TIMEOUT  = 60 # seconds for each remote command

client = OpenAI()

## initial mutable global state ##

robot_name         = os.getenv("ROBOT_NAME", "nao")
is_speaking        = False
speech_interrupted = False

## openai function-calling (https://developers.openai.com/api/docs/guides/function-calling/)  ##
TOOLS = [
    {"type": "function", "function": {
        "name": "web_search",
        "description": "search the web for current information.",
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string", "description": "search query"}
        }, "required": ["query"]}
    }},
    {"type": "function", "function": {
        "name": "get_time_date",
        "description": "return the current local time and date.",
        "parameters": {"type": "object", "properties": {}}
    }},
    {"type": "function", "function": {
        "name": "describe_vision",
        "description": "use your camera to see and describe what is in front of you.",
        "parameters": {"type": "object", "properties": {}}
    }},
    {"type": "function", "function": {
        "name": "remember_preference",
        "description": "remember a fact or preference about a person.",
        "parameters": {"type": "object", "properties": {
            "person": {"type": "string"},
            "key":    {"type": "string", "description": "category (e.g. favourite_colour)"},
            "value":  {"type": "string"}
        }, "required": ["person", "key", "value"]}
    }},
    {"type": "function", "function": {
        "name": "recall_preferences",
        "description": "recall everything remembered about a person.",
        "parameters": {"type": "object", "properties": {
            "person": {"type": "string"}
        }, "required": ["person"]}
    }},
    {"type": "function", "function": {
        "name": "change_name",
        "description": "change your own name when the user asks you to.",
        "parameters": {"type": "object", "properties": {
            "new_name": {"type": "string"}
        }, "required": ["new_name"]}
    }},
]

## Dynamically-constructed system prompt ##

def _system_prompt():
    return (
        f"You are a NAO humanoid robot named '{robot_name}'. "
        "You are a friendly, assistive companion. Respond concisely in 1-2 short sentences. "
        f"Only reply if the user mentions your name ('{robot_name}') first. "
        "You can call these tools when appropriate: "
        "web_search, get_time_date, describe_vision, remember_preference, "
        "recall_preferences, change_name. "
        "separate distinct thoughts onto new lines for natural speech pacing."
    )

messages = [{"role": "system", "content": _system_prompt()}]

## persistent memory ##

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as fh:
            return json.load(fh)
    return {}

def save_memory(mem):
    with open(MEMORY_FILE, "w") as fh:
        json.dump(mem, fh, indent=2)

## ssh helpers helper functions ##

def ssh_connect():
    """open an ssh connection to the nao robot."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(NAO_IP, username=NAO_USER, password=NAO_PASS, timeout=SSH_TIMEOUT)
    return ssh

def nao_run(ssh, code):
    """execute a python 2 snippet on the nao via ssh."""
    escaped = code.replace("'", "'\\''")
    _, stdout, _ = ssh.exec_command(f"python -c '{escaped}'", timeout=CMD_TIMEOUT)
    return stdout.read().decode().strip()

## nao robot capabilities ##

def nao_record(ssh):
    """record audio on the nao and sftp the wav file back."""
    nao_run(ssh, f"""
from naoqi import ALProxy
import time
r = ALProxy("ALAudioRecorder","127.0.0.1",9559)
r.stopMicrophonesRecording()
r.startMicrophonesRecording("{REMOTE_WAV}","wav",16000,[0,0,1,0])
time.sleep({RECORD_SECS})
r.stopMicrophonesRecording()
""")
    sftp = ssh.open_sftp()
    sftp.get(REMOTE_WAV, LOCAL_WAV)
    sftp.close()


def nao_say(ssh, text):
    """speak text, pausing 0.5s on newlines. stops early if interrupted."""
    global is_speaking, speech_interrupted
    is_speaking = True
    speech_interrupted = False
    segments = [s.strip() for s in text.split("\n") if s.strip()]
    for i, seg in enumerate(segments):
        if speech_interrupted:
            break
        safe = json.dumps(seg)
        nao_run(ssh, f"""
from naoqi import ALProxy
ALProxy("ALTextToSpeech","127.0.0.1",9559).say({safe})
""")
        if i < len(segments) - 1 and not speech_interrupted:
            time.sleep(0.5)
    is_speaking = False


def nao_say_animated(ssh, text):
    """try animated speech for gestures; fall back to plain text-to-speech."""
    safe = json.dumps(text)
    try:
        nao_run(ssh, f"""
from naoqi import ALProxy
ALProxy("ALAnimatedSpeech","127.0.0.1",9559).say({safe})
""")
    except Exception:
        nao_say(ssh, text)


def nao_stop_speaking(ssh):
    """stop in-progress speech immediately on the nao."""
    global speech_interrupted
    speech_interrupted = True
    try:
        nao_run(ssh, """
from naoqi import ALProxy
ALProxy("ALTextToSpeech","127.0.0.1",9559).stopAll()
""")
    except Exception:
        pass


def nao_capture_image(ssh):
    """take a photo from the nao's camera and download it."""
    nao_run(ssh, f"""
from naoqi import ALProxy
pc = ALProxy("ALPhotoCapture","127.0.0.1",9559)
pc.setResolution(2)
pc.setPictureFormat("jpg")
pc.takePicture("{os.path.dirname(REMOTE_IMG)}/", "{os.path.splitext(os.path.basename(REMOTE_IMG))[0]}")
""")
    sftp = ssh.open_sftp()
    sftp.get(REMOTE_IMG, LOCAL_IMG)
    sftp.close()


def nao_wave(ssh):
    """wave the right hand. silently does nothing if motion fails."""
    try:
        nao_run(ssh, """
from naoqi import ALProxy
import time
m = ALProxy("ALMotion","127.0.0.1",9559)
m.setStiffnesses("RArm", 1.0)
names = ["RShoulderPitch","RShoulderRoll","RElbowYaw","RElbowRoll","RWristYaw","RHand"]
m.angleInterpolation(names, [-0.5,-0.3,1.0,1.0,0.0,1.0], [1.0]*6, True)
for _ in range(3):
    m.angleInterpolation(["RWristYaw"], [0.5], [0.3], True)
    m.angleInterpolation(["RWristYaw"], [-0.5], [0.3], True)
time.sleep(0.3)
m.angleInterpolation(names, [1.4,0.2,1.2,0.5,0.0,0.0], [1.0]*6, True)
m.setStiffnesses("RArm", 0.0)
""")
    except Exception:
        pass


def nao_track_face(ssh, enable=True):
    """toggle face tracking; silently fails."""
    try:
        if enable:
            nao_run(ssh, """
from naoqi import ALProxy
ALProxy("ALFaceDetection","127.0.0.1",9559).subscribe("robot_face")
t = ALProxy("ALTracker","127.0.0.1",9559)
t.registerTarget("Face", 0.1)
t.track("Face")
""")
        else: # if not enabled
            nao_run(ssh, """
from naoqi import ALProxy
t = ALProxy("ALTracker","127.0.0.1",9559)
t.stopTracker()
t.unregisterAllTargets()
try:
    ALProxy("ALFaceDetection","127.0.0.1",9559).unsubscribe("robot_face")
except:
    pass
""")
    except Exception:
        pass


def nao_set_leds(ssh, group, colour, duration=1.0):
    """fade an led group to a specific colour. Silently fail.."""
    try:
        nao_run(ssh, f"""
from naoqi import ALProxy
ALProxy("ALLeds","127.0.0.1",9559).fadeRGB("{group}", {colour}, {duration})
""")
    except Exception:
        pass

## audio analysis ##

def check_audio_volume():
    """return True when the recorded wav is loud enough to process."""
    try:
        with wave.open(LOCAL_WAV, "rb") as wf:
            raw = wf.readframes(wf.getnframes())
            if len(raw) < 2:
                return False
            samples = struct.unpack(f"<{len(raw) // 2}h", raw)
            rms = (sum(s * s for s in samples) / len(samples)) ** 0.5
            return rms > VOLUME_THRESHOLD
    except Exception:
        return True  # proceed if the check itself fails

## transcription ##

def transcribe():
    """transcribe the local .wav with whisper."""
    with open(LOCAL_WAV, "rb") as fh:
        return client.audio.transcriptions.create(model="whisper-1", file=fh).text.strip()

## vision ##

def describe_image(ssh):
    """capture a photo from the nao and describe it with gpt-4 vision."""
    nao_capture_image(ssh)
    with open(LOCAL_IMG, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode()
    resp = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": "Describe what you see in this image in 1-2 sentences."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
        ]}],
    )
    return resp.choices[0].message.content

## web search ##

def web_search(query):
    """search the web via the responses API; falls back to model knowledge."""
    try:
        resp = client.responses.create(
            model="gpt-4.1",
            tools=[{"type": "web_search_preview"}],
            input=query,
        )
        return resp.output_text
    except Exception:
        resp = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "Answer briefly using your best knowledge."},
                {"role": "user", "content": query},
            ],
        )
        return resp.choices[0].message.content

## tool-call dispatch ##

def handle_tool_call(ssh, name, args):
    """execute a tool call and return the result string."""
    global robot_name, messages

    if name == "web_search":
        return web_search(args.get("query", ""))
    if name == "get_time_date":
        return datetime.datetime.now().strftime("It is %I:%M %p on %A, %B %d, %Y.")
    if name == "describe_vision":
        return describe_image(ssh)
    if name == "remember_preference":
        mem = load_memory()
        mem.setdefault(args["person"].lower(), {})[args["key"]] = args["value"]
        save_memory(mem)
        return f"Remembered {args['key']} for {args['person']}."
    if name == "recall_preferences":
        prefs = load_memory().get(args["person"].lower(), {})
        return json.dumps(prefs) if prefs else f"I don't remember anything about {args['person']}."
    if name == "change_name":
        old = robot_name
        robot_name = args["new_name"]
        messages[0] = {"role": "system", "content": _system_prompt()}
        return f"Name changed from '{old}' to '{robot_name}'."
    return "Unknown tool."

## gpt interaction (with iterative tool-call handling) ##
def ask_gpt(ssh, text):
    """send user text to the model, handle any tool calls, return the final reply."""
    messages.append({"role": "user", "content": text})
    resp = client.chat.completions.create(model="gpt-4.1", messages=messages, tools=TOOLS)
    msg = resp.choices[0].message

    # resolve tool calls in a loop until the model returns plain text
    while msg.tool_calls:
        messages.append(msg)
        for tc in msg.tool_calls:
            result = handle_tool_call(
                ssh, tc.function.name, json.loads(tc.function.arguments)
            )
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
        resp = client.chat.completions.create(model="gpt-4.1", messages=messages, tools=TOOLS)
        msg = resp.choices[0].message

    messages.append({"role": "assistant", "content": msg.content})
    return msg.content

# MAIN EXECUTION ──────────────────────────────────────────────────────────────────

def main():
    global is_speaking

    ssh     = ssh_connect()   # recording, commands, general I/O
    ssh_tts = ssh_connect()   # dedicated connection for TTS (enables interruption)
    speech_thread = None

    print(f"Connected to NAO at {NAO_IP}")
    print(f"Robot name: {robot_name}\n")

    # startup: face tracking + leds + wave + greeting (all optional)
    nao_track_face(ssh, enable=True)
    nao_set_leds(ssh, "FaceLeds", 0x0000FF00, 1.0)
    nao_wave(ssh)
    nao_say_animated(ssh, f"Hello! My name is {robot_name}.")

    # conversation loop
    try:
        while True:
            # ── listen ──
            print("Listening...")
            nao_set_leds(ssh, "EarLeds", 0x0000FF00, 0.3)
            nao_record(ssh)

            if not check_audio_volume():
                print("(Below volume threshold - skipping)")
                continue

            text = transcribe()
            print(f"Heard: {text}")

            if not text:
                continue

            lower = text.lower().strip()

            # ── goodbye ──
            first_word = lower.split()[0].rstrip(".,!?") if lower.split() else ""
            if first_word in {"goodbye", "bye"}:
                if is_speaking:
                    nao_stop_speaking(ssh)
                    if speech_thread and speech_thread.is_alive():
                        speech_thread.join(timeout=2)
                nao_set_leds(ssh, "FaceLeds", 0x00FF0000, 0.5)
                nao_say(ssh_tts, "Goodbye!")
                break

            # ── interrupt previous speech ──
            if is_speaking:
                print("(Interrupting previous speech)")
                nao_stop_speaking(ssh)
                if speech_thread and speech_thread.is_alive():
                    speech_thread.join(timeout=2)

            # ── face tracking when name is heard ──
            if robot_name.lower() in lower:
                nao_track_face(ssh, enable=True)

            # think 
            nao_set_leds(ssh, "EarLeds", 0x000000FF, 0.3)
            reply = ask_gpt(ssh, text)
            print(f"Reply: {reply}\n")

            # speak (running on background thread so it can be interrupted) 
            nao_set_leds(ssh, "FaceLeds", 0x00FFFFFF, 0.3)
            speech_thread = threading.Thread(
                target=nao_say, args=(ssh_tts, reply), daemon=True
            )
            speech_thread.start()

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        if speech_thread and speech_thread.is_alive():
            nao_stop_speaking(ssh)
            speech_thread.join(timeout=3)
        nao_track_face(ssh, enable=False)
        nao_set_leds(ssh, "FaceLeds", 0x00000000, 0.5)
        ssh.close()
        ssh_tts.close()
        print(f"{robot_name} disconnected.")


if __name__ == "__main__":
    main()
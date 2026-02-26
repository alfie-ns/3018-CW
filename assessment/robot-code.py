“””
NAO + OpenAI Conversation Loop
Run on your laptop. Requires: pip install paramiko openai python-dotenv
Create a .env file with: OPENAI_API_KEY=sk-your-key-here
“””

import os
import json
import tempfile
import paramiko
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

NAO_IP = “192.168.1.X”
NAO_USER = “nao”
NAO_PASS = “nao”
RECORD_SECS = 5
REMOTE_WAV = “/var/persistent/home/nao/input.wav”
LOCAL_WAV = os.path.join(tempfile.gettempdir(), “nao_input.wav”)

client = OpenAI()
messages = [{“role”: “system”, “content”: “You are a NAO robot. Converse with the user as a helpful assisstance”}]

def ssh_connect():
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(NAO_IP, username=NAO_USER, password=NAO_PASS)
return ssh

def nao_run(ssh, code):
escaped = code.replace(”’”, “’\’’”)
_, out, err = ssh.exec_command(f”python -c ‘{escaped}’”, timeout=30)
return out.read().decode().strip()

def nao_record(ssh):
nao_run(ssh, f”””
from naoqi import ALProxy
import time
r = ALProxy(“ALAudioRecorder”,“127.0.0.1”,9559)
r.stopMicrophonesRecording()
r.startMicrophonesRecording(”{REMOTE_WAV}”,“wav”,16000,[0,0,1,0])
time.sleep({RECORD_SECS})
r.stopMicrophonesRecording()
“””)
sftp = ssh.open_sftp()
sftp.get(REMOTE_WAV, LOCAL_WAV)
sftp.close()

def nao_say(ssh, text):
safe = json.dumps(text)
nao_run(ssh, f”””
from naoqi import ALProxy
ALProxy(“ALTextToSpeech”,“127.0.0.1”,9559).say({safe})
“””)

def transcribe():
with open(LOCAL_WAV, “rb”) as f:
return client.audio.transcriptions.create(model=“whisper-1”, file=f).text.strip()

def ask_gpt(text):
messages.append({“role”: “user”, “content”: text})
reply = client.chat.completions.create(model=“gpt-4o”, messages=messages).choices[0].message.content
messages.append({“role”: “assistant”, “content”: reply})
return reply

def main():
ssh = ssh_connect()
print(f”Connected to NAO at {NAO_IP}\n”)

```
try:
    while True:
        print("Listening...")
        nao_record(ssh)

        text = transcribe()
        print(f"Heard: {text}")

        if not text:
            continue
        if "goodbye" in text.lower():
            nao_say(ssh, "Goodbye!")
            break

        reply = ask_gpt(text)
        print(f"Reply: {reply}\n")
        nao_say(ssh, reply)

except KeyboardInterrupt:
    pass
finally:
    ssh.close()
```

if **name** == “**main**”:
main()
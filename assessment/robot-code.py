"""
TODO

- [ ] get connected to openai api
- [ ] make web-search capabilities
- [ ] make vision capabilities  
- [ ] capability to fetch time and date if the AI determines its useful, encode this ability into system prompt 
"""

import os
import json
import tempfile
import paramiko
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

NAO_IP = "ROBOT's IP ADDRESS"  
NAO_USER = "nao"
NAO_PASS = "nao"
RECORD_SECS = 5 # record for 5 seconds
REMOTE_WAV = "/var/persistent/home/nao/input.wav" # location on the NAO robot where the audio will be temporarily saved
LOCAL_WAV = os.path.join(tempfile.gettempdir(), "nao_input.wav") # location on the local machine wherein the audio will be temporarily saved

client = OpenAI() # init OpenAI API client

messages = [{"role": "system", "content": "You are a NAO robot. You are an assistive humanoid robot"}]

def ssh_connect():
    """
    SSH into the NAO robot. Returns an active SSH connection.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(NAO_IP, username=NAO_USER, password=NAO_PASS)
    return ssh


def nao_run(ssh, code):
    """
    Run the script via SSH on the NAO robot. Takes in the SSH connection and the code to run as a string. Returns the output of the command.
    """
    escaped = code.replace("'", "'\\''")
    _, out, err = ssh.exec_command(f"python -c '{escaped}'", timeout=30)
    return out.read().decode().strip()


def nao_record(ssh):
    """
    Record audio on the NAO robot. Uses the ALAudioRecorder module to record from the microphones and saves the file to a temporary location. Then, use SFTP to transfer the recorded file back to this machine for transcription.
    """
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
    """
    Make the NAO robot speak. Takes in the SSH connection and the text to say. Uses the ALTextToSpeech module to 'speak' the text.
    """
    safe = json.dumps(text) # wraps text as a safe Python string literal for the remote script
    nao_run(ssh, f"""
from naoqi import ALProxy
ALProxy("ALTextToSpeech","127.0.0.1",9559).say({safe})
""")


def transcribe():
    """
    Transcribe the recorded audio using OpenAI's Whisper model.
    """
    with open(LOCAL_WAV, "rb") as f:
        return client.audio.transcriptions.create(model="whisper-1", file=f).text.strip()


def ask_gpt(text):
    """
    Prompt GPT with the conversation history and append the reply to the convo.
    """
    messages.append({"role": "user", "content": text})
    reply = client.chat.completions.create(model="gpt-4.1", messages=messages).choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply

# MAIN EXECUTION -----

def main():
    ssh = ssh_connect() # init SSH connection
    print(f"Connected to NAO at {NAO_IP}\n")

    try:
        while True:
            print("Listening...")
            nao_record(ssh)

            text = transcribe()
            print(f"Heard: {text}")

            if not text:
                continue
            if "goodbye" in text.lower() or "bye" in text.lower():
                nao_say(ssh, "Goodbye!")
                break

            reply = ask_gpt(text)
            print(f"Reply: {reply}\n")
            nao_say(ssh, reply)

    except KeyboardInterrupt:
        pass
    finally:
        ssh.close()


if __name__ == "__main__":
    main()
import sounddevice as sd
import numpy as np

# try each input device until one works
devices = sd.query_devices()
input_devs = [(i, d) for i, d in enumerate(devices) if d["max_input_channels"] > 0]

for idx, dev in input_devs:
    rate = int(dev["default_samplerate"])
    print(f"Trying device {idx}: {dev['name']} at {rate}Hz ... ", end="", flush=True)
    try:
        sd.default.device = (idx, None)
        audio = sd.rec(int(2 * rate), samplerate=rate, channels=1, dtype="int16", blocking=True)
        rms = (np.mean(audio.astype(np.float64) ** 2)) ** 0.5
        print(f"RMS: {rms:.0f}")
        if rms > 10:
            print(f"  USE THIS ONE: device {idx}")
            break
    except Exception as e:
        print(f"FAILED: {e}")

print("Done.")

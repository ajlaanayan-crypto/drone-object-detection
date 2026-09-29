import sounddevice as sd
import numpy as np
import wave

def record_audio(filename="input.wav", duration=5, fs=16000):
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    audio = np.int16(audio * 32767)

    with wave.open(filename, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(fs)
        f.writeframes(audio.tobytes())
"""Kokoro (Apache-2.0, offline) test voices for HOLLOW KIN dialogue.
usage: .venv/bin/python say.py "<text>" out/name.wav [voice] [speed]
Voices: am_michael / am_adam (Max), af_bella / af_heart (Jaz, nurses), af_sky (Emilia), bm_george (Halvorsen)."""
import sys, os, soundfile as sf
from kokoro_onnx import Kokoro
D = os.path.dirname(os.path.abspath(__file__))
k = Kokoro(os.path.join(D, 'models/kokoro-v1.0.onnx'), os.path.join(D, 'models/voices-v1.0.bin'))
text, out = sys.argv[1], sys.argv[2]
voice = sys.argv[3] if len(sys.argv) > 3 else 'am_michael'; speed = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
os.makedirs(os.path.dirname(os.path.join(D, out)) or D, exist_ok=True)
samples, sr = k.create(text, voice=voice, speed=speed, lang='en-us')
sf.write(os.path.join(D, out), samples, sr); print('wrote', out, round(len(samples) / sr, 1), 's')

"""All voiced lines (Kokoro, offline). id -> (voice, speed, text). Max = am_echo (early 20s), Jaz = af_sarah,
Emilia = af_sky, police radio = am_onyx. Run: .venv/bin/python lines.py  -> out/vo/VO_<id>.wav"""
LINES = {
    # prologue: the call
    'jaz_1': ('af_sarah', 1.0, "Max Hunt? Don't hang up. My name is Jaz. I used to work for Project Lantern."),
    'jaz_2': ('af_sarah', 1.0, "Your sister is alive. Emilia. They never put her in foster care. She's under Saint Brigid's clinic, at the end of this street."),
    'jaz_3': ('af_sarah', 1.05, "They're shutting the place down tonight, and they'll erase everything down there. Her too. The front door is open. Go. Now."),
    'max_phone': ('am_echo', 0.95, "...Em?"),
    # prologue: new beats on Main Street
    'max_city_1': ('am_echo', 1.0, "Six days since that letter. And now a stranger calls me at midnight. Okay. Okay, Em. I'm coming."),
    'radio_1': ('am_onyx', 1.1, "All units, avoid Main Street. State quarantine order is in effect. Do not engage. Repeat, do not engage."),
    'max_city_2': ('am_echo', 1.0, "Missing. Missing. Missing. Every one of these kids came out of state care. So did Em."),
    'max_city_3': ('am_echo', 1.05, "Hey! Hey, wait! ...Em?"),
    'jaz_4': ('af_sarah', 1.05, "Max, it's Jaz. Whatever you just saw out there, don't follow it. Get inside the clinic. Now."),
    'max_city_4': ('am_echo', 0.95, "Saint Brigid's. Every light on, and nobody home."),
    # clinic / labs cutscenes
    'max_f1': ('am_echo', 1.0, "Where is everyone? Emilia was brought here. I saw the ambulance."),
    'max_b9': ('am_echo', 0.95, "Emilia... if you can hear me, I'm coming. I don't care how deep this goes."),
    'max_b12': ('am_echo', 0.95, "This is what they were turning the children into."),
    'max_b15': ('am_echo', 0.9, "It's okay. I'm here to take you home. All of you."),
    'emilia_1': ('af_sky', 1.0, "Max? You came. They told me you'd forgotten me."),
    'emilia_2': ('af_sky', 0.95, "The others are like me now. The lantern in my head is so bright, Max. Don't let them put it out."),
}
if __name__ == '__main__':
    import os, soundfile as sf
    from kokoro_onnx import Kokoro
    D = os.path.dirname(os.path.abspath(__file__))
    k = Kokoro(os.path.join(D, 'models/kokoro-v1.0.onnx'), os.path.join(D, 'models/voices-v1.0.bin'))
    os.makedirs(os.path.join(D, 'out/vo'), exist_ok=True)
    for i, (v, sp, t) in LINES.items():
        s, sr = k.create(t, voice=v, speed=sp, lang='en-us')
        sf.write(os.path.join(D, 'out/vo/VO_%s.wav' % i), s, sr, subtype='PCM_16'); print(i, round(len(s) / sr, 1))

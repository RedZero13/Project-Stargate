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
    # choices
    'paramedic': ('bm_george', 0.9, "Service lift... first floor. The drawing on the nurse glass... tells you the order."),
    'nurse_okafor': ('af_bella', 1.05, "Thank God. There's a med kit in the B2 nurse station, take it. And whatever you do, don't trust the quiet floors."),
    'guard_hale': ('am_adam', 0.95, "You're not one of them. Okay. My squad's on B9. I'll tell them to hold fire. Ammo cache by the lift. Go."),
    # New Game+ only: Emilia's echoes (hints toward the hidden ending)
    'echo_1': ('af_sky', 0.9, "Max... the medicine on the fourth floor. Leave it. It's for us."),
    'echo_2': ('af_sky', 0.9, "The nurse knows the way out. Let her go."),
    'echo_3': ('af_sky', 0.9, "Tell everyone, Max. Send them everything."),
    # NPC arcs
    'leo_2': ('bm_george', 0.85, "I drove her in. Your sister. Three weeks ago... If you see a little girl called Sofi... tell her Daddy's sorry he was late."),
    'okafor_b5': ('af_bella', 1.0, "You came back down. I owe you the truth. I sedated them. Every night, the little ones. They paid for my boy's treatment, and I told myself they were just sick children. Can you forgive that?"),
    'okafor_forgive': ('af_bella', 0.95, "Then I'll help you carry them out. Every one of them. I'll be at the bottom when you need me."),
    'okafor_condemn': ('af_bella', 0.95, "No. You're right. I don't deserve it."),
    'hale_b12': ('am_adam', 0.9, "Hey. Hunt. Told you I'd hold them off... the bite's spreading. I can feel it in my teeth. I don't want to become one of those things."),
    'hale_mercy': ('am_adam', 0.85, "Thank you. Find your sister."),
    'hale_stand': ('am_adam', 0.95, "One bullet's enough. Go. Whatever's coming down that corridor goes through me first."),
    'jaz_wards': ('af_sarah', 1.0, "Max, you're in the wards. I wrote the dosing schedules for those children. I need you to know that before you trust anything else I say."),
    'jaz_deep': ('af_sarah', 1.0, "Emilia's cell is L-03. The others are Noor, Theo, Mila, Sofi and Ivy. I gave them names, because nobody else would."),
    'jaz_reveal': ('af_sarah', 0.9, "My name is Jasmine Halvorsen. Doctor Halvorsen is my father. Every door you've opened tonight... I should have opened years ago."),
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

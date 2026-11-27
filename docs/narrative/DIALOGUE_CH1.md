# Chapter 1 dialogue draft (Containment Wing slice)

> Draft lines for the Chapter 1 slice. Voices: ElevenLabs later (see ROADMAP §2.6). Tone: tired, specific, never quippy. Max is 21 and scared, talking low. Keep each line short enough for a subtitle (≤ 2 lines). IDs are for String Tables (`ST_Dialogue`).

## Radio — Jaz (ally, remote; hint system, optional)
| ID | When | Line |
|----|------|------|
| JAZ_001 | Max enters the wing | "Max. Say something. The feed's all static on my end." |
| JAZ_002 | first save terminal used | "That terminal still has power? Then it still has records. Don't read them. Save and move." |
| JAZ_003 | idle 60 s near breaker puzzle | "Breaker panel needs two fuses. Old lab, old hardware. Check the lockers, the dead ends." |
| JAZ_004 | power restored | "I heard that. Whatever you did, the lights are on in the whole wing now. Good... and bad." |
| JAZ_005 | sanity < 40 first time | "Your pulse is through the roof. Breathe. Turn the flashlight on, the dark isn't helping." |
| JAZ_006 | Hollow Child spared | "Was that... she's not yours, is she? Okay. Okay. Keep walking." |
| JAZ_007 | Hollow Child killed | "Max. That was a kid. Tell me that wasn't a kid." |

## Emilia — intercom voice (Bond lines; she is a Hollow, speaking through the PA)
| ID | When | Line |
|----|------|------|
| EMI_001 | first intercom | "Max? You came. You're late. You always say five minutes." |
| EMI_002 | after first drone | "Don't be mad at them. They're hungry. They don't know your name." |
| EMI_003 | near a drawing | "I left you one. It's the blue one. You're the tall one holding the lantern." |
| EMI_004 | sanity < 20 | "You're doing the thing with your hands. Mum did that. Look at me, not the dark." |
| EMI_005 | Bond ≥ 40 | "You didn't hurt them. I knew you wouldn't." |
| EMI_006 | Taint ≥ 40 | "Your voice sounds different. Did they put something in you too?" |
| EMI_007 | Hollow whisper (hallucination layer) | "Max... Max... five minutes... five minutes..." |

## Max — short barks (spoken low, in-world)
| ID | When | Line |
|----|------|------|
| MAX_001 | picks up ammo | "Not much." |
| MAX_002 | health gel | "That'll do." |
| MAX_003 | fuse pickup | "One. Where's the other?" |
| MAX_004 | locked / sealed door | "Dead. Needs power." |
| MAX_005 | drone spotted | "Don't look at me. Don't look at me." |
| MAX_006 | reload | "Come on, come on." |
| MAX_007 | Hollow Child spared | "I'm not going to hurt you. I'm not." |
| MAX_008 | ending trigger, power on | "Emilia?" |

## Guard barks (human, armed, panicking; they never speak to Max calmly)
| ID | When | Line |
|----|------|------|
| GRD_001 | spots Max | "Contact! Hands where I can see them!" |
| GRD_002 | alerts others | "He's in the east corridor, all units!" |
| GRD_003 | loses Max | "Where'd he go? Where did he go?" |
| GRD_004 | hit | "Argh— he's armed!" |
| GRD_005 | dying | "Tell Halvorsen... it wasn't worth..." |

## Notes / documents (found text, ≤ 40 words)
1. **Shutdown memo (L-7 wing)** — "All subject activity suspended pending transfer. Do not attempt to restore Containment power. If a subject responds to a name, do not use it again."
2. **Nurse log** — "The girl in L-03 asks for her brother every night at the same hour. Yesterday the speakers answered her. We didn't touch the speakers."
3. **Emilia's drawing note** — "This is Max. He's tall. He has a lantern because he's scared of the dark but he never says."

## Ending cards (shown after the final trigger)
- **HOMECOMING** (Bond ≥ 70, Taint < 40): "Emilia is human again. They walk out into the morning."
- **KIN** (Bond ≥ 40): "She stays Hollow. She never lets go of your hand."
- **LANTERN** (otherwise): "You stay, so she can leave."

## Music cues (placeholder tracks in `Content/HollowKin/Audio/Music`)
- `MUS_Ambient_Containment`: default exploration bed (playing now from the test layout).
- `MUS_Tension`: fade in while any enemy is chasing; out 8 s after losing sight (not wired yet).
- `MUS_Lullaby_MusicBox`: safe rooms and Emilia's scenes; plays at the save terminal (not wired yet).

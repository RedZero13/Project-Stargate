"""Shared definition of the Options page rows (007 First Light layout): page -> rows of
(widget name, label, default value text, description). Used by build_options.py and build_options_logic.py."""
PAGES = [
    ('GAMEPLAY', [
        ('BtnOverlay', 'Screen HUD', 'OFF', "Show health, sanity and ammo as an overlay on the screen. When off, they appear only on Max's wrist monitor and the pistol's display."),
        ('BtnTextSize', 'Text size', 'NORMAL', 'Size of notes, objectives and dialogue text.'),
    ]),
    ('CONTROLS', [
        ('BtnSens', 'Look sensitivity', '100%', 'How fast the camera turns with the mouse, trackpad or right stick.'),
        ('BtnInvert', 'Invert camera Y', 'OFF', 'Push the mouse or stick up to look down.'),
    ]),
    ('GRAPHICS', [
        ('BtnQuality', 'Graphics quality', 'HIGH', 'Overall detail preset. Lower settings run faster and use less memory; EPIC is for strong desktop GPUs.'),
        ('BtnResScale', 'Resolution scale', '100%', 'Renders the 3D scene at a lower resolution and upscales it. The biggest speed and memory saver on laptops and wide screens.'),
        ('BtnVsync', 'VSync', 'ON', 'Locks the frame rate to the display to prevent tearing. Turn off for lower input delay.'),
        ('BtnWindow', 'Display mode', 'FULLSCREEN', 'Borderless full screen at your desktop resolution, or a window.'),
        ('BtnFps', 'Frame rate limit', '60', 'Caps the frame rate. Lower caps keep laptops cooler and quieter.'),
        ('BtnMotionBlur', 'Motion blur', 'ON', 'Blur when the camera moves quickly. Turn off if it causes discomfort.'),
    ]),
    ('AUDIO', [
        ('BtnMaster', 'Master volume', '100%', 'Overall game volume.'),
        ('BtnMusic', 'Music volume', '100%', 'Score and safe-room music.'),
        ('BtnSfx', 'Effects volume', '100%', 'Footsteps, weapons, creatures, ambience and the interface.'),
    ]),
    ('ACCESSIBILITY', [
        ('BtnFlash', 'Reduce flashing', 'OFF', 'Softens muzzle flashes, damage flashes and flickering lights.'),
    ]),
]
KEYS = [('Move', 'W  A  S  D'), ('Look', 'Mouse / trackpad'), ('Run', 'Shift'), ('Crouch', 'C'), ('Jump', 'Space'),
        ('Flashlight', 'F'), ('Aim', 'Right mouse / Q   (T toggles)'), ('Fire', 'Left mouse / E'), ('Punch', 'V'),
        ('Reload', 'R'), ('Swap shoulder', 'Tab'), ('Pause / back', 'P / Esc')]

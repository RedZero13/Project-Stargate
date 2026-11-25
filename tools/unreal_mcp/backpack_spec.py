"""Item and recipe definitions for the backpack screen (WBP_Backpack)."""
ITEMS = [  # key, label, icon text, icon colour, max var, description, usable fn
    ('Ammo', 'PISTOL ROUNDS', '9mm', 'c9a24a', 'ReserveAmmo', '.45 rounds for the M1911. Reload with R.', None),
    ('Gel', 'HEALTH GEL', '+HP', '3fae6a', 'Gels', 'Field wound gel. Restores 40 health. Click to use.', 'UseGel'),
    ('Sed', 'SEDATIVE', 'Rx', '4f8fd8', 'Sedatives', 'Calms the mind. Restores 35 sanity. Click to use.', 'UseSedative'),
    ('Bottle', 'GLASS BOTTLE', 'GLS', '7fb0a8', 'Bottles', 'Throw with G. It shatters where it lands and Hollows go to the noise.', None),
    ('Fuse', 'FUSE', 'FUSE', 'dfe9e6', 'Fuses', 'Ceramic power fuse. The breaker needs two.', None),
    ('Parts', 'SCRAP PARTS', 'PRT', '9a8a78', 'Parts', 'Springs, casings and wire. A workbench ingredient.', None),
    ('Chem', 'CHEMICALS', 'CHM', 'b56fd6', 'Chem', 'Lab reagents. A workbench ingredient.', None),
    ('Tape', 'CASSETTE TAPES', 'TAPE', 'e0a547', 'Tapes', 'Messages you recorded for Emilia at save points.', None),
]
RECIPES = [  # key, result label, icon, colour, ingredients [(item key, need)], craft fn, description
    ('RAmmo', '6 PISTOL ROUNDS', '9mm', 'c9a24a', [('Parts', 2), ('Chem', 1)], 'CraftAmmo', 'Pack spare casings with powder from the lab reagents.'),
    ('RTonic', 'SEDATIVE', 'Rx', '4f8fd8', [('Chem', 2)], 'CraftTonic', 'Mix a calming tonic from two reagents.'),
]

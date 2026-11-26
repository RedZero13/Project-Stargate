"""Achievement list and collectible totals (shared by progress_system.py, achievement_hooks.py, build_achievements.py)."""
ACH = [  # id, title, description
    ('first_light', 'First Light', 'Take the pistol from the dead guard.'),
    ('lights_on', 'Lights On', 'Restore power to the Containment Wing.'),
    ('mercy', 'Mercy', 'Lower your gun for the Hollow Child.'),
    ('darkened', 'Something Darkens', 'Hurt the Hollow Child.'),
    ('going_down', 'Going Down', 'Reach the wards below St. Brigid\'s.'),
    ('deep_labs', 'The Real Program', 'Reach the Deep Labs.'),
    ('isolation', 'L-03', 'Reach the isolation chambers on B15.'),
    ('end_lantern', 'Lantern', 'See the Lantern ending.'),
    ('end_kin', 'Kin', 'See the Kin ending.'),
    ('end_home', 'Homecoming', 'See the Homecoming ending.'),
    ('all_endings', 'Every Door', 'See all three endings.'),
    ('drawings_5', 'Crayon Trail', 'Find 5 of Emilia\'s drawings in one run.'),
    ('drawings_all', 'The Whole Gallery', 'Find all of Emilia\'s drawings in one run.'),
    ('files_5', 'Paper Trail', 'Read 5 patient files in one run.'),
    ('files_all', 'Archivist', 'Read every patient file in one run.'),
    ('kills_10', 'Orderly', 'Put down 10 Hollows.'),
    ('kills_50', 'Exterminator', 'Put down 50 Hollows.'),
    ('elite', 'The Bigger They Are', 'Kill a brute or an Experiment.'),
    ('crafter', 'Field Medic', 'Craft 5 items at the workbench.'),
]
TOTAL_DRAWINGS = 3 + 14   # 3 in the Containment Wing + one on G, F1, B2-B8, B10-B14
TOTAL_FILES = 14

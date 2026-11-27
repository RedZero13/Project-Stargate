#!/usr/bin/env python3
"""Containment Wing greybox generator (HOLLOW KIN vertical slice).

Rooms follow docs/levels/CONTAINMENT_WING.md (C1-C9). Coordinates are centimetres,
X forward from the lift, Y to the right. Walls are computed on a 25 cm grid from the
room + doorway rectangles, then merged into as few boxes as possible.

Output: JSON consumed by tools/unreal_mcp/build_slice.sh (places SM_Cube actors in
Lvl_ContainmentWing; SM_Cube is 100 cm with its pivot at the min corner).
Run:  python3 tools/slice_layout.py > /tmp/slice.json
"""
import json, sys

G = 25            # grid cell (cm)
WALL_H = 460      # walls are taller than every ceiling; the excess is hidden above
# name: (x0, y0, x1, y1, ceiling height, material key)
ROOMS = {
    "C1_LiftLanding":     (0,    -300,  800,   300, 300, "concrete"),
    "C2_DeconCorridor":   (825,  -200,  2800,  200, 300, "tile"),
    "C3_NursesStation":   (2825, -300,  3600,  300, 300, "warm"),
    "C4_ObservationRing": (3625, -600,  5400,  600, 450, "tile"),
    "C5_CellBlockA":      (3625, -1525, 5100, -625, 350, "concrete"),
    "C6_ChildrensDorm":   (3625,  625,  4800,  1425, 350, "warm"),
    "C7_IsolationCells":  (5125, -1525, 6500, -725, 300, "concrete"),
    "C8_EmiliasRoom":     (6525, -1425, 7300, -825, 350, "warm"),
    "C9_LabDoor":         (5425, -200,  5800,  200, 450, "tile"),
}
# doorways: floor strips that cut through the 25 cm wall between two rooms
DOORS = {
    "C1_C2": (800,  -150, 825,  150),
    "C2_C3": (2800, -100, 2825, 100),
    "C3_C4": (3600, -100, 3625, 100),
    "C4_C5": (4200, -625, 4400, -600),
    "C4_C6": (4000,  600, 4200,  625),
    "C4_C9": (5400, -200, 5425,  200),
    "C5_C7": (5100, -1200, 5125, -1000),
    "C7_C8": (6500, -1225, 6525, -1025),   # power door sits here
}
DOOR_H = 240

def cells(r):
    x0, y0, x1, y1 = r[:4]
    for i in range(x0 // G, x1 // G):
        for j in range(y0 // G, y1 // G):
            yield (i, j)

def build():
    floor = set()
    for r in ROOMS.values(): floor.update(cells(r))
    for d in DOORS.values(): floor.update(cells(d))
    solid = set()
    for (i, j) in floor:
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                c = (i + di, j + dj)
                if c not in floor: solid.add(c)
    # greedy merge: runs along Y per X column, then extend along X
    boxes, used = [], set()
    for c in sorted(solid):
        if c in used: continue
        i, j = c
        j1 = j
        while (i, j1 + 1) in solid and (i, j1 + 1) not in used: j1 += 1
        i1 = i
        while all((i1 + 1, jj) in solid and (i1 + 1, jj) not in used for jj in range(j, j1 + 1)): i1 += 1
        for ii in range(i, i1 + 1):
            for jj in range(j, j1 + 1): used.add((ii, jj))
        boxes.append(dict(name="Wall", mat="wall", x=i * G, y=j * G, z=0,
                          sx=(i1 - i + 1) * G, sy=(j1 - j + 1) * G, sz=WALL_H))
    out = list(boxes)
    for n, (x0, y0, x1, y1, h, m) in ROOMS.items():
        # exact room bounds (no overlap with the neighbours' floors/ceilings: overlapping coplanar faces z-fought
        # in doorways); walls cover the seams
        out.append(dict(name=n + "_Floor", mat=m + "_floor", x=x0, y=y0, z=-20, sx=x1 - x0, sy=y1 - y0, sz=20))
        out.append(dict(name=n + "_Ceiling", mat="ceiling", x=x0, y=y0, z=h, sx=x1 - x0, sy=y1 - y0, sz=20))
    for n, (x0, y0, x1, y1) in DOORS.items():
        if x1 - x0 > 0 and y1 - y0 > 0:   # floor strip through the wall, 1 mm lower than the rooms
            out.append(dict(name="DoorFloor_" + n, mat="concrete_floor", x=x0, y=y0, z=-20.1, sx=x1 - x0, sy=y1 - y0, sz=20))
        out.append(dict(name="Lintel_" + n, mat="wall", x=x0, y=y0, z=DOOR_H, sx=x1 - x0, sy=y1 - y0, sz=WALL_H - DOOR_H))
    out += PROPS
    return out

def P(name, x, y, sx, sy, sz, mat="prop", z=0):
    return dict(name=name, mat=mat, x=x, y=y, z=z, sx=sx, sy=sy, sz=sz)

PROPS = [
    # C1: dead lift behind the player, a crate
    P("C1_LiftDoors", 0, -150, 20, 300, 260, "metal"),
    P("C1_Crate", 600, 180, 90, 90, 80),
    # C3: safe room desk + item box
    P("C3_Desk", 3300, 160, 200, 80, 75),
    P("C3_ItemBox", 2900, -280, 120, 60, 70, "metal"),
    # C4: the cracked observation tank in the middle of the ring
    P("C4_Tank", 4250, -250, 500, 500, 400, "glass"),
    P("C4_TankBase", 4200, -300, 600, 600, 30, "metal"),
    # C5: six cells along the south wall (cells 2 and 4 open)
    *[P(f"C5_CellWall{k}", 3625 + k * 245, -1525, 20, 300, 300, "concrete_floor") for k in range(1, 6)],
    *[P(f"C5_CellFront{k}", 3625 + k * 245 + (20 if k else 0), -1245, 225 if k else 245, 20, 300, "metal")
      for k in range(6) if k not in (1, 3)],
    # C6: four beds and a toy chest
    *[P(f"C6_Bed{k}", 3700 + k * 270, 1200, 100, 200, 50, "bed") for k in range(4)],
    P("C6_ToyChest", 4600, 700, 120, 60, 60, "warm_floor"),
    # C7: lockers (hiding later)
    *[P(f"C7_Locker{k}", 5200 + k * 70, -780, 60, 50, 200, "metal") for k in range(4)],
    # C8: the bolted bed
    P("C8_Bed", 7050, -1400, 200, 100, 50, "bed"),
    # C9: sealed blast door
    P("C9_BlastDoor", 5780, -200, 20, 400, 450, "metal"),
]

# point lights: (name, x, y, z, intensity (cd), r, g, b, radius)
LIGHTS = [
    ("L_C1", 400, 0, 260, 72, 1.0, 0.55, 0.25, 900),        # sodium-orange emergency lamp
    ("L_C2a", 1300, 0, 270, 48, 0.55, 0.85, 0.8, 700),      # teal fluorescent, flickers later
    ("L_C2b", 2300, 0, 270, 36, 0.55, 0.85, 0.8, 700),
    ("L_C3", 3200, 100, 230, 216, 1.0, 0.75, 0.45, 900),    # warm safe-room lamp
    ("L_C4a", 4500, 0, 380, 96, 0.4, 0.8, 1.0, 900),         # cold light inside the tank
    ("L_C4b", 3800, 450, 400, 60, 0.55, 0.85, 0.8, 800),
    ("L_C4c", 5200, -450, 400, 60, 0.55, 0.85, 0.8, 800),
    ("L_C5", 4300, -900, 320, 70, 0.9, 0.3, 0.25, 900),      # red alarm wash
    ("L_C6", 4200, 1000, 320, 60, 1.0, 0.8, 0.6, 800),       # night-light
    ("L_C7", 5400, -1300, 280, 45, 0.5, 0.6, 0.9, 600),    # nearly dark: flashlight room
    ("L_C8", 6900, -1100, 320, 110, 0.8, 0.7, 1.0, 700),
    ("L_C9", 5600, 0, 400, 48, 1.0, 0.2, 0.15, 600),         # red lockdown light
]

if __name__ == "__main__":
    data = dict(boxes=build(), lights=[dict(zip(("name", "x", "y", "z", "i", "r", "g", "b", "rad"), l)) for l in LIGHTS])
    json.dump(data, sys.stdout)
    print(f"boxes={len(data['boxes'])} lights={len(data['lights'])}", file=sys.stderr)

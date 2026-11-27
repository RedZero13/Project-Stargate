#!/usr/bin/env python3
"""Sub-Level 3 "Deep Labs" greybox (HOLLOW KIN). Same format as tools/slice_layout.py (consumed by
tools/unreal_mcp/build_slice.py with LEVEL=Lvl_DeepLabs). X forward from the lift, Y to the right, cm.
Route: lift lobby -> reception -> long hall (diagnostic labs A/B either side) -> records (safe room) ->
maintenance tunnels (a small maze with dead ends) -> abandoned generator hall (power-plant zone, hazards, the
brute) -> observation bridge -> Emilia's chamber (L-03, the ending)."""
import json, sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
import slice_layout as S

S.ROOMS = {
    "D1_LiftLobby":      (0,    -300,  800,   300, 320, "concrete"),
    "D2_Reception":      (825,  -500,  2000,  500, 340, "warm"),
    "D3_Hall":           (2025, -125,  3800,  125, 300, "tile"),
    "D4_DiagLabA":       (2200, -1000, 3400, -150, 340, "tile"),
    "D5_DiagLabB":       (2200,  150,  3400,  1000, 340, "tile"),
    "D6_Records":        (3825, -600,  4600,  600, 320, "warm"),
    "T1_Tunnel":         (4625, -100,  5300,  100, 260, "concrete"),
    "T2_Tunnel":         (5100,  100,  5300,  1300, 260, "concrete"),
    "T3_Tunnel":         (5300,  1100, 6400,  1300, 260, "concrete"),
    "T4_DeadEnd":        (5400,  1300, 5600,  1900, 260, "concrete"),
    "T5_Tunnel":         (6200, -900,  6400,  1100, 260, "concrete"),
    "T6_DeadEnd":        (5300, -900,  6200, -700, 260, "concrete"),
    "T7_Tunnel":         (6400, -900,  7100, -700, 260, "concrete"),
    "D7_GeneratorHall":  (7125, -1400, 8800,  700, 700, "concrete"),
    "D8_Bridge":         (8825, -150,  10000, 150, 500, "tile"),
    "D9_EmiliaChamber":  (10025, -800, 11300, 800, 450, "warm"),
}
S.DOORS = {
    "D1_D2": (800, -150, 825, 150), "D2_D3": (2000, -100, 2025, 100),
    "D3_D4": (2600, -150, 2800, -125), "D3_D5": (2900, 125, 3100, 150),
    "D3_D6": (3800, -100, 3825, 100), "D6_T1": (4600, -100, 4625, 100),
    "T1_T2": (5100, 100, 5300, 100), "T2_T3": (5300, 1100, 5300, 1300),
    "T3_T4": (5400, 1300, 5600, 1300), "T3_T5": (6200, 1100, 6400, 1100),
    "T5_T6": (6200, -900, 6200, -700), "T5_T7": (6400, -900, 6400, -700),
    "T7_D7": (7100, -900, 7125, -700), "D7_D8": (8800, -150, 8825, 150),
    "D8_D9": (10000, -150, 10025, 150),
}
P = S.P
S.PROPS = [
    P("D1_LiftDoors", 0, -150, 20, 300, 260, "metal"),
    P("D2_Desk", 1300, -200, 400, 90, 105, "warm_floor"), P("D2_Bench1", 900, 380, 300, 60, 45), P("D2_Bench2", 1500, 380, 300, 60, 45),
    P("D4_ScannerBed", 2900, -760, 320, 80, 70, "bed"),
    P("D4_Counter", 2250, -400, 60, 240, 95, "metal"),
    P("D5_Gurney1", 2400, 500, 220, 80, 80, "bed"), P("D5_Gurney2", 2900, 700, 220, 80, 80, "bed"),
    P("D5_Cabinet", 3300, 200, 60, 400, 200, "metal"),
    P("D6_Shelf0", 3900, -590, 300, 60, 240, "prop"), P("D6_Shelf1", 4250, -590, 300, 60, 240, "prop"),
    P("D6_Desk", 4300, 300, 200, 80, 75),
    P("T4_Grate", 5400, 1880, 200, 20, 260, "metal"), P("T6_Grate", 5300, -900, 20, 200, 260, "metal"),
    *[P("D7_Generator%d" % k, 7400 + k * 420, -1250, 300, 500, 380, "metal") for k in range(3)],
    P("D7_Catwalk", 7300, 300, 1400, 160, 20, "metal", z=300), P("D7_Pipe", 7150, 550, 1600, 80, 80, "metal", z=520),
    P("D7_Tank", 8300, -400, 300, 300, 500, "metal"),
    P("D8_RailL", 8825, -150, 1175, 10, 110, "metal"), P("D8_RailR", 8825, 140, 1175, 10, 110, "metal"),
    P("D9_Bed", 11000, -500, 200, 100, 50, "bed"),
]
S.LIGHTS = [
    ("L_D1", 400, 0, 280, 180, 1.0, 0.55, 0.25, 900), ("L_D2", 1400, 0, 300, 240, 1.0, 0.8, 0.55, 1000),
    ("L_D3a", 2400, 0, 270, 120, 0.55, 0.85, 0.8, 700), ("L_D3b", 3400, 0, 270, 120, 0.55, 0.85, 0.8, 700),
    ("L_D4", 2800, -550, 300, 210, 0.7, 0.85, 1.0, 900), ("L_D5", 2800, 550, 300, 165, 0.9, 0.3, 0.25, 900),
    ("L_D6", 4200, 0, 280, 540, 1.0, 0.75, 0.45, 900),
    ("L_T1", 4950, 0, 230, 100, 1.0, 0.5, 0.2, 500), ("L_T3", 5850, 1200, 230, 80, 1.0, 0.5, 0.2, 500),
    ("L_T5", 6300, 100, 230, 88, 1.0, 0.5, 0.2, 500), ("L_T7", 6750, -800, 230, 100, 1.0, 0.5, 0.2, 500),
    ("L_D7a", 7600, -300, 600, 360, 0.4, 0.75, 1.0, 1400), ("L_D7b", 8400, 300, 600, 270, 1.0, 0.25, 0.15, 1200),
    ("L_D8", 9400, 0, 450, 150, 0.55, 0.85, 0.8, 900), ("L_D9", 10650, 0, 400, 420, 0.8, 0.7, 1.0, 1200),
    ("L_D2b", 1000, -300, 300, 120, 1.0, 0.8, 0.55, 800), ("L_D3c", 2900, 0, 270, 120, 0.55, 0.85, 0.8, 700),
    ("L_D7c", 8000, -1000, 600, 300, 1.0, 0.6, 0.3, 1400), ("L_D8b", 9800, 0, 450, 150, 0.55, 0.85, 0.8, 900),
    ("L_D9b", 11000, -400, 400, 250, 1.0, 0.7, 0.55, 1000), ("L_T2", 5200, 700, 230, 100, 1.0, 0.5, 0.2, 500),
]
if __name__ == "__main__":
    data = dict(boxes=S.build(), lights=[dict(zip(("name", "x", "y", "z", "i", "r", "g", "b", "rad"), l)) for l in S.LIGHTS])
    json.dump(data, sys.stdout)
    print(f"boxes={len(data['boxes'])} lights={len(data['lights'])}", file=sys.stderr)

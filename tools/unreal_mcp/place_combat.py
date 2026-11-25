#!/usr/bin/env python3
"""Places hazards + the C4 elite in Lvl_ContainmentWing (tag SliceCombat, folder Slice/Combat; re-runnable)."""
import json
I = "/Game/HollowKin/Blueprints/Interactables/"
ITEMS = [  # (label, blueprint, x, y, z, scale, tags, props)
    ("HZ_C4_Barrel1", I + "BP_HazardBarrel.BP_HazardBarrel", 4950, -470, 60, 1.0, [], {}),
    ("HZ_C4_Barrel2", I + "BP_HazardBarrel.BP_HazardBarrel", 3900, 470, 60, 1.0, [], {}),
    ("HZ_C4_Barrel3", I + "BP_HazardBarrel.BP_HazardBarrel", 5250, 150, 60, 1.0, [], {}),
    ("HZ_C5_Barrel", I + "BP_HazardBarrel.BP_HazardBarrel", 4800, -1080, 60, 1.0, [], {}),
    ("HZ_C4_Shock", I + "BP_HazardShock.BP_HazardShock", 4100, -380, 60, 1.0, [], {}),
    ("HZ_C2_Shock", I + "BP_HazardShock.BP_HazardShock", 1750, -95, 60, 0.85, [], {}),
    ("C4_EliteBrute", "/Game/HollowKin/Blueprints/AI/BP_HollowDrone.BP_HollowDrone", 5050, 380, 120, 1.3, ["Elite"], {"DroneHealth": 240}),
]
TEMPLATE = r'''
import json
ITEMS = json.loads(%(items)r)
T = lambda n, a: execute_tool(n, json.dumps(a))
def run():
    if "Lvl_ContainmentWing" not in str(T("editor_toolset.toolsets.scene.SceneTools.get_current_level", {})["returnValue"]):
        return {"error": "wrong level"}
    for a in T("editor_toolset.toolsets.scene.SceneTools.find_actors", {"name": "", "tag": "SliceCombat", "collision_channels": []})["returnValue"]:
        T("editor_toolset.toolsets.scene.SceneTools.remove_from_scene", {"actor": a})
    out = []
    for (label, bp, x, y, z, s, tags, props) in ITEMS:
        a = T("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset", {"asset_path": bp, "name": label,
            "xform": {"location": {"x": x, "y": y, "z": z}, "scale": {"x": s, "y": s, "z": s}}})["returnValue"]
        for t in tags + ["SliceCombat"]:
            T("editor_toolset.toolsets.actor.ActorTools.add_tag", {"actor": a, "tag": t})
        if props:
            T("editor_toolset.toolsets.object.ObjectTools.set_properties", {"instance": a, "values": json.dumps(props)})
        T("editor_toolset.toolsets.actor.ActorTools.set_label", {"actor": a, "label": label})
        T("editor_toolset.toolsets.scene.SceneTools.set_actor_folder", {"actor": a, "folder_path": "Slice/Combat"})
        out.append(label)
    return {"placed": out}
'''
if __name__ == "__main__":
    print(TEMPLATE % {"items": json.dumps(ITEMS)})

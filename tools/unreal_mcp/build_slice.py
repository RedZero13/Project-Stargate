#!/usr/bin/env python3
"""Builds the editor-side script that places the Containment Wing greybox.

usage: python3 tools/slice_layout.py > slice.json
       python3 tools/unreal_mcp/build_slice.py slice.json > script.py
       then send script.py to ProgrammaticToolset.execute_tool_script (see build_slice.sh)

Every placed actor gets the tag "Slice" (and "M_<material key>" for boxes) and lives in
the Outliner folder "Slice/...", so the whole greybox can be found, re-textured or removed.
"""
import json, sys

MATS = {  # material key -> material path (greybox; swapped for kit materials later)
    "wall": "/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray.MI_PrototypeGrid_Gray",
    "ceiling": "/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray_02.MI_PrototypeGrid_Gray_02",
    "concrete_floor": "/Game/LevelPrototyping/Materials/MI_PrototypeGrid_TopDark.MI_PrototypeGrid_TopDark",
    "tile_floor": "/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray_Round.MI_PrototypeGrid_Gray_Round",
    "warm_floor": "/Game/LevelPrototyping/Materials/MI_PrototypeGrid_TopDark.MI_PrototypeGrid_TopDark",
    "prop": "/Game/LevelPrototyping/Materials/MI_DefaultColorway.MI_DefaultColorway",
    "metal": "/Game/LevelPrototyping/Materials/MI_PrototypeGrid_TopDark.MI_PrototypeGrid_TopDark",
    "glass": "/Game/LevelPrototyping/Materials/MI_DefaultColorway.MI_DefaultColorway",
    "bed": "/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray_02.MI_PrototypeGrid_Gray_02",
}

TEMPLATE = r'''
import json
DATA = json.loads(%(data)r)
MATS = json.loads(%(mats)r)
LEVEL = None

def T(name, args):
    return execute_tool(name, json.dumps(args))

def run():
    lvl = T("editor_toolset.toolsets.scene.SceneTools.get_current_level", {})["returnValue"]
    if "Lvl_ContainmentWing" not in str(lvl):
        return {"error": "wrong level " + str(lvl)}
    # remove a previous build of the slice
    old = T("editor_toolset.toolsets.scene.SceneTools.find_actors", {"name": "", "tag": "Slice", "collision_channels": []})["returnValue"]
    for a in old:
        T("editor_toolset.toolsets.scene.SceneTools.remove_from_scene", {"actor": a})
    n = 0
    for b in DATA["boxes"]:
        a = T("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset", {
            "asset_path": "/Game/LevelPrototyping/Meshes/SM_Cube.SM_Cube", "name": b["name"],
            "xform": {"location": {"x": b["x"], "y": b["y"], "z": b["z"]},
                      "scale": {"x": b["sx"] / 100.0, "y": b["sy"] / 100.0, "z": b["sz"] / 100.0}}})["returnValue"]
        T("editor_toolset.toolsets.object.ObjectTools.set_properties", {
            "instance": {"refPath": a["refPath"] + ".StaticMeshComponent0"},
            "values": json.dumps({"OverrideMaterials": [MATS.get(b["mat"], MATS["prop"])]})})
        T("editor_toolset.toolsets.actor.ActorTools.add_tag", {"actor": a, "tag": "Slice"})
        T("editor_toolset.toolsets.actor.ActorTools.add_tag", {"actor": a, "tag": "M_" + b["mat"]})
        T("editor_toolset.toolsets.actor.ActorTools.set_label", {"actor": a, "label": b["name"]})
        T("editor_toolset.toolsets.scene.SceneTools.set_actor_folder", {"actor": a, "folder_path": "Slice/Geometry"})
        n += 1
    for l in DATA["lights"]:
        a = T("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_class", {
            "actor_type": {"refPath": "/Script/Engine.PointLight"}, "name": l["name"],
            "xform": {"location": {"x": l["x"], "y": l["y"], "z": l["z"]}}})["returnValue"]
        T("editor_toolset.toolsets.object.ObjectTools.set_properties", {
            "instance": {"refPath": a["refPath"] + ".LightComponent0"},
            "values": json.dumps({"Mobility": "Movable", "IntensityUnits": "Candelas", "Intensity": l["i"],
                                  "LightColor": {"r": l["r"], "g": l["g"], "b": l["b"], "a": 1.0},
                                  "AttenuationRadius": l["rad"], "SourceRadius": 8})})
        T("editor_toolset.toolsets.actor.ActorTools.add_tag", {"actor": a, "tag": "Slice"})
        T("editor_toolset.toolsets.actor.ActorTools.set_label", {"actor": a, "label": l["name"]})
        T("editor_toolset.toolsets.scene.SceneTools.set_actor_folder", {"actor": a, "folder_path": "Slice/Lights"})
        n += 1
    return {"placed": n}
'''

if __name__ == "__main__":
    data = open(sys.argv[1]).read()
    print(TEMPLATE % {"data": data, "mats": json.dumps(MATS)})

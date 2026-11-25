#!/usr/bin/env python3
"""Builds the opening street in Lvl_City (copy of the Assetsville Town demo map): street lamps + lights, rain,
St. Brigid's Clinic front at the north end of main street, the phone-call trigger and the clinic door
(loads the Containment Wing). Everything gets the tag "CityHK" and lives under Outliner folder City/...; re-runnable.
Main street runs along +X at Y ~ -800 (road tiles at Y=0). Max starts at the south end and walks north."""
import json
LAMP = "/Game/Mega_Street_Props_Pack/Street_Props_pack_V2/Meshes/SM_Lamp_1.SM_Lamp_1"
HH = "/Game/Horror_Hospital/Meshes/"
CUBE = "/Game/LevelPrototyping/Meshes/SM_Cube.SM_Cube"
MESHES = []   # (label, mesh, x, y, z, yaw, sx, sy, sz, material or None, folder)
LIGHTS = []   # (label, x, y, z, candela, r, g, b, radius)
for i, x in enumerate(range(-9000, 8001, 1700)):
    west = i % 2 == 0
    y = -1850 if west else 250
    MESHES.append((f"CL_Lamp{i:02d}", LAMP, x, y, 0, 180 if west else 0, 1.4, 1.4, 1.4, None, "City/Lamps"))
    LIGHTS.append((f"CL_LampLight{i:02d}", x, y + (130 if west else -130), 575, 140, 0.78, 0.86, 1.0, 1300))
# St. Brigid's Clinic front: a block across the north end of main street (front face at X=8600)
W = "/Game/HollowKin/Materials/MI_HK_Wall.MI_HK_Wall"
M = "/Game/HollowKin/Materials/MI_HK_Metal.MI_HK_Metal"
MESHES += [
    ("CL_ClinicBlock", CUBE, 8600, -2700, -150, 0, 9, 38, 10.5, W, "City/Clinic"),
    ("CL_ClinicRoofEdge", CUBE, 8560, -2750, 880, 0, 0.6, 39, 0.35, M, "City/Clinic"),
    ("CL_Canopy", CUBE, 8300, -1350, 330, 0, 3.0, 11, 0.25, M, "City/Clinic"),
    ("CL_CanopyPostL", CUBE, 8320, -1330, 0, 0, 0.2, 0.2, 3.3, M, "City/Clinic"),
    ("CL_CanopyPostR", CUBE, 8320, -270, 0, 0, 0.2, 0.2, 3.3, M, "City/Clinic"),
    ("CL_Door", HH + "SM_Door_01_v01.SM_Door_01_v01", 8590, -858, 0, 90, 1.2, 1.2, 1.2, None, "City/Clinic"),
    ("CL_CrossSign", HH + "SM_Hospital_Board_Sign_Plus_01_v01.SM_Hospital_Board_Sign_Plus_01_v01", 8588, -1700, 560, -90, 6, 6, 6, None, "City/Clinic"),
    ("CL_EntranceSign", HH + "SM_Sign_Text_Main_Entrance.SM_Sign_Text_Main_Entrance", 8585, -700, 300, 180, 2.5, 2.5, 2.5, None, "City/Clinic"),
    ("CL_DoorLamp", HH + "SM_Lamp_05_v01.SM_Lamp_05_v01", 8450, -800, 325, 90, 1, 1, 1, None, "City/Clinic"),
]
for k, y in enumerate((-2300, -1500, -400, 300)):
    MESHES.append((f"CL_Window{k}", HH + "SM_Window_01_v01.SM_Window_01_v01", 8588, y, 420, 90, 1.3, 1.3, 1.3, None, "City/Clinic"))
LIGHTS += [
    ("CL_DoorLight", 8400, -800, 300, 90, 0.75, 1.0, 0.8, 900),     # sickly green-white over the door
    ("CL_SignLight", 8450, -1700, 620, 60, 1.0, 0.25, 0.2, 700),    # red glow on the cross
]
TEXTS = [("CL_ClinicName", "ST. BRIGID'S CLINIC", 8585, -800, 470, 110)]
SPECIAL = {
    "start": (-8700, -800, 120, 0),
    "phone": (-8150, -800, 150, 3.0),
    "door": (8470, -800, 150, 1.0),
    "rain": (-8000, -800, 600),
}
TEMPLATE = r'''
import json
D = json.loads(%(data)r)
T = lambda n, a: execute_tool(n, json.dumps(a))
def tag(a, label, folder):
    T("editor_toolset.toolsets.actor.ActorTools.add_tag", {"actor": a, "tag": "CityHK"})
    T("editor_toolset.toolsets.actor.ActorTools.set_label", {"actor": a, "label": label})
    T("editor_toolset.toolsets.scene.SceneTools.set_actor_folder", {"actor": a, "folder_path": folder})
def comp(a, cls):
    c = T("editor_toolset.toolsets.actor.ActorTools.get_components", {"actor": a, "component_type": {"refPath": cls}})["returnValue"]
    return c[0] if c else None
def run():
    if "Lvl_City" not in str(T("editor_toolset.toolsets.scene.SceneTools.get_current_level", {})["returnValue"]):
        return {"error": "wrong level"}
    for a in T("editor_toolset.toolsets.scene.SceneTools.find_actors", {"name": "", "tag": "CityHK", "collision_channels": []})["returnValue"]:
        T("editor_toolset.toolsets.scene.SceneTools.remove_from_scene", {"actor": a})
    errs = []
    for (lab, mesh, x, y, z, yaw, sx, sy, sz, mat, folder) in D["meshes"]:
        try:
            a = T("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset", {"asset_path": mesh, "name": lab,
                "xform": {"location": {"x": x, "y": y, "z": z}, "rotation": {"pitch": 0, "yaw": yaw, "roll": 0}, "scale": {"x": sx, "y": sy, "z": sz}}})["returnValue"]
            if mat:
                T("editor_toolset.toolsets.object.ObjectTools.set_properties", {"instance": comp(a, "/Script/Engine.StaticMeshComponent"), "values": json.dumps({"OverrideMaterials": [mat]})})
            tag(a, lab, folder)
        except Exception as e:
            errs.append(lab + ": " + str(e)[:120])
    for (lab, x, y, z, cd, r, g, b, rad) in D["lights"]:
        a = T("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_class", {"actor_type": {"refPath": "/Script/Engine.PointLight"}, "name": lab, "xform": {"location": {"x": x, "y": y, "z": z}}})["returnValue"]
        T("editor_toolset.toolsets.object.ObjectTools.set_properties", {"instance": comp(a, "/Script/Engine.PointLightComponent"), "values": json.dumps({
            "Mobility": "Movable", "IntensityUnits": "Candelas", "Intensity": cd, "LightColor": {"r": r, "g": g, "b": b, "a": 1},
            "AttenuationRadius": rad, "SourceRadius": 10, "VolumetricScatteringIntensity": 3.0, "CastShadows": not lab.startswith("CL_LampLight")})})
        tag(a, lab, "City/Lights")
    for (lab, txt, x, y, z, size) in D["texts"]:
        a = T("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_class", {"actor_type": {"refPath": "/Script/Engine.TextRenderActor"}, "name": lab,
            "xform": {"location": {"x": x, "y": y, "z": z}, "rotation": {"pitch": 0, "yaw": 180, "roll": 0}}})["returnValue"]
        T("editor_toolset.toolsets.object.ObjectTools.set_properties", {"instance": comp(a, "/Script/Engine.TextRenderComponent"), "values": json.dumps({
            "Text": txt, "WorldSize": size, "HorizontalAlignment": "EHTA_Center", "TextRenderColor": {"r": 200, "g": 205, "b": 190, "a": 255}})})
        tag(a, lab, "City/Clinic")
    sp = D["special"]
    for a in T("editor_toolset.toolsets.scene.SceneTools.find_actors", {"name": "PlayerStart", "tag": "", "collision_channels": []})["returnValue"]:
        x, y, z, yaw = sp["start"]
        T("editor_toolset.toolsets.actor.ActorTools.set_actor_transform", {"actor": a, "xform": {"location": {"x": x, "y": y, "z": z}, "rotation": {"pitch": 0, "yaw": yaw, "roll": 0}}, "worldspace": True})
    x, y, z, s = sp["phone"]
    a = T("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset", {"asset_path": "/Game/HollowKin/Blueprints/Interactables/BP_PhoneCall.BP_PhoneCall", "name": "CL_PhoneCall",
        "xform": {"location": {"x": x, "y": y, "z": z}, "scale": {"x": s, "y": s, "z": 1}}})["returnValue"]
    tag(a, "CL_PhoneCall", "City/Story")
    x, y, z, s = sp["door"]
    a = T("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset", {"asset_path": "/Game/HollowKin/Blueprints/Interactables/BP_LevelDoor.BP_LevelDoor", "name": "CL_ClinicDoor",
        "xform": {"location": {"x": x, "y": y, "z": z}, "scale": {"x": 0.6, "y": 0.8, "z": 1}}})["returnValue"]
    T("editor_toolset.toolsets.object.ObjectTools.set_properties", {"instance": a, "values": json.dumps({
        "TargetLevel": "/Game/HollowKin/Maps/Containment/Lvl_ContainmentWing",
        "Message": "St. Brigid's Clinic. The door is unlocked, just like Jaz said. The lobby is dark and stripped bare. Behind reception a service lift still has power, and only one button works: SUB-LEVEL 2."})})
    tag(a, "CL_ClinicDoor", "City/Story")
    x, y, z = sp["rain"]
    a = T("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset", {"asset_path": "/Game/HollowKin/FX/NS_Rain.NS_Rain", "name": "CL_Rain", "xform": {"location": {"x": x, "y": y, "z": z}}})["returnValue"]
    tag(a, "CL_Rain", "City/FX")
    for (lab, snd, vol) in D["sounds"]:
        a = T("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_class", {"actor_type": {"refPath": "/Script/Engine.AmbientSound"}, "name": lab, "xform": {"location": {"x": 0, "y": -800, "z": 300}}})["returnValue"]
        T("editor_toolset.toolsets.object.ObjectTools.set_properties", {"instance": comp(a, "/Script/Engine.AudioComponent"), "values": json.dumps({"Sound": snd, "VolumeMultiplier": vol, "bOverrideAttenuation": False})})
        tag(a, lab, "City/Audio")
    return {"errors": errs, "meshes": len(D["meshes"]), "lights": len(D["lights"])}
'''
SOUNDS = [
    ("CL_RainThunder", "/Game/Thunder_Sounds/CUE/CUE_Thunder_Lightning_Ambience_Field_recording_Cue.CUE_Thunder_Lightning_Ambience_Field_recording_Cue", 0.8),
    ("CL_TownAmbience", "/Game/Free_City_Ambiences/CUE/CUE_Free_City_AMB__3_Cue.CUE_Free_City_AMB__3_Cue", 0.25),
]
if __name__ == "__main__":
    print(TEMPLATE % {"data": json.dumps({"meshes": MESHES, "lights": LIGHTS, "texts": TEXTS, "special": SPECIAL, "sounds": SOUNDS})})

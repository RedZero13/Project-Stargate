#!/usr/bin/env python3
"""Places set dressing (pack props + ambient particle effects) in Lvl_ContainmentWing.
Everything gets the tag "SliceDress" and the Outliner folder Slice/Dressing; re-running replaces it.
usage: python3 tools/unreal_mcp/dress_slice.py > /tmp/dress.py, then run it with
       ProgrammaticToolset.execute_tool_script (see build_slice.py)."""
import json
VFX = "/Game/Realistic_Starter_VFX_Pack_Vol2/Particles/"
R = "/Game/Military_Radio/StaticMesh/"
ITEMS = [  # (label, asset, x, y, z, yaw, scale)
    ("D_C3_Lamp", "/Game/Tablelamp/Meshes/SM_Tablelamp.SM_Tablelamp", 3340, 200, 90, 200, 1.6),
    ("D_C3_Phone", R + "SM_Telephone.SM_Telephone", 3420, 180, 88, 170, 1.0),
    ("D_C3_Radio", R + "SM_Radio.SM_Radio", 2960, -250, 70, 0, 1.0),
    ("D_C1_Walkie", R + "SM_WalkieTalkie_LongAntenna.SM_WalkieTalkie_LongAntenna", 640, 220, 77, 35, 0.3),
    ("D_C7_Headphones", R + "SM_Headphones.SM_Headphones", 5230, -760, 200, 90, 0.45),
    ("FX_C2_Drip", VFX + "Water/P_Water_Dripping_A.P_Water_Dripping_A", 1650, -150, 295, 0, 1.0),
    ("FX_C2_Steam", VFX + "Smoke/P_Steam_A.P_Steam_A", 1360, 170, 20, 0, 0.6),
    ("FX_C2_Sparks", VFX + "Sparks/P_Sparks_A.P_Sparks_A", 2300, 0, 290, 0, 0.6),
    ("FX_C5_Drip", VFX + "Water/P_Water_Dripping_B.P_Water_Dripping_B", 4500, -1350, 345, 0, 1.0),
    ("FX_C7_Drip", VFX + "Water/P_Water_Dripping_A.P_Water_Dripping_A", 5900, -900, 295, 0, 1.0),
    ("FX_C9_Sparks", VFX + "Sparks/P_Sparks_B.P_Sparks_B", 5700, 170, 420, 0, 0.6),
]
DB = "/Game/DeadBodies_Poses_nikoff/"
POSES = [  # (label, skeletal mesh, pose animation, x, y, z, yaw): dead staff posed against walls
    ("D_C1_DeadGuard", DB + "Demo/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple",
     DB + "Animations/AS_DeadBody_Pose_Sit_01.AS_DeadBody_Pose_Sit_01", 480, -255, 0, 0),
    ("D_C5_DeadOrderly", DB + "Demo/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple",
     DB + "Animations/AS_DeadBody_Pose_Lie_04.AS_DeadBody_Pose_Lie_04", 4700, -800, 0, 60),
]
WS = "/Game/FD_WarningSigns_V1/Decals/MI_WarningSign_V1_"
DECALS = [  # (label, sign number, x, y, z, yaw): decal projects along its X axis, so yaw points into the wall
    ("S_C2_StopRun", 8, 1000, -200, 165, -90),
    ("S_C4_Biohazard", 11, 4250, 0, 210, 0),
    ("S_C5_NoLife", 7, 4800, -625, 170, 90),
    ("S_C7_Poison", 14, 5800, -725, 170, 90),
    ("S_C7_Stop", 9, 6500, -1350, 170, 0),
    ("S_C9_Radiation", 12, 5780, 120, 250, 0),
]
TEMPLATE = r'''
import json
ITEMS = json.loads(%(items)r)
POSES = json.loads(%(poses)r)
DECALS = json.loads(%(decals)r)
WS = %(ws)r
def T(name, args):
    return execute_tool(name, json.dumps(args))
def run():
    lvl = T("editor_toolset.toolsets.scene.SceneTools.get_current_level", {})["returnValue"]
    if "Lvl_ContainmentWing" not in str(lvl):
        return {"error": "wrong level " + str(lvl)}
    for a in T("editor_toolset.toolsets.scene.SceneTools.find_actors", {"name": "", "tag": "SliceDress", "collision_channels": []})["returnValue"]:
        T("editor_toolset.toolsets.scene.SceneTools.remove_from_scene", {"actor": a})
    out = []
    for (label, asset, x, y, z, yaw, s) in ITEMS:
        try:
            a = T("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset", {
                "asset_path": asset, "name": label,
                "xform": {"location": {"x": x, "y": y, "z": z}, "rotation": {"pitch": 0, "yaw": yaw, "roll": 0},
                          "scale": {"x": s, "y": s, "z": s}}})["returnValue"]
            T("editor_toolset.toolsets.actor.ActorTools.add_tag", {"actor": a, "tag": "SliceDress"})
            T("editor_toolset.toolsets.actor.ActorTools.set_label", {"actor": a, "label": label})
            T("editor_toolset.toolsets.scene.SceneTools.set_actor_folder", {"actor": a, "folder_path": "Slice/Dressing"})
            out.append(label)
        except Exception as e:
            out.append(label + " FAILED " + str(e)[:200])
    for (label, mesh, anim, x, y, z, yaw) in POSES:
        try:
            a = T("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset", {
                "asset_path": mesh, "name": label,
                "xform": {"location": {"x": x, "y": y, "z": z}, "rotation": {"pitch": 0, "yaw": yaw, "roll": 0}}})["returnValue"]
            comps = T("editor_toolset.toolsets.actor.ActorTools.get_components", {"actor": a, "component_type": {"refPath": "/Script/Engine.SkeletalMeshComponent"}})["returnValue"]
            T("editor_toolset.toolsets.object.ObjectTools.set_properties", {"instance": comps[0], "values": json.dumps({
                "AnimationMode": "AnimationSingleNode",
                "AnimationData": {"AnimToPlay": anim, "bSavedLooping": False, "bSavedPlaying": False, "SavedPosition": 0.0, "SavedPlayRate": 1.0}})})
            T("editor_toolset.toolsets.actor.ActorTools.add_tag", {"actor": a, "tag": "SliceDress"})
            T("editor_toolset.toolsets.actor.ActorTools.set_label", {"actor": a, "label": label})
            T("editor_toolset.toolsets.scene.SceneTools.set_actor_folder", {"actor": a, "folder_path": "Slice/Dressing"})
            out.append(label)
        except Exception as e:
            out.append(label + " FAILED " + str(e)[:300])
    for (label, num, x, y, z, yaw) in DECALS:
        try:
            a = T("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_class", {
                "actor_type": {"refPath": "/Script/Engine.DecalActor"}, "name": label,
                "xform": {"location": {"x": x, "y": y, "z": z}, "rotation": {"pitch": 0, "yaw": yaw, "roll": 0}}})["returnValue"]
            comps = T("editor_toolset.toolsets.actor.ActorTools.get_components", {"actor": a, "component_type": {"refPath": "/Script/Engine.DecalComponent"}})["returnValue"]
            T("editor_toolset.toolsets.object.ObjectTools.set_properties", {"instance": comps[0], "values": json.dumps({
                "DecalMaterial": WS + str(num) + ".MI_WarningSign_V1_" + str(num),
                "DecalSize": {"x": 12, "y": 45, "z": 45}, "RelativeRotation": {"pitch": 0, "yaw": 0, "roll": 0}})})
            T("editor_toolset.toolsets.actor.ActorTools.add_tag", {"actor": a, "tag": "SliceDress"})
            T("editor_toolset.toolsets.actor.ActorTools.set_label", {"actor": a, "label": label})
            T("editor_toolset.toolsets.scene.SceneTools.set_actor_folder", {"actor": a, "folder_path": "Slice/Dressing"})
            out.append(label)
        except Exception as e:
            out.append(label + " FAILED " + str(e)[:300])
    return {"placed": out}
'''
if __name__ == "__main__":
    print(TEMPLATE % {"items": json.dumps(ITEMS), "poses": json.dumps(POSES), "decals": json.dumps(DECALS), "ws": WS})

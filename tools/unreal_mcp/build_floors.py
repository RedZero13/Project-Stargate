#!/usr/bin/env python3
"""Builds the stacked floors from tools/floors_layout.py into the CURRENT level (docs/EXPANSION_PLAN.md).
usage: python3 build_floors.py wards Lvl_Wards        (deep Lvl_DeepLabs for B10-B15)
Everything placed gets the tag "Floors" (plus "Floor_<label>") and lives under the Outliner folder Floors/<label>/.
Runs one floor at a time (keeps each editor script short). Re-runnable: removes that floor's previous build first.
Furniture: Horror Hospital meshes; each prop is dropped so its bounding box sits on the floor."""
import json, sys, os, subprocess
from ui_lib import call
from build_slice import MATS
HH = '/Game/Horror_Hospital/Meshes/'
KINDS = {
    'bed': 'SM_Bed_01_p03', 'iv': 'SM_IVstand_01_v02', 'stretcher': 'SM_Stretcher_02_v01', 'treat': 'SM_Treatment_Table_06_v01',
    'wheelchair': 'SM_Wheel_Chair_01_v01', 'xray': 'SM_Fluoragrapht_01_v01', 'angio': 'SM_Angiography_Scanner_01_v1',
    'angiomon': 'SM_Angiography_Monitors_01_v1', 'anesth': 'SM_Anesthesia_Machine_01_v01', 'bloodtest': 'SM_Blood_Test_Machine_v01',
    'fume': 'SM_Fume_Cupboard_v02', 'micro': 'SM_Pathology_Microscope_01_v01', 'fridge': 'SM_Fridge_Tall_01_v3', 'rack': 'SM_Rack_06_v01',
    'wastebin': 'SM_Medical_Waste_Bin_02_v01', 'curtain': 'SM_Curtain_01_v5', 'bedside': 'SM_Bedside_Table_04_p01',
    'cabinet': 'SM_Cabinet_01_p3', 'desk': 'SM_Desk_01_p02', 'chair': 'SM_Office_Chair_01_v01', 'monitor': 'SM_Computer_Monitor_01_v01',
    'barrier': 'SM_Medical_Barrier_01_p02', 'dentist': 'SM_Dentist_Chair_01_v01', 'scanmon': 'SM_Scanner_Monitor_01_v1',
    'beddev': 'SM_Bed_Devices_01_v01', 'bloodcab': 'SM_Blood_Cabinet_01_v01', 'cam': 'SM_Security_Cam_01_v01', 'lift': 'SM_Lift_02_p02',
    'reception': 'SM_Reception_02_v01', 'bench': 'SM_Bench_01_v01', 'disinf': 'SM_Disinfector_03_v01', 'cylinder': 'SM_Cylinder_01_v01',
    'tray': 'SM_Tray_02_v02', 'washstand': 'SM_Washstand_02_v1', 'sign_xray': 'SM_Sign_Text_Radiology_X_Ray', 'sign_surgery': 'SM_Sign_Text_Surgery',
    'sign_nursery': 'SM_Sign_Text_Nursery', 'sign_lab': 'SM_Sign_Text_Laboratory', 'sign_reception': 'SM_Sign_Text_Reception',
}
ON_DESK = {'monitor', 'micro'}          # sit on a desk (75 cm) instead of the floor
WALL = {'cam'}                          # mounted high
TEMPLATE = r'''
import json
D = json.loads(%(data)r)
MATS = json.loads(%(mats)r)
LABEL = %(label)r
def T(name, args):
    return execute_tool(name, json.dumps(args))
def tagit(a, folder, lbl):
    T("editor_toolset.toolsets.actor.ActorTools.add_tag", {"actor": a, "tag": "Floors"})
    T("editor_toolset.toolsets.actor.ActorTools.add_tag", {"actor": a, "tag": "Floor_" + LABEL})
    T("editor_toolset.toolsets.actor.ActorTools.set_label", {"actor": a, "label": lbl})
    T("editor_toolset.toolsets.scene.SceneTools.set_actor_folder", {"actor": a, "folder_path": "Floors/" + LABEL + "/" + folder})
def run():
    for a in T("editor_toolset.toolsets.scene.SceneTools.find_actors", {"name": "", "tag": "Floor_" + LABEL, "collision_channels": []})["returnValue"]:
        T("editor_toolset.toolsets.scene.SceneTools.remove_from_scene", {"actor": a})
    n = 0; bad = []
    for b in D["boxes"]:
        a = T("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset", {
            "asset_path": "/Game/LevelPrototyping/Meshes/SM_Cube.SM_Cube", "name": b["name"],
            "xform": {"location": {"x": b["x"], "y": b["y"], "z": b["z"]},
                      "scale": {"x": b["sx"] / 100.0, "y": b["sy"] / 100.0, "z": b["sz"] / 100.0}}})["returnValue"]
        T("editor_toolset.toolsets.object.ObjectTools.set_properties", {"instance": {"refPath": a["refPath"] + ".StaticMeshComponent0"},
            "values": json.dumps({"OverrideMaterials": [MATS.get(b["mat"], MATS["prop"])]})})
        T("editor_toolset.toolsets.actor.ActorTools.add_tag", {"actor": a, "tag": "M_" + b["mat"]})
        tagit(a, "Geometry", b["name"]); n += 1
    for l in D["lights"]:
        a = T("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_class", {"actor_type": {"refPath": "/Script/Engine.PointLight"},
            "name": l["name"], "xform": {"location": {"x": l["x"], "y": l["y"], "z": l["z"]}}})["returnValue"]
        T("editor_toolset.toolsets.object.ObjectTools.set_properties", {"instance": {"refPath": a["refPath"] + ".LightComponent0"},
            "values": json.dumps({"Mobility": "Movable", "IntensityUnits": "Candelas", "Intensity": l["i"],
                "LightColor": {"r": l["r"], "g": l["g"], "b": l["b"], "a": 1.0}, "AttenuationRadius": l["rad"], "SourceRadius": 8,
                "CastShadows": ("_LC" not in l["name"])})})
        tagit(a, "Lights", l["name"]); n += 1
    for i, f in enumerate(D["furnish"]):
        try:
            a = T("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset", {"asset_path": f["mesh"], "name": "%%s_%%s_%%d" %% (LABEL, f["kind"], i),
                "xform": {"location": {"x": f["x"], "y": f["y"], "z": f["z"] + 200}, "rotation": {"pitch": 0, "yaw": f["yaw"], "roll": 0}}})["returnValue"]
            bb = T("editor_toolset.toolsets.actor.ActorTools.get_actor_bounds", {"actor": a})["returnValue"]
            dz = f["z"] + f["lift"] - bb["min"]["z"]
            T("editor_toolset.toolsets.actor.ActorTools.set_actor_transform", {"actor": a, "xform": {"location": {"x": f["x"], "y": f["y"], "z": f["z"] + 200 + dz},
                "rotation": {"pitch": 0, "yaw": f["yaw"], "roll": 0}}, "worldspace": True})
            tagit(a, "Props", "%%s_%%s_%%d" %% (LABEL, f["kind"], i)); n += 1
        except Exception as e:
            bad.append(f["kind"] + ": " + str(e)[:120])
    return {"placed": n, "failed": bad[:10]}
'''
def floor_data(d, fl):
    z = fl['z']
    pre = fl['label'] + '_'
    boxes = [b for b in d['boxes'] if b['name'].startswith(pre)]
    lights = [l for l in d['lights'] if l['name'].startswith(pre)]
    furn = []
    for f in d['furnish']:
        if f['z'] != z: continue
        k = f['kind']
        lift = 75 if k in ON_DESK else 230 if k in WALL else (f.get('dz', 0) if k.startswith('sign') else 0)
        g = dict(f, mesh=HH + KINDS[k] + '.' + KINDS[k], lift=lift)
        if k.startswith('sign'):
            g['lift'] = 0; g['z'] = f['z']        # signs keep their own height (z already +250 in the layout)
        furn.append(g)
    return dict(boxes=boxes, lights=lights, furnish=furn)

if __name__ == '__main__':
    m, level = sys.argv[1], sys.argv[2]
    only = sys.argv[3:]                                   # optional floor labels
    here = os.path.dirname(os.path.abspath(__file__))
    d = json.loads(subprocess.check_output([sys.executable, os.path.join(here, '..', 'floors_layout.py'), m]))
    lvl = str(call('editor_toolset.toolsets.scene.SceneTools', 'get_current_level', {})['returnValue'])
    assert level in lvl, 'open ' + level + ' first (current: ' + lvl + ')'
    for fl in d['floors']:
        if only and fl['label'] not in only: continue
        code = TEMPLATE % {'data': json.dumps(floor_data(d, fl)), 'mats': json.dumps(MATS), 'label': fl['label']}
        r = call('editor_toolset.toolsets.programmatic.ProgrammaticToolset', 'execute_tool_script', {'script': code})
        print(fl['label'], fl['name'], str(r)[:300])
    print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': []}))
    json.dump(d['floors'], open(os.path.join(here, 'floors_%s.json' % m), 'w'), indent=1)

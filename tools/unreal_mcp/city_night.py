"""Turns Lvl_City (copy of the Assetsville Town demo map) into a rainy night. Re-runnable.
usage: python3 tools/unreal_mcp/city_night.py > /tmp/n.py, run it with ProgrammaticToolset.execute_tool_script."""
SCRIPT = r'''
import json
T = lambda n, a: execute_tool(n, json.dumps(a))
def find(name):
    return [a for a in T("editor_toolset.toolsets.scene.SceneTools.find_actors", {"name": name[:3], "tag": "", "collision_channels": []})["returnValue"]
            if a["refPath"].endswith("." + name)]
def comp(a, cls):
    c = T("editor_toolset.toolsets.actor.ActorTools.get_components", {"actor": a, "component_type": {"refPath": cls}})["returnValue"]
    return c[0] if c else None
def setp(o, v):
    try:
        return T("editor_toolset.toolsets.object.ObjectTools.set_properties", {"instance": o, "values": json.dumps(v)})["returnValue"]
    except Exception as e:
        return str(e)[:200]
def run():
    if "Lvl_City" not in str(T("editor_toolset.toolsets.scene.SceneTools.get_current_level", {})["returnValue"]):
        return {"error": "wrong level"}
    out = {}
    for a in find("LightSource"):
        c = comp(a, "/Script/Engine.DirectionalLightComponent")
        out["moon"] = setp(c, {"Intensity": 0.06, "LightColor": {"r": 0.55, "g": 0.65, "b": 1.0, "a": 1}, "bAtmosphereSunLight": False})
        T("editor_toolset.toolsets.actor.ActorTools.set_actor_transform", {"actor": a, "xform": {"rotation": {"pitch": -35, "yaw": 120, "roll": 0}}, "worldspace": True})
    for a in find("SkyLight_1"):
        c = comp(a, "/Script/Engine.SkyLightComponent")
        out["sky"] = setp(c, {"Intensity": 0.04, "LightColor": {"r": 0.45, "g": 0.55, "b": 0.85, "a": 1}, "bLowerHemisphereIsBlack": True})
    for n in ("SkySphere", "AtmosphericFog_1"):
        for a in find(n):
            out[n] = setp(a, {"bHidden": True})
    for a in find("ExponentialHeightFog_1"):
        c = comp(a, "/Script/Engine.ExponentialHeightFogComponent")
        out["fog"] = setp(c, {"FogDensity": 0.035, "FogHeightFalloff": 0.12, "StartDistance": 0.0,
            "FogInscatteringLuminance": {"r": 0.004, "g": 0.005, "b": 0.009, "a": 1}, "DirectionalInscatteringLuminance": {"r": 0, "g": 0, "b": 0, "a": 1},
            "bEnableVolumetricFog": True, "VolumetricFogScatteringDistribution": 0.55, "VolumetricFogExtinctionScale": 1.5})
    for a in find("PostProcessVolume_1"):
        out["pp"] = setp(a, {"bUnbound": True, "Settings": {
            "bOverride_AutoExposureMinBrightness": True, "AutoExposureMinBrightness": -2.0,
            "bOverride_AutoExposureMaxBrightness": True, "AutoExposureMaxBrightness": -0.5,
            "bOverride_AutoExposureBias": True, "AutoExposureBias": -1.5,
            "bOverride_ColorSaturation": True, "ColorSaturation": {"x": 0.75, "y": 0.8, "z": 0.95, "w": 0.85},
            "bOverride_VignetteIntensity": True, "VignetteIntensity": 0.55,
            "bOverride_FilmGrainIntensity": True, "FilmGrainIntensity": 0.25}})
    return out
'''
if __name__ == "__main__":
    print(SCRIPT)

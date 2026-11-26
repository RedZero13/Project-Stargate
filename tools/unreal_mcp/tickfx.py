"""BP_Max.TickFX: drives WBP_ScreenFX each frame (damage/sanity overlays, blood, reticle, and the HUD ring)."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
FX = '(Variables|Default|GetScreenFXRef)'
dsl = '''(fn TickFX ()
  (Utilities|IsValid %(fx)s
    (:"Is Valid"
      (Class|WBPScreenFX|UpdateFX :self %(fx)s :Sanity (Variables|Default|GetSanity) :Hurt (* (Variables|Default|GetHurtFlash) (select (Variables|Default|GetReduceFlash) 0.3 1.0)))
      (Class|WBPScreenFX|SetBlood :self %(fx)s :Amount (Math|Float|Clamp(Float) (+ (* (/ (- 50.0 (Variables|Default|GetHealth)) 50.0) 0.75) (* (Variables|Default|GetHurtFlash) 0.45)) 0.0 0.9))
      (Class|WBPScreenFX|SetAim :self %(fx)s :Aiming (Variables|Default|GetAiming))
      (Class|WBPScreenFX|UpdateRing :self %(fx)s :Ammo (Variables|Default|GetAmmo) :Reserve (Variables|Default|GetReserveAmmo) :Health (Variables|Default|GetHealth) :Aiming (Variables|Default|GetAiming))
      (Class|WBPScreenFX|SetRingShown :self %(fx)s :Shown (Variables|Default|GetHasPistol)))
    (:"Is Not Valid"
      (bind w (Utilities|Casting|CastToWBP_ScreenFX (UserInterface|CreateWidget "/Game/HollowKin/UI/Diegetic/WBP_ScreenFX.WBP_ScreenFX_C" (Game|GetPlayerController 0))))
      (Variables|Default|SetScreenFXRef w)
      (UserInterface|Viewport|AddToViewport w 5))))''' % {'fx': FX}
print(call(BT, 'write_graph_dsl', {'graph': {'refPath': MAX + ':TickFX'}, 'code': dsl}))

import json,urllib.request
M='/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
BPT='editor_toolset.toolsets.blueprint.BlueprintTools'
def T(tag,cls='ActorComponent'): return f'(Utilities|Array|Get(acopy) (Actor|GetComponentsbyTag :ComponentClass "/Script/Engine.{cls}" :Tag "{tag}") 0)'
def call(tool,args):
    SID=open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'sid')).read().strip()
    p={'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'call_tool','arguments':{'toolset_name':BPT,'tool_name':tool,'arguments':args}}}
    r=urllib.request.Request('http://127.0.0.1:8000/mcp',json.dumps(p).encode(),{'Content-Type':'application/json','Accept':'application/json, text/event-stream','Mcp-Session-Id':SID})
    d=json.load(urllib.request.urlopen(r,timeout=120)); res=d['result']; return ''.join(c.get('text','') for c in res['content'])
def w(name,dsl):
    r=call('write_graph_dsl',{'graph':{'refPath':f'{M}:{name}'},'code':dsl}); print(name,r[:260])
def SC(var,tag,body,extra=''): return f'(bind {var} (Utilities|Casting|CastToSceneComponent :Object {T(tag)})\n  (:then\n{body})\n  (:CastFailed))'
HUDP='/Game/HollowKin/UI/HUD/WBP_HUD.WBP_HUD_C'
w('AimFlashlight',f'''(fn AimFlashlight ()
  (bind pm (Utilities|Casting|CastToStaticMeshComponent :Object {T('Pistol')})
    (:then
      (if (not (Variables|Default|GetFlashlightAttached))
        (Transformation|AttachComponentToComponent :self pm :Parent (Variables|Character|GetMesh) :SocketName "hand_r" :LocationRule "SnapToTarget" :RotationRule "SnapToTarget" :ScaleRule "KeepWorld")
        (Collision|SetCollisionEnabled :self pm :NewType "NoCollision"))
      (Rendering|SetVisibility :self pm :bNewVisibility (Variables|Default|GetAiming) :bPropagateToChildren false)
      (bind sl (Utilities|Casting|CastToSpotLightComponent :Object {T('Flashlight')})
        (:then
          (bind wrist (Utilities|Casting|CastToSceneComponent :Object {T('Wrist')})
            (:then
              (if (not (Variables|Default|GetFlashlightAttached))
                (Transformation|AttachComponentToComponent :self sl :Parent (Variables|Character|GetMesh) :SocketName "hand_l" :LocationRule "SnapToTarget" :RotationRule "KeepWorld" :ScaleRule "KeepWorld")
                (Transformation|AttachComponentToComponent :self wrist :Parent (Variables|Character|GetMesh) :SocketName "spine_03" :LocationRule "KeepRelative" :RotationRule "KeepRelative" :ScaleRule "KeepRelative")
                (Variables|Default|SetFlashlightAttached true))
              (bind aim (Pawn|GetBaseAimRotation))
              (bind face (Transformation|GetActorRotation))
              (Transformation|SetWorldRotation :self sl :NewRotation (Math|Rotator|MakeRotator :Roll 0.0 :Pitch (.pitch aim) :Yaw (.yaw face))))
            (:CastFailed)))
        (:CastFailed)))
    (:CastFailed)))
''')
w('HideMuzzleFlash','(fn HideMuzzleFlash ()\n  '+SC('mz','Muzzle','    (Rendering|SetVisibility :self mz :bNewVisibility false :bPropagateToChildren false)')+')\n')
w('MuzzleFx','(fn MuzzleFx (Target)\n  '+SC('pst','Pistol','''    (Rendering|Debug|DrawDebugLine :LineStart (Transformation|GetWorldLocation pst) :LineEnd Target :LineColor "(R=1.0,G=0.8,B=0.4,A=1.0)" :Duration 0.06 :Thickness 1.5)
    (bind mz (Utilities|Casting|CastToSceneComponent :Object '''+T('Muzzle')+''')
      (:then
        (Rendering|SetVisibility :self mz :bNewVisibility true :bPropagateToChildren false)
        (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "HideMuzzleFlash" :Time 0.06 :bLooping false))
      (:CastFailed))''')+')\n')
w('FirePistol','''(fn FirePistol ()
  (bind now (Utilities|Time|GetTimeSeconds))
  (if (and (and (Variables|Default|GetAiming) (> (Variables|Default|GetAmmo) 0)) (>= (- now (Variables|Default|GetLastFireTime)) (Variables|Default|GetFireInterval)))
    (Variables|Default|SetLastFireTime now)
    (Variables|Default|SetAmmo (- (Variables|Default|GetAmmo) 1))
    (bind cam (Game|GetPlayerCameraManager :PlayerIndex 0))
    (bind start (Camera|GetCameraLocation :self cam))
    (bind fwd (Math|Vector|GetForwardVector :InRot (Camera|GetCameraRotation :self cam)))
    (bind finish (+ start (* fwd (Variables|Default|GetPistolRange))))
    (bind (hit ok) (Collision|LineTraceByChannel :Start start :End finish :TraceChannel "TraceTypeQuery1" :bIgnoreSelf true :DrawDebugType "None"))
    (bind (_a _b _c _d _e impact _g _h _i hitActor) (Collision|BreakHitResult hit))
    (if ok
      (Game|Damage|ApplyDamage :DamagedActor hitActor :BaseDamage (Variables|Default|GetPistolDamage) :EventInstigator (Pawn|GetController) :DamageCauser self))
    (CallFunction|MuzzleFx :Target (select ok impact finish))))
''')
w('TickVitals','''(fn TickVitals (DeltaSeconds)
  (bind sl (Utilities|Casting|CastToSpotLightComponent :Object '''+T('Flashlight')+''')
    (:then
      (if (not (Rendering|IsVisible :self sl))
        (Variables|Default|SetSanity (Math|Float|Clamp(Float) (- (Variables|Default|GetSanity) (* DeltaSeconds 0.6)) 0.0 100.0)))
      (Variables|Default|SetHurtFlash (Math|Float|Clamp(Float) (- (Variables|Default|GetHurtFlash) (* DeltaSeconds 2.0)) 0.0 1.0))
      (CallFunction|TickFX)
      (CallFunction|TickOverlay)
      (CallFunction|TickDiegetic))
    (:CastFailed)))
''')
w('TickOverlay',f'''(fn TickOverlay ()
  (if (Variables|Default|GetShowOverlayHUD)
    (Utilities|IsValid (Variables|Default|GetHUDRef)
      (:"Is Valid"
        (Widget|SetVisibility :self (Variables|Default|GetHUDRef) :InVisibility "HitTestInvisible")
        (Class|WBPHUD|UpdateHUD :self (Variables|Default|GetHUDRef) :Health (Variables|Default|GetHealth) :Sanity (Variables|Default|GetSanity) :Ammo (Variables|Default|GetAmmo) :Reserve (Variables|Default|GetReserveAmmo) :Aiming (Variables|Default|GetAiming) :Hurt 0.0))
      (:"Is Not Valid"
        (bind made (UserInterface|CreateWidget :Class "{HUDP}" :OwningPlayer (Game|GetPlayerController :PlayerIndex 0)))
        (bind wc (Utilities|Casting|CastToWBP_HUD :Object made)
          (:then
            (Variables|Default|SetHUDRef wc)
            (UserInterface|Viewport|AddtoViewport :self wc :ZOrder 0))
          (:CastFailed))))
    (else
      (Utilities|IsValid (Variables|Default|GetHUDRef)
        (:"Is Valid"
          (Widget|SetVisibility :self (Variables|Default|GetHUDRef) :InVisibility "Hidden"))
        (:"Is Not Valid")))))
''')
w('TickDiegetic','''(fn TickDiegetic ()
  (bind wcomp (Utilities|Casting|CastToWidgetComponent :Object '''+T('Wrist')+''')
    (:then
      (bind ww (Utilities|Casting|CastToWBP_WristMonitor :Object (UserInterface|GetUserWidgetObject :self wcomp))
        (:then
          (Class|WBPWristMonitor|UpdateMonitor :self ww :Health (Variables|Default|GetHealth) :Sanity (Variables|Default|GetSanity))
          (bind gcomp (Utilities|Casting|CastToWidgetComponent :Object '''+T('Gun')+''')
            (:then
              (bind gw (Utilities|Casting|CastToWBP_GunDisplay :Object (UserInterface|GetUserWidgetObject :self gcomp))
                (:then
                  (Class|WBPGunDisplay|UpdateGun :self gw :Ammo (Variables|Default|GetAmmo) :Reserve (Variables|Default|GetReserveAmmo)))
                (:CastFailed)))
            (:CastFailed)))
        (:CastFailed)))
    (:CastFailed)))
''')

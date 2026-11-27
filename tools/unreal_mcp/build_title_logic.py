"""WBP_MainMenu intro (Control-style): Phase 0 company logo -> 1 splash card -> 2 content warning -> 3 title (logo over drifting
smoke, PRESS ANY KEY pulsing) -> 4 menu fades/slides in. Any key or click skips ahead. The splash plays once per
launch (BP_HKGameInstance.bIntroDone); returning from the game goes straight to the menu."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
U = 'UMGToolSet.UMGToolSet'
MM = '/Game/HollowKin/UI/Menus/WBP_MainMenu.WBP_MainMenu'
MENU = ['Left', 'Card', 'FrameT', 'FrameB', 'FrameL', 'FrameR', 'CTLh', 'CTRh', 'CBLh', 'CBRh', 'CTLv', 'CTRv', 'CBLv', 'CBRv', 'Build']
for n in MENU:
    call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': {'refPath': MM}, 'widget': {'refPath': MM + ':WidgetTree.' + n}, 'bIsVariable': True})
B = {'refPath': MM}
call(BT, 'add_variable', {'blueprint': B, 'name': 'Phase', 'type_name': 'int'})
call(BT, 'add_variable', {'blueprint': B, 'name': 'PT', 'type_name': 'float'})
def G(n): return '(Variables|WBP_MainMenu|Get%s)' % n
def op(n, expr): return '(Widget|SetRenderOpacity %s %s)' % (G(n), expr)
def cl(e): return '(Math|Float|Clamp(Float) %s 0.0 1.0)' % e
def fn(name, params, dsl, ptypes=None):
    call(BT, 'add_function_graph', {'blueprint': B, 'graph_name': name})
    for p in params:
        call(BT, 'add_function_param', {'graph': {'refPath': MM + ':' + name}, 'param_name': p, 'param_type': (ptypes or {}).get(p, 'float'), 'input_param': True})
    print(name, call(BT, 'write_graph_dsl', {'graph': {'refPath': MM + ':' + name}, 'code': dsl}))
alpha = '\n  '.join(op(n, 'A') for n in MENU)
fn('SetMenuAlpha', ['A'], '''(fn SetMenuAlpha (A)
  %s
  (Widget|Transform|SetRenderTranslation %s (Math|Vector2D|MakeVector2D (* (- 1.0 A) -110.0) 0.0))
  (if (> A 0.5)
    (Widget|SetVisibility %s "SelfHitTestInvisible")
    (else (Widget|SetVisibility %s "HitTestInvisible"))))''' % (alpha, G('Left'), G('Left'), G('Left')))
fade = lambda t_end: '(Math|Float|Min(Float) %s %s)' % (cl('(/ t 0.7)'), cl('(/ (- %s t) 0.7)' % t_end))
fn('AnimTick', ['Dt'], '''(fn AnimTick (Dt)
  (Variables|Default|SetPT (+ (Variables|Default|GetPT) Dt))
  (bind t (Variables|Default|GetPT))
  (switch int (Variables|Default|GetPhase)
    (:0
      %(co)s
      (Widget|Transform|SetRenderScale %(G_co)s (Math|Vector2D|MakeVector2D (+ 0.97 (* t 0.02)) (+ 0.97 (* t 0.02))))
      (if (> t 4.6) (Variables|Default|SetPhase 1) (Variables|Default|SetPT 0.0)))
    (:1
      %(cooff)s
      %(s1)s
      (if (> t 3.4) (Variables|Default|SetPhase 2) (Variables|Default|SetPT 0.0)))
    (:2
      %(s1off)s
      %(s2)s
      (if (> t 4.4) (Variables|Default|SetPhase 3) (Variables|Default|SetPT 0.0)))
    (:3
      %(cooff)s
      %(s1off)s
      %(s2off)s
      %(logo)s
      %(smoke)s
      %(press)s
      %(copy)s)
    (:Default
      %(cooff)s
      %(s1off)s
      %(s2off)s
      %(smoke1)s
      %(logoout)s
      %(pressout)s
      %(copy1)s
      (CallFunction|SetMenuAlpha :A %(menu)s))))''' % {
    'co': op('SplashCo', fade(4.6)), 'cooff': op('SplashCo', '0.0'), 'G_co': G('SplashCo'),
    's1': op('Splash1', fade(3.4)), 's1off': op('Splash1', '0.0'),
    's2': op('Splash2', fade(4.4)), 's2off': op('Splash2', '0.0'),
    'logo': op('TitleImg', cl('(/ t 1.6)')), 'smoke': op('BgSmoke', cl('(/ t 2.5)')), 'smoke1': op('BgSmoke', '1.0'),
    'press': op('PressText', '(* %s (+ 0.55 (* 0.45 (Math|Trig|Sin(Radians) (* t 3.0)))))' % cl('(- t 1.6)')),
    'copy': op('Copyright', cl('(- (/ t 1.6) 0.5)')), 'copy1': op('Copyright', '0.8'),
    'logoout': op('TitleImg', cl('(- 1.0 (* t 2.5))')), 'pressout': op('PressText', '0.0'),
    'menu': cl('(* (- t 0.25) 1.8)')})
fn('AnyKey', [], '''(fn AnyKey ()
  (if (< (Variables|Default|GetPhase) 3)
    (Variables|Default|SetPhase 3)
    (Variables|Default|SetPT 0.0)
    (else
      (if (== (Variables|Default|GetPhase) 3)
        (Variables|Default|SetPhase 4)
        (Variables|Default|SetPT 0.0)
        (Audio|PlaySound2D "/Game/Interface_And_Item_Sounds/WAV/Futuristic_Click_04.Futuristic_Click_04" 0.7)))))''')
fn('IntroStart', [], '''(fn IntroStart ()
  (CallFunction|SetMenuAlpha :A 0.0)
  (Variables|Interaction|SetIsFocusable :bIsFocusable true)
  (Widget|SetKeyboardFocus self)
  (bind gi (Utilities|Casting|CastToBP_HKGameInstance (Widget|GetGameInstance))
    (:then
      (if (Class|BPHKGameInstance|GetIntroDone :self gi)
        (Variables|Default|SetPhase 4)
        (Variables|Default|SetPT 5.0)
        (else
          (Variables|Default|SetPhase 0)
          (Variables|Default|SetPT 0.0)
          (Class|BPHKGameInstance|SetIntroDone :self gi :bIntroDone true))))
    (:CastFailed (Variables|Default|SetPhase 0))))''')
for name in ('OnKeyDown', 'OnMouseButtonDown'):
    call(BT, 'add_function_graph', {'blueprint': B, 'graph_name': name})
    g = MM + ':' + name
    args = 'MyGeometry InKeyEvent' if name == 'OnKeyDown' else 'MyGeometry MouseEvent'
    print(name, call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': '''(fn %s (%s)
  (if (< (Variables|Default|GetPhase) 4)
    (CallFunction|AnyKey)
    (return (Widget|EventReply|Handled))
    (else (return (Widget|EventReply|Unhandled)))))''' % (name, args)}))
fn('MenuVolumes', [], '''(fn MenuVolumes ()
  (bind sv (Utilities|Casting|CastToBP_SettingsSave (SaveGame|LoadGameFromSlot "HollowKinSettings" 0))
    (:then (Class|BPSettingsSave|ApplyVolumes :self sv :Ctx self))
    (:CastFailed)))''')
print('Construct', call(BT, 'write_graph_dsl', {'graph': {'refPath': MM + ':EventGraph'}, 'code': '''(event UserInterface|EventConstruct
  (Development|ExecuteConsoleCommand "stat none")
  (CallFunction|IntroStart)
  (CallFunction|MenuVolumes))'''}))
print('Tick', call(BT, 'write_graph_dsl', {'graph': {'refPath': MM + ':EventGraph'}, 'code': '''(event UserInterface|EventTick (MyGeometry InDeltaTime)
  (CallFunction|AnimTick :Dt InDeltaTime))'''}))

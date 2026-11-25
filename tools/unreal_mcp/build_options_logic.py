"""Logic for the 007-style Options page (WBP_Settings): value-only labels, new settings (sensitivity, invert Y,
motion blur, text size), category switching, hover descriptions with default values, Esc/P to go back,
and applying changes live to Max and the HUD."""
from ui_lib import call
from options_spec import PAGES
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
UM = 'UMGToolSet.UMGToolSet'
SET = '/Game/HollowKin/UI/Menus/WBP_Settings.WBP_Settings'
B = {'refPath': SET}
SAVE_C = '/Game/HollowKin/Blueprints/Systems/BP_SettingsSave.BP_SettingsSave_C'
def fn(name, dsl, params=()):
    call(BT, 'add_function_graph', {'blueprint': B, 'graph_name': name})
    for p, t in params:
        call(BT, 'add_function_param', {'graph': {'refPath': SET + ':' + name}, 'param_name': p, 'param_type': t, 'input_param': True})
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': SET + ':' + name}, 'code': dsl})
    if not isinstance(r, dict) or r.get('returnValue') is not None: print(name, str(r)[:300])
def G(n): return '(Variables|WBP_Settings|Get%s)' % n
def setlabel(btn, expr): return '(Widget|SetText(Text) %s (Utilities|Text|ToText(String) %s))' % (G(btn + 'Label'), expr)
def onoff(btn, cond): return '(if %s %s (else %s))' % (cond, setlabel(btn, '"ON"'), setlabel(btn, '"OFF"'))
def pct(btn, expr): return setlabel(btn, '(Utilities|String|BuildString(Integer) :Prefix "" :InInt %s :Suffix "%%")' % expr)
SV = lambda v: '(Class|BPSettingsSave|Get%s :self s)' % v
# ---------- labels ----------
fn('RefreshLabels', '''(fn RefreshLabels ()
  (CallFunction|RefreshGraphics)
  (bind s (Utilities|Casting|CastToBP_SettingsSave (SaveGame|LoadGameFromSlot "HollowKinSettings" 0))
    (:then
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      (if %s %s (else %s)))
    (:CastFailed
      %s %s %s %s %s %s %s %s %s)))''' % (
    onoff('BtnOverlay', SV('OverlayHUD')), onoff('BtnFlash', SV('ReduceFlash')),
    pct('BtnMaster', SV('MasterVol')), pct('BtnMusic', SV('MusicVol')), pct('BtnSfx', SV('SfxVol')),
    pct('BtnSens', SV('LookSens')), onoff('BtnInvert', SV('InvertY')),
    onoff('BtnMotionBlur', '(not %s)' % SV('NoMotionBlur')),
    SV('LargeText'), setlabel('BtnTextSize', '"LARGE"'), setlabel('BtnTextSize', '"NORMAL"'),
    setlabel('BtnOverlay', '"OFF"'), setlabel('BtnFlash', '"OFF"'), setlabel('BtnMaster', '"100%"'), setlabel('BtnMusic', '"100%"'),
    setlabel('BtnSfx', '"100%"'), setlabel('BtnSens', '"100%"'), setlabel('BtnInvert', '"OFF"'), setlabel('BtnMotionBlur', '"ON"'),
    setlabel('BtnTextSize', '"NORMAL"')))
GUS = '(Settings|GetGameUserSettings)'
fn('RefreshGraphics', '''(fn RefreshGraphics ()
  (bind g %(g)s)
  %(res)s
  (if (Settings|IsVSyncEnabled :self g) %(von)s (else %(voff)s))
  (if (Class|BPSettingsSave|GetWindowed :self (Utilities|Casting|CastToBP_SettingsSave (SaveGame|LoadGameFromSlot "HollowKinSettings" 0))) %(win)s (else %(full)s))
  (if (< (Settings|GetFrameRateLimit :self g) 1.0) %(funl)s
    (else %(fnum)s))
  (switch int (Settings|GetOverallScalabilityLevel :self g)
    (:0 %(q0)s)
    (:1 %(q1)s)
    (:2 %(q2)s)
    (:Default %(q3)s)))''' % {
    'g': GUS, 'res': pct('BtnResScale', '(Math|Float|Round (* (Settings|GetResolutionScaleNormalized :self g) 100.0))'),
    'von': setlabel('BtnVsync', '"ON"'), 'voff': setlabel('BtnVsync', '"OFF"'),
    'win': setlabel('BtnWindow', '"WINDOWED"'), 'full': setlabel('BtnWindow', '"FULLSCREEN"'),
    'funl': setlabel('BtnFps', '"UNLIMITED"'),
    'fnum': setlabel('BtnFps', '(Utilities|String|BuildString(Integer) :Prefix "" :InInt (Math|Float|Round (Settings|GetFrameRateLimit :self g)) :Suffix "")'),
    'q0': setlabel('BtnQuality', '"LOW"'), 'q1': setlabel('BtnQuality', '"MEDIUM"'), 'q2': setlabel('BtnQuality', '"HIGH"'), 'q3': setlabel('BtnQuality', '"EPIC"')})
# ---------- live apply ----------
fn('ApplyLive', '''(fn ApplyLive ()
  (for w (Widget|GetAllWidgetsOfClass "/Game/HollowKin/UI/Diegetic/WBP_ScreenFX.WBP_ScreenFX_C" false)
    (Class|WBPScreenFX|ApplyTextSize :self (Utilities|Casting|CastToWBP_ScreenFX w)))
  (bind m (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))
    (:then (Class|BPMax|ApplyMaxSettings :self m))
    (:CastFailed)))''')
# ---------- save-backed toggles ----------
def save_edit(name, set_expr_existing, set_expr_new):
    fn(name, '''(fn %s ()
  (bind s (Utilities|Casting|CastToBP_SettingsSave (SaveGame|LoadGameFromSlot "HollowKinSettings" 0))
    (:then
      %s
      (SaveGame|SaveGameToSlot s "HollowKinSettings" 0)
      (CallFunction|ApplyLive)
      (CallFunction|RefreshLabels))
    (:CastFailed
      (bind s2 (Utilities|Casting|CastToBP_SettingsSave (SaveGame|CreateSaveGameObject "%s")))
      %s
      (SaveGame|SaveGameToSlot s2 "HollowKinSettings" 0)
      (CallFunction|ApplyLive)
      (CallFunction|RefreshLabels))))''' % (name, set_expr_existing, SAVE_C, set_expr_new))
save_edit('CycleSens', '(Class|BPSettingsSave|SetLookSens :self s :LookSens (select (>= (Class|BPSettingsSave|GetLookSens :self s) 150) 50 (+ (Class|BPSettingsSave|GetLookSens :self s) 25)))',
          '(Class|BPSettingsSave|SetLookSens :self s2 :LookSens 125)')
for name, var in [('ToggleInvert', 'InvertY'), ('ToggleMotionBlur', 'NoMotionBlur'), ('ToggleTextSize', 'LargeText')]:
    save_edit(name, '(Class|BPSettingsSave|Set%s :self s :b%s (not (Class|BPSettingsSave|Get%s :self s)))' % (var, var, var),
              '(Class|BPSettingsSave|Set%s :self s2 :b%s true)' % (var, var))
# ---------- pages + descriptions ----------
cats = len(PAGES)
fn('ShowPage', '''(fn ShowPage (Idx Title Body)
  (Switcher|SetActiveWidgetIndex %s Idx)
  %s
  (Widget|SetText(Text) %s (Utilities|Text|ToText(String) Title))
  (Widget|SetText(Text) %s (Utilities|Text|ToText(String) Body))
  (Widget|SetText(Text) %s (Utilities|Text|ToText(String) "")))''' % (G('Pages'),
    '\n  '.join('(Widget|SetRenderOpacity %s (select (== Idx %d) 1.0 0.0))\n  (Widget|SetRenderOpacity %s (select (== Idx %d) 1.0 0.55))' % (G('Cat%dDot' % i), i, G('Cat%dName' % i), i) for i in range(cats)),
    G('DescTitle'), G('DescBody'), G('DescDefault')), [('Idx', 'int'), ('Title', 'string'), ('Body', 'string')])
PAGE_BODY = {'GAMEPLAY': 'How information is shown while you play.', 'CONTROLS': 'Camera feel and the default key layout. Rebinding comes in a later build.',
             'GRAPHICS': 'Quality and performance. Lower Resolution Scale first if the game runs slowly or the Mac gets hot.',
             'AUDIO': 'Volume levels. Headphones recommended.', 'ACCESSIBILITY': 'Comfort options.'}
for i, (page, rows) in enumerate(PAGES):
    fn('Page%d' % i, '(fn Page%d ()\n  (CallFunction|ShowPage :Idx %d :Title "%s" :Body "%s"))' % (i, i, page, PAGE_BODY[page]))
    for (bn, label, default, desc) in rows:
        fn('Desc' + bn, '''(fn Desc%s ()
  (Widget|SetText(Text) %s (Utilities|Text|ToText(String) "%s"))
  (Widget|SetText(Text) %s (Utilities|Text|ToText(String) "%s"))
  (Widget|SetText(Text) %s (Utilities|Text|ToText(String) "Default value:  %s")))''' % (bn, G('DescTitle'), label.upper(), G('DescBody'), desc.replace('"', "'"), G('DescDefault'), default))
fn('OnKeyDown', '''(fn OnKeyDown (MyGeometry InKeyEvent)
  (bind k (Utilities|String|ToString(Text) (Input|Key|GetKeyDisplayName (Input|KeyEvent|GetKey InKeyEvent))))
  (if (or (Utilities|String|Equal,CaseInsensitive(String) k "Escape") (Utilities|String|Equal,CaseInsensitive(String) k "P"))
    (CallFunction|DoBack)
    (return (Widget|EventReply|Handled))
    (else (return (Widget|EventReply|Unhandled)))))''')
fn('OpenInit', '''(fn OpenInit ()
  (CallFunction|RefreshLabels)
  (CallFunction|Page0)
  (Variables|Interaction|SetIsFocusable :bIsFocusable true)
  (Widget|SetKeyboardFocus self))''')
print('Construct', call(BT, 'write_graph_dsl', {'graph': {'refPath': SET + ':EventGraph'}, 'code': '(event UserInterface|EventConstruct\n  (CallFunction|OpenInit))'}))

def bind_event(event, mapping):
    g = {'refPath': SET + ':EventGraph'}
    for b in mapping:
        call(UM, 'BindToEventProperty', {'widgetBlueprint': B, 'eventName': event, 'propertyName': b, 'propertyClass': {'refPath': '/Script/UMG.Button'}})
    evs = call(BT, 'find_nodes', {'graph': g, 'title': event.replace('On', '')})['returnValue']
    infos = call(BT, 'get_node_infos', {'nodes': evs})['returnValue']
    y = 0
    for n in infos:
        for b, f in mapping.items():
            if ('(%s)' % b) in n['type_id'] and event in n['type_id']:
                outs = [p for p in n['output_pins'] if p['type_id'] == 'Exec']
                if outs and outs[0]['connected_pins']:
                    continue
                cf = call(BT, 'create_node', {'graph': g, 'type_id': 'CallFunction|' + f, 'pos': {'x': 900, 'y': y}})['returnValue']; y += 160
                call(BT, 'connect_pins', {'output_pin': outs[0]['pin_id'], 'input_pin': {'direction': 'EGPD_Input', 'index_id': 0, 'node': cf}})
hover = {bn: 'Desc' + bn for page, rows in PAGES for (bn, l, d, x) in rows}
clicks = {'Cat%d' % i: 'Page%d' % i for i in range(cats)}
clicks.update({'BtnSens': 'CycleSens', 'BtnInvert': 'ToggleInvert', 'BtnMotionBlur': 'ToggleMotionBlur', 'BtnTextSize': 'ToggleTextSize'})
bind_event('OnHovered', hover)
bind_event('OnClicked', clicks)
print(call(BT, 'compile_blueprint', {'blueprint': B, 'warnings_as_errors': False}))

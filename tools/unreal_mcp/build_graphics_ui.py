"""Protocols screen: GRAPHICS section (quality preset, resolution scale, VSync, display mode, frame limit) using
GameUserSettings (saved to GameUserSettings.ini automatically), plus AUDIO / GRAPHICS / ACCESSIBILITY headings
and tighter rows so everything fits. Run 'widgets' once, then 'logic'."""
import sys
from menu_common import *
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
SET = '/Game/HollowKin/UI/Menus/WBP_Settings.WBP_Settings'
F_BODY = '/Game/HollowKin/UI/Fonts/BarlowSemiCondensed-SemiBold_Font.BarlowSemiCondensed-SemiBold_Font'
GFX = [('BtnQuality', 'GRAPHICS QUALITY:  HIGH'), ('BtnResScale', 'RESOLUTION SCALE:  100%'), ('BtnVsync', 'VSYNC:  ON'),
       ('BtnWindow', 'DISPLAY:  FULLSCREEN'), ('BtnFps', 'FRAME LIMIT:  60')]

def widgets():
    W = Wbp(SET)
    brush, txt, box, cslot, bslot, rule, button = mk(W)
    def cap(name, label, idx):
        W.count['PBox'] = idx
        t, s = W.add('TextBlock', name, 'PBox')
        setp(t, {'text': label, 'colorAndOpacity': {'specifiedColor': col(TEAL), 'colorUseRule': 'UseColor_Specified'},
                 'font': {'fontObject': F_BODY, 'typefaceFontName': 'Default', 'size': 16, 'letterSpacing': 300}})
        bslot(s, pad=(0, 10, 0, 2))
    cap('CapAudio', 'AUDIO', 3)
    cap('CapGfx', 'GRAPHICS', 7)
    W.count['PBox'] = 8
    for b, label in GFX:
        button(b, 'PBox', label)
        lab = W.widget(b + 'Label')
        f = json.loads(call(O, 'get_properties', {'instance': {'refPath': lab}, 'properties': ['Font']})['returnValue'])['Font']
        f.update({'fontObject': F_BODY, 'typefaceFontName': 'Default', 'letterSpacing': 200})
        setp(lab, {'font': f})
        for n in (b, b + 'Label'):
            call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}, 'bIsVariable': True})
    cap('CapAccess', 'ACCESSIBILITY', 13)
    # tighter rows for every button
    for x in call(U, 'GetWidgets', {'widgetBlueprint': W.ref})['returnValue']['widgets']:
        name = x['widget']['refPath'].split('.')[-1]
        if name.startswith('Btn') and name.endswith('Label') and isinstance(x.get('slot'), dict):
            bslot(x['slot']['refPath'], pad=(16, 6, 16, 6), v='VAlign_Center')
        if name.startswith('Btn') and name[3:].isalpha() and not name.endswith(('Label', 'Row', 'Tick', 'TickBar')) and isinstance(x.get('slot'), dict):
            bslot(x['slot']['refPath'], pad=(0, 1, 0, 1))
        if name == 'Panel':
            setp(x['slot']['refPath'], {'layoutData': {'offsets': {'left': 0, 'top': 0, 'right': 660, 'bottom': 960},
                 'anchors': {'minimum': {'x': 0.5, 'y': 0.5}, 'maximum': {'x': 0.5, 'y': 0.5}}, 'alignment': {'x': 0.5, 'y': 0.5}}})
    print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))

GUS = '(Settings|GetGameUserSettings)'
def lab(btn, text_expr):
    return '(Widget|SetText(Text) (Variables|WBP_Settings|Get%sLabel) (Utilities|Text|ToText(String) %s))' % (btn, text_expr)

def logic():
    fns = {
     'RefreshGraphics': '''(fn RefreshGraphics ()
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
        'g': GUS,
        'q0': lab('BtnQuality', '"GRAPHICS QUALITY:  LOW"'), 'q1': lab('BtnQuality', '"GRAPHICS QUALITY:  MEDIUM"'),
        'q2': lab('BtnQuality', '"GRAPHICS QUALITY:  HIGH"'), 'q3': lab('BtnQuality', '"GRAPHICS QUALITY:  EPIC"'),
        'res': lab('BtnResScale', '(Utilities|String|BuildString(Integer) :Prefix "RESOLUTION SCALE:  " :InInt (Math|Float|Round (* (Settings|GetResolutionScaleNormalized :self g) 100.0)) :Suffix "%")'),
        'von': lab('BtnVsync', '"VSYNC:  ON"'), 'voff': lab('BtnVsync', '"VSYNC:  OFF"'),
        'win': lab('BtnWindow', '"DISPLAY:  WINDOWED"'), 'full': lab('BtnWindow', '"DISPLAY:  FULLSCREEN"'),
        'funl': lab('BtnFps', '"FRAME LIMIT:  UNLIMITED"'),
        'fnum': lab('BtnFps', '(Utilities|String|BuildString(Integer) :Prefix "FRAME LIMIT:  " :InInt (Math|Float|Round (Settings|GetFrameRateLimit :self g)) :Suffix "")')},
     'CycleQuality': '''(fn CycleQuality ()
  (bind g %s)
  (bind lvl (Settings|GetOverallScalabilityLevel :self g))
  (Settings|SetOverallScalabilityLevel :self g :Value (select (>= lvl 3) 0 (+ lvl 1)))
  (Settings|ApplySettings :self g :bCheckForCommandLineOverrides false)
  (CallFunction|RefreshGraphics))''' % GUS,
     'CycleVsync': '''(fn CycleVsync ()
  (bind g %s)
  (Settings|SetVSyncEnabled :self g :bEnable (not (Settings|IsVSyncEnabled :self g)))
  (Settings|ApplySettings :self g :bCheckForCommandLineOverrides false)
  (CallFunction|RefreshGraphics))''' % GUS,
     'CycleFps': '''(fn CycleFps ()
  (bind g %s)
  (bind f (Settings|GetFrameRateLimit :self g))
  (Settings|SetFrameRateLimit :self g :NewLimit (select (< f 1.0) 30.0 (select (< f 45.0) 60.0 (select (< f 90.0) 120.0 0.0))))
  (Settings|ApplySettings :self g :bCheckForCommandLineOverrides false)
  (CallFunction|RefreshGraphics))''' % GUS,
     'CycleWindow': '''(fn CycleWindow ()
  (bind g %s)
  (bind s (Utilities|Casting|CastToBP_SettingsSave (SaveGame|LoadGameFromSlot "HollowKinSettings" 0))
    (:then
      (Class|BPSettingsSave|SetWindowed :self s :bWindowed (not (Class|BPSettingsSave|GetWindowed :self s)))
      (SaveGame|SaveGameToSlot s "HollowKinSettings" 0)
      (if (Class|BPSettingsSave|GetWindowed :self s)
        (Settings|SetFullscreenMode :self g :InFullscreenMode "Windowed")
        (else (Settings|SetFullscreenMode :self g :InFullscreenMode "WindowedFullscreen")))
      (Settings|ApplySettings :self g :bCheckForCommandLineOverrides false)
      (CallFunction|RefreshGraphics))
    (:CastFailed
      (bind n (Utilities|Casting|CastToBP_SettingsSave (SaveGame|CreateSaveGameObject "/Game/HollowKin/Blueprints/Systems/BP_SettingsSave.BP_SettingsSave_C")))
      (Class|BPSettingsSave|SetWindowed :self n :bWindowed true)
      (SaveGame|SaveGameToSlot n "HollowKinSettings" 0)
      (Settings|SetFullscreenMode :self g :InFullscreenMode "Windowed")
      (Settings|ApplySettings :self g :bCheckForCommandLineOverrides false)
      (CallFunction|RefreshGraphics))))''' % GUS,
     'CycleResScale': '''(fn CycleResScale ()
  (bind g %s)
  (bind r (Settings|GetResolutionScaleNormalized :self g))
  (Settings|SetResolutionScaleNormalized :self g :NewScaleNormalized (select (> r 0.9) 0.75 (select (> r 0.6) 0.5 1.0)))
  (Settings|ApplySettings :self g :bCheckForCommandLineOverrides false)
  (CallFunction|RefreshGraphics))''' % GUS,
    }
    for name, dsl in fns.items():
        call(BT, 'add_function_graph', {'blueprint': {'refPath': SET}, 'graph_name': name})
        print(name, call(BT, 'write_graph_dsl', {'graph': {'refPath': SET + ':' + name}, 'code': dsl}))

if __name__ == '__main__':
    if 'widgets' in sys.argv: widgets()
    if 'logic' in sys.argv: logic()

def bind():
    import menu_logic as ml
    m = {'BtnQuality': 'CycleQuality', 'BtnResScale': 'CycleResScale', 'BtnVsync': 'CycleVsync', 'BtnWindow': 'CycleWindow', 'BtnFps': 'CycleFps'}
    for b, f in m.items():
        ml.wire(SET, b, f, 0)
    ml.connect_clicks(SET, m)

if __name__ == '__main__' and 'bind' in sys.argv:
    bind()

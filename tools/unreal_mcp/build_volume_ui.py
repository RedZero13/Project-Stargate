"""Protocols screen: MASTER / MUSIC / EFFECTS volume rows (click cycles 100-75-50-25-0), saved in HollowKinSettings,
applied through BP_SettingsSave.ApplyVolumes. Also applies the saved volumes when the main menu or in-game HUD opens."""
from menu_common import *
import menu_logic as ml
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
SET = '/Game/HollowKin/UI/Menus/WBP_Settings.WBP_Settings'
SAVE_C = '/Game/HollowKin/Blueprints/Systems/BP_SettingsSave.BP_SettingsSave_C'
ROWS = [('BtnMaster', 'Master', 'MASTER VOLUME'), ('BtnMusic', 'Music', 'MUSIC VOLUME'), ('BtnSfx', 'Sfx', 'EFFECTS VOLUME')]

def build_buttons():
    W = Wbp(SET)
    brush, txt, box, cslot, bslot, rule, button = mk(W)
    W.count['PBox'] = 3                      # after Cap, Head, SzR1 -> before the toggles
    for b, _, label in ROWS:
        button(b, 'PBox', label + ':  100%')
        lab = W.widget(b + 'Label')
        f = json.loads(call(O, 'get_properties', {'instance': {'refPath': lab}, 'properties': ['Font']})['returnValue'])['Font']
        f.update({'fontObject': '/Game/HollowKin/UI/Fonts/BarlowSemiCondensed-SemiBold_Font.BarlowSemiCondensed-SemiBold_Font', 'typefaceFontName': 'Default', 'letterSpacing': 200})
        setp(lab, {'font': f})
        for n in (b, b + 'Label'):
            call(U, 'ToggleWidgetAsVariable', {'widgetBlueprint': W.ref, 'widget': {'refPath': W.widget(n)}, 'bIsVariable': True})
    print(call(U, 'CompileWidgetBlueprint', {'widgetBlueprint': W.ref}))

def label_set(btn, key, src):
    return '(Widget|SetText(Text) (Variables|WBP_Settings|Get%sLabel) (Utilities|Text|ToText(String) (Utilities|String|BuildString(Integer) :Prefix "%s:  " :InInt %s :Suffix "%%")))' % (btn, key, src)

def logic():
    ok = '\n        '.join(label_set(b, l, '(Class|BPSettingsSave|Get%sVol :self s)' % k) for b, k, l in ROWS)
    bad = '\n      '.join(label_set(b, l, '100') for b, k, l in ROWS)
    refresh = '''(fn RefreshLabels ()
  (CallFunction|RefreshGraphics)
  (bind s (Utilities|Casting|CastToBP_SettingsSave (SaveGame|LoadGameFromSlot "HollowKinSettings" 0))
    (:then
      (if (Class|BPSettingsSave|GetOverlayHUD :self s)
        (Widget|SetText(Text) (Variables|WBP_Settings|GetBtnOverlayLabel) "OVERLAY HUD:  ON")
        (else (Widget|SetText(Text) (Variables|WBP_Settings|GetBtnOverlayLabel) "OVERLAY HUD:  OFF")))
      (if (Class|BPSettingsSave|GetReduceFlash :self s)
        (Widget|SetText(Text) (Variables|WBP_Settings|GetBtnFlashLabel) "REDUCE FLASHING:  ON")
        (else (Widget|SetText(Text) (Variables|WBP_Settings|GetBtnFlashLabel) "REDUCE FLASHING:  OFF")))
        %s)
    (:CastFailed
      (Widget|SetText(Text) (Variables|WBP_Settings|GetBtnOverlayLabel) "OVERLAY HUD:  OFF")
      (Widget|SetText(Text) (Variables|WBP_Settings|GetBtnFlashLabel) "REDUCE FLASHING:  OFF")
      %s)))''' % (ok, bad)
    print('RefreshLabels', call(BT, 'write_graph_dsl', {'graph': {'refPath': SET + ':RefreshLabels'}, 'code': refresh}))
    for b, k, l in ROWS:
        fn = 'Cycle%sVol' % k
        dsl = '''(fn %(fn)s ()
  (bind s (Utilities|Casting|CastToBP_SettingsSave (SaveGame|LoadGameFromSlot "HollowKinSettings" 0))
    (:then
      (Class|BPSettingsSave|Set%(k)sVol :self s :%(k)sVol (select (<= (Class|BPSettingsSave|Get%(k)sVol :self s) 0) 100 (- (Class|BPSettingsSave|Get%(k)sVol :self s) 25)))
      (SaveGame|SaveGameToSlot s "HollowKinSettings" 0)
      (Class|BPSettingsSave|ApplyVolumes :self s :Ctx self)
      (CallFunction|RefreshLabels))
    (:CastFailed
      (bind n (Utilities|Casting|CastToBP_SettingsSave (SaveGame|CreateSaveGameObject "%(c)s")))
      (Class|BPSettingsSave|Set%(k)sVol :self n :%(k)sVol 75)
      (SaveGame|SaveGameToSlot n "HollowKinSettings" 0)
      (Class|BPSettingsSave|ApplyVolumes :self n :Ctx self)
      (CallFunction|RefreshLabels))))''' % {'fn': fn, 'k': k, 'c': SAVE_C}
        print(fn, call(BT, 'write_graph_dsl', {'graph': {'refPath': SET + ':' + fn}, 'code': dsl}))
    if 'bind' in __import__('sys').argv:
        for b, k, l in ROWS: ml.wire(SET, b, 'Cycle%sVol' % k, 0)
        ml.connect_clicks(SET, {b: 'Cycle%sVol' % k for b, k, l in ROWS})

if __name__ == '__main__':
    import sys
    if 'buttons' in sys.argv: build_buttons()
    if 'logic' in sys.argv: logic()

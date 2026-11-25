"""WBP_Backpack logic: RefreshCase (counts from BP_Max, dims empty tiles, ingredient have/need, CRAFT enabled only
when affordable), ShowTab, use/craft buttons, hover descriptions, I/Esc/P closes (unpauses)."""
from ui_lib import call
from backpack_spec import ITEMS, RECIPES
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
UM = 'UMGToolSet.UMGToolSet'
P = '/Game/HollowKin/UI/Menus/WBP_Backpack.WBP_Backpack'
B = {'refPath': P}
def fn(name, dsl, params=()):
    call(BT, 'add_function_graph', {'blueprint': B, 'graph_name': name})
    for pn, pt in params:
        call(BT, 'add_function_param', {'graph': {'refPath': P + ':' + name}, 'param_name': pn, 'param_type': pt, 'input_param': True})
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': P + ':' + name}, 'code': dsl})
    if not isinstance(r, dict) or r.get('returnValue') is not None: print(name, str(r)[:300])
G = lambda n: '(Variables|WBP_Backpack|Get%s)' % n
MV = lambda v: '(Class|BPMax|Get%s :self m)' % v
var_of = {k: mv for (k, l, i, c, mv, d, u) in ITEMS}
lines = []
for (k, l, i, c, mv, d, u) in ITEMS:
    lines.append('(Widget|SetText(Text) %s (Utilities|Text|ToText(String) (Utilities|String|BuildString(Integer) :Prefix "x " :InInt %s :Suffix "")))' % (G('It%sCount' % k), MV(mv)))
    lines.append('(Widget|SetRenderOpacity %s (select (> %s 0) 1.0 0.35))' % (G('It' + k), MV(mv)))
for (rk, rl, ri, rc, ings, cfn, rd) in RECIPES:
    conds = []
    for (ik, need) in ings:
        have = MV(var_of[ik])
        lines.append('(Widget|SetText(Text) %s (Utilities|Text|ToText(String) (Utilities|String|BuildString(Integer) :Prefix "" :InInt %s :Suffix " / %d")))' % (G('%s%sCount' % (rk, ik)), have, need))
        lines.append('(Widget|SetRenderOpacity %s (select (>= %s %d) 1.0 0.45))' % (G(rk + ik), have, need))
        conds.append('(>= %s %d)' % (have, need))
    cond = conds[0] if len(conds) == 1 else '(and %s %s)' % (conds[0], conds[1])
    lines.append('(Widget|SetIsEnabled %s %s)' % (G(rk + 'Craft'), cond))
    lines.append('(Widget|SetText(Text) %s (Utilities|Text|ToText(String) "x 1"))' % G(rk + 'OutCount'))
fn('RefreshCase', '''(fn RefreshCase ()
  (bind m (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))
    (:then
      %s)
    (:CastFailed)))''' % '\n      '.join(lines))
fn('ShowTab', '''(fn ShowTab (Idx)
  (Switcher|SetActiveWidgetIndex %s Idx)
  (Widget|SetRenderOpacity %s (select (== Idx 0) 1.0 0.0))
  (Widget|SetRenderOpacity %s (select (== Idx 1) 1.0 0.0))
  (Widget|SetRenderOpacity %s (select (== Idx 0) 1.0 0.5))
  (Widget|SetRenderOpacity %s (select (== Idx 1) 1.0 0.5))
  (CallFunction|RefreshCase))''' % (G('CasePages'), G('Tab0Line'), G('Tab1Line'), G('Tab0Name'), G('Tab1Name')), [('Idx', 'int')])
fn('TabItems', '(fn TabItems ()\n  (CallFunction|ShowTab :Idx 0))')
fn('TabCraft', '(fn TabCraft ()\n  (CallFunction|ShowTab :Idx 1))')
for (k, l, i, c, mv, d, u) in ITEMS:
    if u:
        fn('Do' + u, '''(fn Do%s ()
  (bind m (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))
    (:then (Class|BPMax|%s :self m) (CallFunction|RefreshCase))
    (:CastFailed)))''' % (u, u))
for (rk, rl, ri, rc, ings, cfn, rd) in RECIPES:
    fn('Do' + cfn, '''(fn Do%s ()
  (bind m (Utilities|Casting|CastToBP_Max (Game|GetPlayerPawn 0))
    (:then (Class|BPMax|%s :self m) (CallFunction|RefreshCase))
    (:CastFailed)))''' % (cfn, cfn))
def desc(fname, name, text):
    fn(fname, '''(fn %s ()
  (Widget|SetText(Text) %s (Utilities|Text|ToText(String) "%s"))
  (Widget|SetText(Text) %s (Utilities|Text|ToText(String) "%s")))''' % (fname, G('DescName'), name, G('DescText'), text.replace('"', "'")))
hover = {}
for (k, l, i, c, mv, d, u) in ITEMS:
    desc('Desc' + k, l, d); hover['It' + k] = 'Desc' + k
for (rk, rl, ri, rc, ings, cfn, rd) in RECIPES:
    need = '  +  '.join('%d %s' % (n, [x[1] for x in ITEMS if x[0] == ik][0]) for ik, n in ings)
    desc('Desc' + rk, rl, rd + '   Needs ' + need + '.'); hover[rk + 'Craft'] = 'Desc' + rk; hover[rk + 'Out'] = 'Desc' + rk
fn('CloseCase', '''(fn CloseCase ()
  (bind pc (Game|GetPlayerController 0))
  (Game|SetGamePaused false)
  (Input|SetInputModeGameOnly pc false)
  (Class|PlayerController|SetShowMouseCursor :self pc :bShowMouseCursor false)
  (Widget|RemoveFromParent self))''')
fn('OnKeyDown', '''(fn OnKeyDown (MyGeometry InKeyEvent)
  (bind k (Utilities|String|ToString(Text) (Input|Key|GetKeyDisplayName (Input|KeyEvent|GetKey InKeyEvent))))
  (if (or (or (Utilities|String|Equal,CaseInsensitive(String) k "Escape") (Utilities|String|Equal,CaseInsensitive(String) k "P")) (Utilities|String|Equal,CaseInsensitive(String) k "I"))
    (CallFunction|CloseCase)
    (return (Widget|EventReply|Handled))
    (else (return (Widget|EventReply|Unhandled)))))''')
print(call(BT, 'write_graph_dsl', {'graph': {'refPath': P + ':EventGraph'}, 'code': '(event UserInterface|EventTick (MyGeometry InDeltaTime)\n  (Variables|Default|SetT 0.0))'}))
print(call(BT, 'write_graph_dsl', {'graph': {'refPath': P + ':EventGraph'}, 'code': '''(event UserInterface|EventConstruct
  (Variables|Interaction|SetIsFocusable :bIsFocusable true)
  (Widget|SetKeyboardFocus self)
  (CallFunction|RefreshCase))'''}))
def bind_event(event, mapping):
    g = {'refPath': P + ':EventGraph'}
    for b in mapping:
        call(UM, 'BindToEventProperty', {'widgetBlueprint': B, 'eventName': event, 'propertyName': b, 'propertyClass': {'refPath': '/Script/UMG.Button'}})
    evs = call(BT, 'find_nodes', {'graph': g, 'title': event.replace('On', '')})['returnValue']
    infos = call(BT, 'get_node_infos', {'nodes': evs})['returnValue']
    y = 0
    for n in infos:
        for b, f in mapping.items():
            if ('(%s)' % b) in n['type_id'] and event in n['type_id']:
                outs = [p for p in n['output_pins'] if p['type_id'] == 'Exec']
                if outs and outs[0]['connected_pins']: continue
                cf = call(BT, 'create_node', {'graph': g, 'type_id': 'CallFunction|' + f, 'pos': {'x': 900, 'y': y}})['returnValue']; y += 160
                call(BT, 'connect_pins', {'output_pin': outs[0]['pin_id'], 'input_pin': {'direction': 'EGPD_Input', 'index_id': 0, 'node': cf}})
clicks = {'Tab0': 'TabItems', 'Tab1': 'TabCraft'}
clicks.update({'It' + k: 'Do' + u for (k, l, i, c, mv, d, u) in ITEMS if u})
clicks.update({rk + 'Craft': 'Do' + cfn for (rk, rl, ri, rc, ings, cfn, rd) in RECIPES})
bind_event('OnHovered', hover)
bind_event('OnClicked', clicks)
r = call(BT, 'compile_blueprint', {'blueprint': B, 'warnings_as_errors': False}); print('compile', r)
print(call('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': ['/Game/HollowKin/UI/Menus/WBP_Backpack']}))

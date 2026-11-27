"""Six endings (2026-11-26). Hidden tally like Silent Hill 2: the game judges how you played, checked in this order:
1 HOLLOW     Taint >= 80 (hurting Hollow Children +40 each, L-7 serum +15 each)
2 SIX DOORS  opened the B15 cells (needs 5 patient files) and Bond >= 70 and Taint < 40
3 LULLABY    no Hollow killed this run, Bond >= 40, Taint < 40
4 HOMECOMING Bond >= 70 and Taint < 40
5 KIN        Bond >= 40
6 LANTERN    otherwise
WBP_DeathScreen gets SetEnding(Head, Sub) for the new three; BP_Max.ShowEnding rewritten (logs "ENDING <NAME>")."""
from ui_lib import call
BT = 'editor_toolset.toolsets.blueprint.BlueprintTools'; A = 'editor_toolset.toolsets.asset.AssetTools'
DS = '/Game/HollowKin/UI/Diegetic/WBP_DeathScreen.WBP_DeathScreen'
MAX = '/Game/HollowKin/Blueprints/Player/BP_Max.BP_Max'
def w(g, dsl):
    r = call(BT, 'write_graph_dsl', {'graph': {'refPath': g}, 'code': dsl}); print(g.split(':')[-1], 'ok' if isinstance(r, dict) and r.get('returnValue') is None else r)
call(BT, 'add_function_graph', {'blueprint': {'refPath': DS}, 'graph_name': 'SetEnding'})
for p in ('Head', 'Sub'):
    call(BT, 'add_function_param', {'graph': {'refPath': DS + ':SetEnding'}, 'param_name': p + 'Text', 'param_type': 'string', 'input_param': True})
w(DS + ':SetEnding', '''(fn SetEnding (HeadText SubText)
  (Widget|SetText(Text) (Variables|WBP_DeathScreen|GetHead) (Utilities|Text|ToText(String) HeadText))
  (Widget|SetText(Text) (Variables|WBP_DeathScreen|GetSub) (Utilities|Text|ToText(String) SubText)))''')
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': DS}, 'warnings_as_errors': False}))
B, T = '(Variables|Default|GetBond)', '(Variables|Default|GetTaint)'
FL = lambda f: '(CallFunction|HasFlag :F "%s")' % f
TRUE = '(and (and (CallFunction|HasFlag :F "NG+") (Variables|Default|GetFreedChildren)) (and (and %s %s) (and %s (< %s 20.0))))' % (FL('evidence'), FL('left_meds'), FL('nurse_freed'), '(Variables|Default|GetTaint)')
NAME = ('(select (>= %(T)s 80.0) "HOLLOW" (select TRUE "LANTERNLIT" (select (and (Variables|Default|GetFreedChildren) (and (>= %(B)s 70.0) (< %(T)s 40.0))) "SIXDOORS" '
        '(select (and (== (Variables|Default|GetRunKills) 0) (and (>= %(B)s 40.0) (< %(T)s 40.0))) "LULLABY" '
        '(select (and (>= %(B)s 70.0) (< %(T)s 40.0)) "HOMECOMING" (select (>= %(B)s 40.0) "KIN" "LANTERN"))))))') % {'B': B, 'T': T}
NAME = NAME.replace('TRUE', TRUE)
EQ = lambda s: '(Utilities|String|EqualExactly(String) name "%s")' % s
w(MAX + ':ShowEnding', '''(fn ShowEnding ()
  (bind pc (Game|GetPlayerController 0))
  (if (not (Variables|Default|GetDead))
    (Variables|Default|SetDead true)
    (Input|DisableInput self pc)
    (Utilities|Time|SetTimerbyFunctionName self "EndRun" 14.0)
    (bind ds (Utilities|Casting|CastToWBP_DeathScreen (UserInterface|CreateWidget "/Game/HollowKin/UI/Diegetic/WBP_DeathScreen.WBP_DeathScreen_C" pc)))
    (UserInterface|Viewport|AddToViewport ds 30)
    (bind name %s)
    (CallFunction|HKLog :Msg (Utilities|String|Append "ENDING " name))
    (bind epi (Utilities|String|Append (Utilities|String|Append (select %s "   //   WITHIN A WEEK, HALVORSEN'S FILES ARE ON EVERY SCREEN IN THE COUNTRY." (select %s "   //   HALVORSEN BIOLOGICS REOPENS NEXT SPRING UNDER A NEW NAME." ""))
      (select (CallFunction|HasFlag :F "forgave_okafor") "   //   NURSE OKAFOR CARRIES THE LAST CHILD UP THE STAIRS." ""))
      (select (CallFunction|HasFlag :F "hale_stand") "   //   THEY FIND SGT. HALE AT HIS POST ON B12. HE NEVER TURNED." "")))
    (if %s
      (Class|WBPDeathScreen|SetEnding :self ds :HeadText "LANTERN LIT" :SubText (Utilities|String|Append "MAX, EMILIA AND FIVE CHILDREN WALK OUT INTO THE DAWN. NOBODY IS LEFT BEHIND THIS TIME." epi))
    (elif %s
      (Class|WBPDeathScreen|SetEnding :self ds :HeadText "HOLLOW" :SubText "THE SERUM FINISHES WHAT IT STARTED  //  EMILIA HOLDS HER BROTHER'S HAND AS HIS EYES GO DARK")
      (elif %s
        (Class|WBPDeathScreen|SetEnding :self ds :HeadText "SIX DOORS" :SubText (Utilities|String|Append "SIX CHILDREN WALK OUT OF ST. BRIGID'S  //  THE CITY FINALLY HEARS THEIR NAMES" epi))
        (elif %s
          (Class|WBPDeathScreen|SetEnding :self ds :HeadText "LULLABY" :SubText (Utilities|String|Append "NOT ONE SHOT IN ANGER  //  EMILIA SINGS, AND EVERY HOLLOW IN THE BUILDING LIES DOWN TO SLEEP" epi))
          (elif %s
            (Class|WBPDeathScreen|SetHomecoming ds)
            (elif %s
              (Class|WBPDeathScreen|SetKin ds)
              (else (Class|WBPDeathScreen|SetLantern ds))))))))
    (bind gi (Utilities|Casting|CastToBP_HKGameInstance (Game|GetGameInstance))
      (:then (Class|BPHKGameInstance|UnlockNG :self gi :J (Variables|Default|GetJournal)))
      (:CastFailed))))''' % (NAME, '(CallFunction|HasFlag :F "evidence")', '(CallFunction|HasFlag :F "wiped")', EQ('LANTERNLIT'), EQ('HOLLOW'), EQ('SIXDOORS'), EQ('LULLABY'), EQ('HOMECOMING'), EQ('KIN')))
print(call(BT, 'compile_blueprint', {'blueprint': {'refPath': MAX}, 'warnings_as_errors': False}))
print(call(A, 'save_assets', {'asset_paths': []}))

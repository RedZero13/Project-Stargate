#!/bin/bash
# Makes the shareable playtest report from the PLAYTEST build's log.
# usage: bash tools/playtest_report.sh      -> writes ~/Desktop/HollowKin_Playtest_<date-time>.txt (send this file to Claude)
# The report has every HKLOG line (state every 2 s, messages, objectives, damage, deaths, lifts, puzzles, cutscenes,
# pause, enemies) plus all warnings/errors from the engine log.
OUT=~/Desktop/HollowKin_Playtest_$(date +%Y%m%d-%H%M).txt
LOGS=$(ls -t ~/Library/Containers/com.YourCompany.HollowKin/Data/Library/Logs/HollowKin/HollowKin*.log ~/Library/Logs/HollowKin/HollowKin*.log 2>/dev/null)
[ -z "$LOGS" ] && { echo "No HollowKin log found. Play the PLAYTEST build first."; exit 1; }
{
  echo "HOLLOW KIN playtest report  //  $(date)  //  $(sw_vers -productName) $(sw_vers -productVersion)  //  $(sysctl -n machdep.cpu.brand_string)"
  for L in $LOGS; do
    echo; echo "===== $(basename "$L")  ($(stat -f %Sm "$L")) ====="
    grep -o "HKLOG|.*" "$L"
    echo "----- warnings / errors -----"
    grep -E "Error|Warning: Script|Accessed None|Blueprint Runtime" "$L" | grep -v "HKLOG" | tail -200
  done
} > "$OUT"
echo "Report written: $OUT ($(wc -l < "$OUT") lines)"

#!/bin/bash
# Builds both Mac versions into ~/Documents/Unreal Projects/Builds:
#   HollowKin.app + HollowKin-Mac.zip                    (Shipping, regular game)
#   HollowKin-Playtest.app + HollowKin-Playtest-Mac.zip  (Development, HKLOG playtest logging)
# Usage: make_builds.sh [regular|playtest]  (no argument = both)
# Copies the ICU data each build needs, then deletes the staging folders to save space.
set -e
REPO="$(cd "$(dirname "$0")/.." && pwd)"
UAT="/Users/Shared/Epic Games/UE_5.8/Engine/Build/BatchFiles/RunUAT.sh"
ICU="/Users/Shared/Epic Games/UE_5.8/Engine/Content/Internationalization/English/."
OUT="$REPO/../Builds"
build() {  # config stagingdir appname zipname
  "$UAT" BuildCookRun -project="$REPO/HollowKin/HollowKin.uproject" -noP4 -platform=Mac -clientconfig=$1 \
    -build -cook -stage -pak -compressed -utf8output -stagingdirectory="$2"
  APP="$(ls -d "$2"/Mac/*.app | head -1)"   # Shipping stages HollowKin-Mac-Shipping.app
  mkdir -p "$APP/Contents/UE/Engine/Content/Internationalization"
  cp -R "$ICU" "$APP/Contents/UE/Engine/Content/Internationalization/"
  rm -rf "$OUT/$3" "$OUT/$4"
  ditto "$APP" "$OUT/$3"
  (cd "$OUT" && ditto -c -k --keepParent "$3" "$4")
  rm -rf "$2"
}
if [ "$1" != "playtest" ]; then build Shipping "$REPO/HollowKin/Saved/StagedBuilds" HollowKin.app HollowKin-Mac.zip; fi
if [ "$1" != "regular" ]; then build Development "$REPO/HollowKin/Saved/StagedPlaytest" HollowKin-Playtest.app HollowKin-Playtest-Mac.zip; fi
ls -la "$OUT"
echo BUILDS DONE

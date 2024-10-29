#!/bin/bash

OS_INFO=$(uname -a)
SCRIPT_DIR="$(dirname "$0")"

source $SCRIPT_DIR/config/cfg_filter_map.sh # It imports the settingsMap variable

escapeSlashes () {
 inputString="$1"
 escapedForward="$(echo ${inputString//\\/\\\\\\\\})"
 
 echo "$escapedForward"
}

if [[ "$OS_INFO" == *Darwin* ]]; then
 SED_CMD="gsed"
else
 SED_CMD="sed"
fi

for key in ${!settingsMap[@]}; do
 keyEscaped="$(escapeSlashes "${key}")"
 valueEscaped="$(escapeSlashes "${settingsMap[${key}]}")"

 if [[ "$1" == "clean" ]]; then
  SED_CMD+=" -e \"s|${keyEscaped}|${valueEscaped}|g\""
 elif [[ "$1" == "smudge" ]]; then
  SED_CMD+=" -e \"s|${valueEscaped}|${keyEscaped}|g\""
 else
  echo "'smudge' or 'clean' shall be given as the first argument"
  exit 1
 fi
done

eval $SED_CMD
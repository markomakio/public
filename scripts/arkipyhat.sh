#!/bin/bash

if [[ $# == 1 ]] ; then
  VUOSI=$1
else
  echo "Käyttö: $0 <vuosi>"
  exit 1
fi

PYHA_PVMT="01-01 01-06 05-01 12-06 12-24 12-25 12-26"
ARKI_PYHAT=4

for PVM in $PYHA_PVMT ; do
  VPAIVA=$(date -d "$VUOSI-$PVM" +%u)
  if [[ $VPAIVA -lt 6 ]] ; then
    (( ARKI_PYHAT += 1 ))
  fi
done

echo $VUOSI $ARKI_PYHAT

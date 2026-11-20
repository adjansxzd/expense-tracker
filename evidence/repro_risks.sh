#!/usr/bin/env bash
# Reproduces candidate risk findings against the current checkout.
# Usage: bash evidence/repro_risks.sh   (runs in a temp dir, touches no repo data)
cd "$(dirname "$0")/.." || exit 1
export PYTHONPATH="$PWD/src"
T=$(mktemp -d); D="$T/data.json"
et(){ echo "\$ expense-tracker $*"; python3 -m expense_tracker --file "$D" "$@" 2>&1 | tail -n 3; echo "[exit code: ${PIPESTATUS[0]}]"; }

echo "== F1 float money arithmetic =="
et add 2026-11-01 food 0.10
et add 2026-11-02 food 0.20
et report

echo; echo "== F2 input validation =="
rm -f "$D"
et add 2026-11-03 food -50
et add 2026-13-45 food 10
et add 2026-11-04 food abc
et add 2026-11-05 "" 5
et list
et report --month 2026-11

echo; echo "== F3 CSV formula injection =="
rm -f "$D"
et add 2026-11-06 misc 1 -d '=HYPERLINK("http://example.invalid","click")'
et export "$T/out.csv"
echo "\$ cat out.csv"; cat "$T/out.csv"

echo; echo "== F4 corrupt data file =="
echo '[{"id": 1,' > "$D"
et list

echo; echo "== F6 unknown output format =="
rm -f "$D"; et add 2026-11-07 food 1 >/dev/null
et report --format xml
rm -rf "$T"

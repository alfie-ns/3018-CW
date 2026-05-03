#!/usr/bin/env bash
# open gaze22.py + COMP_3018_Report.md + assessment brief in Finder, ready to drag

set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT="$DIR/COMP_3018_Report.md"
BRIEF="$DIR/COMP3018-Assessment_Moderated.pdf"
GAZE="$DIR/task-4/gaze22.py"

for f in "$REPORT" "$BRIEF" "$GAZE"; do
  [[ -f "$f" ]] || { printf 'missing: %s\n' "$f" >&2; exit 1; }
done

osascript >/dev/null <<OSA
tell application "Finder"
    activate
    -- task-4 window: gaze22.py selected
    reveal (POSIX file "$GAZE") as alias
    -- Report window: report + brief selected together
    set fReport to (POSIX file "$REPORT") as alias
    set fBrief  to (POSIX file "$BRIEF")  as alias
    open container of fReport
    select {fReport, fBrief}
end tell
OSA

printf 'opened in Finder, ready to drag:\n'
printf '  - COMP_3018_Report.md\n'
printf '  - COMP3018-Assessment_Moderated.pdf\n'
printf '  - task-4/gaze22.py\n'

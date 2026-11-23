#!/bin/bash
# Daily Scholar stats refresh, run by launchd (~/Library/LaunchAgents/com.user.portfolio-scholar.plist).
# Uses its own clone so it never touches the working copy in ~/Documents/GitHub/portfolio.
set -euo pipefail
export PATH=/opt/homebrew/bin:/usr/bin:/bin
DIR="$HOME/.local/share/portfolio-scholar"
[ -d "$DIR/.git" ] || git clone -q https://github.com/Nafiz43/portfolio "$DIR"
cd "$DIR"
git pull -q --rebase
python3 -I tools/sync_scholar.py
git add data/scholar.json
git diff --cached --quiet && { echo "$(date) no change"; exit 0; }
git commit -qm "chore: sync Google Scholar stats"
git push -q
echo "$(date) pushed: $(tr -d '\n ' < data/scholar.json)"

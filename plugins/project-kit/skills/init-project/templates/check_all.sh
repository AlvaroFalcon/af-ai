#!/usr/bin/env bash
# Run every check CI runs, with one summary at the end. Usage: scripts/check_all.sh
# Installed by project-kit; the project owns it. Add one `check` line per CI step.
set -u
cd "$(dirname "$0")/.."

names=()
results=()
failed=0

check() {
  # check "<name>" <command...>
  local name="$1"
  shift
  local out
  if out=$("$@" 2>&1); then
    results+=("ok")
  else
    results+=("FAILED")
    failed=1
    echo "== $name: FAILED =="
    echo "$out" | tail -40
  fi
  names+=("$name")
}

skip_unless() {
  # skip_unless <tool> "<name>" <command...>: SKIPPED (not failed) when the tool is missing.
  local tool="$1"
  shift
  if command -v "$tool" >/dev/null 2>&1; then
    check "$@"
  else
    names+=("$1")
    results+=("SKIPPED ($tool not installed)")
  fi
}

check "docs + knowledge links" python3 scripts/check_docs.py
# {{PROJECT_CHECKS}} e.g.:
# check "tests" npm test --silent
# skip_unless shellcheck "shellcheck" shellcheck scripts/*.sh

echo "== Summary =="
for i in "${!names[@]}"; do
  printf '  %-26s %s\n' "${names[$i]}" "${results[$i]}"
done
exit $failed

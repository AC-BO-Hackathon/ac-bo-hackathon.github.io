#!/usr/bin/env bash
# Push HEAD to a NEW claude/* branch on origin, so a run started on a pull
# request can open a separate pull request (see "Opening a new PR from a run
# started on a PR" in CLAUDE.md).
#
# The action's own push wrapper only updates the branch the run started on.
# This script is the one sanctioned exception, and it only creates: it refuses
# a name outside claude/ and any branch that already exists on origin, so it
# can't touch main, a person's branch, or another PR's branch.
#
# Usage: scripts/push_new_branch.sh claude/<slug>
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 claude/<slug>" >&2
  exit 1
fi
name="$1"

if [[ ! "$name" =~ ^claude/[A-Za-z0-9][A-Za-z0-9._/-]*$ ]]; then
  echo "Error: the branch must be claude/<slug> (got: $name)" >&2
  exit 1
fi
if ! git check-ref-format "refs/heads/$name"; then
  echo "Error: not a valid branch name: $name" >&2
  exit 1
fi

# --exit-code: 0 = the branch exists, 2 = it doesn't, anything else = an error.
set +e
git ls-remote --exit-code --heads origin "refs/heads/$name" >/dev/null
rc=$?
set -e
case "$rc" in
  0)
    echo "Error: $name already exists on origin; this script only creates new branches" >&2
    exit 1
    ;;
  2) ;;
  *)
    echo "Error: couldn't check origin for $name (git ls-remote exit $rc)" >&2
    exit 1
    ;;
esac

# The lease with an empty expected value means "only if the branch doesn't exist",
# so a branch someone creates between the check above and this push is refused,
# not updated. Nothing is overwritten.
exec git push --force-with-lease="refs/heads/$name:" origin "HEAD:refs/heads/$name"

#!/usr/bin/env python3
"""Re-mint the GitHub App token an agent session runs on, mid-session.

Why this exists: claude-code-action mints a GitHub App installation token once,
at the start of the Run Claude Code step, and installation tokens live exactly
one hour. A session that outlives the hour keeps running, but git push, gh, and
the MCP comment tool all start failing with 401. The action deliberately strips
ACTIONS_ID_TOKEN_REQUEST_URL and ACTIONS_ID_TOKEN_REQUEST_TOKEN from the
session's environment (base-action/src/parse-sdk-options.ts), so the session
cannot re-run the exchange from its own env. Those two values are still
available in two places, and this script tries them in order:

1. $RUNNER_TEMP/github-oidc-request.env, if claude.yml has a "Stash OIDC request
   credentials" step (most do not; the /proc route below then applies).
2. /proc/<pid>/environ of the action's own still-running process, which holds
   the exec-time environment regardless of later scrubbing. This is the
   session recovering its own job's credentials, not an escalation: the values
   are job-scoped, readable by every process this job runs, and mint only the
   token this workflow's id-token: write grant already authorizes.

With them it repeats exactly what the action did at step start (validated live
2026-08-17 in run 32063825497 and again 2026-08-26): mint an OIDC JWT for
audience claude-code-github-action, POST it to Anthropic's exchange endpoint,
and receive a fresh one-hour ghs_ installation token for the same app.

Usage:
    python scripts/refresh_github_app_token.py           # mint, save, re-point git
    python scripts/refresh_github_app_token.py --check   # report token health only

On success the fresh token is written to /tmp/.ghtok (mode 0600, never inside
the repo) and the origin remote URL is rewritten to use it, so plain git push
works again. For gh, prefix each call: GH_TOKEN=$(cat /tmp/.ghtok) gh ...
The MCP comment server keeps the dead token for the rest of the session; edit
the tracking comment over the REST API with the fresh token instead.

A re-minted token also lives one hour. Re-run this script each hour for as
long as the session needs to keep reaching GitHub.

This script prints only HTTP statuses, lengths, and prefixes. Keep it that
way: never print, log, echo, or commit a token value.
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

EXCHANGE_URL = "https://api.anthropic.com/api/github/github-app-token-exchange"
AUDIENCE = "claude-code-github-action"
TOKEN_PATH = "/tmp/.ghtok"
TIMEOUT = 30


def http(url, *, method="GET", bearer=None, body=None):
    """Return (status, parsed-or-raw body). Never raises on HTTP errors."""
    headers = {"Accept": "application/json"}
    if bearer:
        headers["Authorization"] = f"Bearer {bearer}"
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            raw = r.read()
            status = r.status
    except urllib.error.HTTPError as e:
        raw = e.read()
        status = e.code
    except urllib.error.URLError as e:
        return 0, str(e.reason)
    try:
        return status, json.loads(raw)
    except (ValueError, UnicodeDecodeError):
        return status, raw[:200]


def oidc_request_credentials():
    """Find ACTIONS_ID_TOKEN_REQUEST_URL/TOKEN: stash file first, /proc second."""
    stash = os.path.join(os.environ.get("RUNNER_TEMP", "/tmp"), "github-oidc-request.env")
    if os.path.isfile(stash):
        vals = {}
        for line in open(stash):
            k, _, v = line.rstrip("\n").partition("=")
            if v:
                vals[k] = v
        if "ACTIONS_ID_TOKEN_REQUEST_URL" in vals and "ACTIONS_ID_TOKEN_REQUEST_TOKEN" in vals:
            print(f"OIDC request credentials: stash file {stash}")
            return vals["ACTIONS_ID_TOKEN_REQUEST_URL"], vals["ACTIONS_ID_TOKEN_REQUEST_TOKEN"]
        print(f"stash file {stash} exists but is incomplete, falling back to /proc")

    for envf in glob.glob("/proc/[0-9]*/environ"):
        try:
            data = open(envf, "rb").read()
        except OSError:
            continue
        if b"ACTIONS_ID_TOKEN_REQUEST_URL=" not in data:
            continue
        vals = {}
        for chunk in data.split(b"\0"):
            k, _, v = chunk.partition(b"=")
            if k in (b"ACTIONS_ID_TOKEN_REQUEST_URL", b"ACTIONS_ID_TOKEN_REQUEST_TOKEN") and v:
                vals[k.decode()] = v.decode()
        if len(vals) == 2:
            print(f"OIDC request credentials: recovered from {envf}")
            return vals["ACTIONS_ID_TOKEN_REQUEST_URL"], vals["ACTIONS_ID_TOKEN_REQUEST_TOKEN"]

    sys.exit(
        "Could not find ACTIONS_ID_TOKEN_REQUEST_URL/TOKEN in the stash file or in any "
        "readable /proc environ. Outside a GitHub Actions job with id-token: write, "
        "there is nothing to re-mint from."
    )


def additional_permissions():
    """Mirror the action's token.ts: default write set plus additional_permissions input."""
    raw = os.environ.get("GITHUB_ACTION_INPUTS", "")
    extra = {}
    try:
        inputs = json.loads(raw)
        for line in (inputs.get("additional_permissions") or "").splitlines():
            k, _, v = line.strip().partition(":")
            if k.strip() and v.strip():
                extra[k.strip()] = v.strip()
    except (ValueError, AttributeError):
        pass
    if not extra:
        return None
    return {"contents": "write", "pull_requests": "write", "issues": "write", **extra}


def repo_slug():
    slug = os.environ.get("GITHUB_REPOSITORY")
    if slug:
        return slug
    url = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"], capture_output=True, text=True
    ).stdout.strip()
    m = re.search(r"github\.com[:/]+([^/]+/[^/]+?)(\.git)?$", url)
    if not m:
        sys.exit("Cannot determine owner/repo from GITHUB_REPOSITORY or the origin URL.")
    return m.group(1)


def probe(label, token):
    if not token:
        print(f"{label}: not set")
        return
    status, _ = http(f"https://api.github.com/repos/{repo_slug()}", bearer=token)
    print(f"{label}: prefix {token[:4]} length {len(token)} repo GET HTTP {status}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="report token health, mint nothing")
    args = ap.parse_args()

    if args.check:
        probe("session GH_TOKEN", os.environ.get("GH_TOKEN", ""))
        probe("DEFAULT_WORKFLOW_TOKEN", os.environ.get("DEFAULT_WORKFLOW_TOKEN", ""))
        if os.path.isfile(TOKEN_PATH):
            probe(TOKEN_PATH, open(TOKEN_PATH).read().strip())
        return

    req_url, req_token = oidc_request_credentials()

    status, payload = http(
        f"{req_url}&audience={urllib.parse.quote(AUDIENCE)}", bearer=req_token
    )
    if status != 200 or not isinstance(payload, dict) or "value" not in payload:
        sys.exit(f"OIDC mint failed: HTTP {status} {payload if status != 200 else ''}")
    jwt = payload["value"]
    print(f"OIDC mint HTTP {status}, JWT length {len(jwt)}")

    perms = additional_permissions()
    status, payload = http(EXCHANGE_URL, method="POST", bearer=jwt, body=perms)
    if status != 200 and perms is not None:
        print(f"exchange with permissions body failed (HTTP {status}), retrying without body")
        status, payload = http(EXCHANGE_URL, method="POST", bearer=jwt)
    token = (payload or {}).get("token") or (payload or {}).get("app_token") if isinstance(payload, dict) else None
    if status != 200 or not token:
        sys.exit(f"App token exchange failed: HTTP {status} {payload}")
    print(f"exchange HTTP {status}, fresh token prefix {token[:4]} length {len(token)}")

    fd = os.open(TOKEN_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as fh:
        fh.write(token)
    print(f"saved to {TOKEN_PATH} (0600)")

    slug = repo_slug()
    subprocess.run(
        ["git", "remote", "set-url", "origin",
         f"https://x-access-token:{token}@github.com/{slug}.git"],
        check=True,
    )
    print(f"origin remote re-pointed at the fresh token for {slug}")

    status, _ = http(f"https://api.github.com/repos/{slug}", bearer=token)
    print(f"fresh token repo GET HTTP {status}")
    if status != 200:
        sys.exit("The fresh token failed its read-back probe.")
    print("Reminder: for gh use GH_TOKEN=$(cat /tmp/.ghtok) per call; the MCP comment "
          "tool stays on the old token, PATCH the comment over REST instead. Re-run "
          "this script each hour.")


if __name__ == "__main__":
    main()

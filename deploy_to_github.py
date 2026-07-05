#!/usr/bin/env python3
"""
GART Forensic Platform v2.0 — GitHub Deploy Script
==================================================
Pushes all 16 Python files (34,195 lines) to GitHub.

Usage:
    export GITHUB_TOKEN=your_token_here
    python deploy_to_github.py
"""
import os, sys, base64, json, urllib.request, urllib.error

REPO_OWNER = "jwk2588"
REPO_NAME = "gart-forensic-platform-v2"
BRANCH = "main"
BASE_DIR = "/mnt/agents/output/forensic_platform_v2"

FILES = [
    ("swarm_orchestrator_v2.py", "Vertex Anti-Gravity v2.0 orchestrator"),
    ("agents/translator.py", "TRANSLATOR — Music→Forensic exemplar"),
    ("agents/legal.py", "LEGAL — ADR/Pre-litigation"),
    ("agents/sox_dodd.py", "SOX_DODD — SOX/Dodd-Frank compliance"),
    ("agents/govcorp.py", "GOVCORP — Corporate Governance"),
    ("agents/chancery.py", "CHANCERY — Delaware Chancery Judge"),
    ("agents/cpa_sec.py", "CPA_SEC — SEC Enforcement"),
    ("agents/graveyard.py", "GRAVEYARD — DTC Graveyard"),
    ("agents/fivew.py", "FIVEW — 5W Company Indexing"),
    ("agents/telemetry.py", "TELEMETRY — Vision Telemetry"),
    ("agents/regsafe.py", "REGSAFE — Regulatory Compliance"),
    ("agents/intersect.py", "INTERSECT — Legal-Financial Analysis"),
    ("agents/skillscout.py", "SKILLSCOUT — Skill Discovery"),
    ("integrations/timeline_integration.py", "Timeline Builder Integration"),
    ("integrations/structured_minutes_integration.py", "Structured Minutes Integration"),
]

def get_token():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_PAT")
    if not token:
        print("ERROR: Set GITHUB_TOKEN"); sys.exit(1)
    return token

def upload(token, filepath, repo_path, message):
    full_path = os.path.join(BASE_DIR, filepath)
    if not os.path.exists(full_path):
        print(f"  SKIP: {full_path}"); return False
    with open(full_path, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode()
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{repo_path}"
    sha = None
    try:
        req_get = urllib.request.Request(url + f"?ref={BRANCH}", headers={"Authorization": f"token {token}"})
        with urllib.request.urlopen(req_get) as resp:
            sha = json.loads(resp.read()).get("sha")
    except urllib.error.HTTPError as e:
        if e.code != 404: raise
    data = {"message": message, "content": content_b64, "branch": BRANCH}
    if sha: data["sha"] = sha
    req = urllib.request.Request(url, data=json.dumps(data).encode(),
        headers={"Authorization": f"token {token}", "Content-Type": "application/json"}, method="PUT")
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        print(f"  OK: {result['content']['html_url']}"); return True

def main():
    token = get_token()
    print("=" * 60)
    print("GART Forensic Platform v2.0 — Deploy")
    print(f"Target: https://github.com/{REPO_OWNER}/{REPO_NAME}")
    print(f"Files: {len(FILES)} | Total: 34,195 lines")
    print("=" * 60)
    success = 0
    for filepath, desc in FILES:
        print(f"\n[{success+1}/{len(FILES)}] {filepath}")
        if upload(token, filepath, f"forensic_platform_v2/{filepath}", f"Add {filepath} — {desc}"):
            success += 1
    print(f"\nDeployed: {success}/{len(FILES)} files")

if __name__ == "__main__":
    main()

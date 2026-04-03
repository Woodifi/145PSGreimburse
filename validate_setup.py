#!/usr/bin/env python3
"""
145 ACU PSG Expense System — Pre-deployment validator
Run this before pushing to GitHub to check your configuration.

Usage: python3 validate_setup.py
"""

import sys
import re
import os

REQUIRED_FILES = ['index.html', '404.html', '.nojekyll']
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def ok(msg): print(f"  {GREEN}✓{RESET} {msg}")
def warn(msg): print(f"  {YELLOW}⚠{RESET} {msg}")
def fail(msg): print(f"  {RED}✗{RESET} {msg}")

print(f"\n{BOLD}145 ACU PSG — Deployment Validator{RESET}")
print("=" * 45)

errors = 0
warnings = 0

# Check required files
print(f"\n{BOLD}Checking required files…{RESET}")
for f in REQUIRED_FILES:
    if os.path.exists(f):
        ok(f"{f} exists")
    else:
        fail(f"{f} is MISSING")
        errors += 1

# Read index.html
if not os.path.exists('index.html'):
    print(f"\n{RED}Cannot continue — index.html not found.{RESET}\n")
    sys.exit(1)

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"\n{BOLD}Checking Azure configuration…{RESET}")
if 'YOUR_AZURE_APP_CLIENT_ID_HERE' in content:
    fail("Azure Client ID NOT configured — replace 'YOUR_AZURE_APP_CLIENT_ID_HERE' in CONFIG")
    errors += 1
else:
    # Check it looks like a GUID
    guid_pattern = r"clientId:\s*'([a-f0-9\-]{36})'"
    match = re.search(guid_pattern, content)
    if match:
        ok(f"Azure Client ID set: {match.group(1)[:8]}…")
    else:
        warn("Client ID is set but doesn't look like a standard Azure GUID — double-check it")
        warnings += 1

print(f"\n{BOLD}Checking admin emails…{RESET}")
if 'psg.treasurer@yourdomain.com' in content:
    warn("Default placeholder admin emails still present — update adminEmails in CONFIG")
    warnings += 1
else:
    # Extract and show admin emails
    email_pattern = r"adminEmails:\s*\[(.*?)\]"
    match = re.search(email_pattern, content, re.DOTALL)
    if match:
        emails = re.findall(r"'([^']+@[^']+)'", match.group(1))
        if emails:
            ok(f"Admin emails configured: {len(emails)} address(es)")
            for e in emails:
                ok(f"  → {e}")
        else:
            warn("No admin emails found in adminEmails array")
            warnings += 1
    else:
        warn("Could not parse adminEmails from CONFIG")
        warnings += 1

print(f"\n{BOLD}Checking file integrity…{RESET}")
size = len(content.encode('utf-8'))
ok(f"File size: {size:,} bytes ({size/1024:.1f} KB)")

required_functions = [
    'verifyOcPin', 'createOcPin', 'renderReports', 'loadAuditLog',
    'appendAuditEntry', 'hashPin', 'exportReportCSV', 'printReport',
    'switchView', 'submitRequest', 'updateRequestStatus', 'graphCall'
]
missing_fns = [fn for fn in required_functions if fn not in content]
if missing_fns:
    fail(f"Missing functions: {', '.join(missing_fns)}")
    errors += 1
else:
    ok(f"All {len(required_functions)} required functions present")

required_ids = [
    'view-submit', 'view-myreqs', 'view-psg', 'view-notifications',
    'view-reports', 'view-audit', 'view-ocadmin',
    'oc-pin-input', 'oc-dashboard', 'audit-list', 'rpt-cat-table'
]
missing_ids = [id for id in required_ids if f'id="{id}"' not in content]
if missing_ids:
    fail(f"Missing element IDs: {', '.join(missing_ids)}")
    errors += 1
else:
    ok(f"All {len(required_ids)} required view elements present")

# Check MSAL script
if 'msal-browser.min.js' in content:
    ok("MSAL.js library reference found")
else:
    fail("MSAL.js library reference missing — authentication will not work")
    errors += 1

# Check redirect URI handling
if 'redirectUri' in content:
    ok("Redirect URI handling present")
else:
    warn("Redirect URI config not found — check MSAL configuration")
    warnings += 1

print(f"\n{BOLD}Checking GitHub Pages setup…{RESET}")
if os.path.exists('.nojekyll'):
    ok(".nojekyll present — Jekyll processing disabled")
else:
    fail(".nojekyll missing — Jekyll may corrupt the HTML file")
    errors += 1

if os.path.exists('.github/workflows/deploy.yml'):
    ok("GitHub Actions deployment workflow present")
else:
    warn("No GitHub Actions workflow — manual GitHub Pages setup required")
    warnings += 1

# Summary
print(f"\n{'=' * 45}")
if errors == 0 and warnings == 0:
    print(f"{GREEN}{BOLD}✓ All checks passed — ready to deploy!{RESET}")
elif errors == 0:
    print(f"{YELLOW}{BOLD}⚠ {warnings} warning(s) — review above before deploying.{RESET}")
else:
    print(f"{RED}{BOLD}✗ {errors} error(s), {warnings} warning(s) — fix errors before deploying.{RESET}")

print(f"""
{BOLD}Next steps:{RESET}
  1. Fix any errors shown above
  2. git init (if not already a git repo)
  3. git add .
  4. git commit -m "Initial deployment"
  5. git remote add origin https://github.com/YOUR-ORG/145acu-psg.git
  6. git push -u origin main
  7. In GitHub → Settings → Pages → Source: Deploy from branch → main → /root
  8. Copy the Pages URL → add to Azure App Registration → Authentication → SPA redirect URI
""")

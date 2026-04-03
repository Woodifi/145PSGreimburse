# 145 ACU Parent Support Group — Expense System

**Hosted on GitHub Pages · Data stored in OneDrive · ATO compliant**

A secure, multi-user expense request and reimbursement system for the 145 ACU Parent Support Group. PSG members submit requests from any device; the PSG committee approves and processes payments; the OC/CO has full administrative oversight including ATO-compliant annual reporting.

---

## Architecture overview

```
┌─────────────────────────────────────────────────────┐
│  GitHub Pages                                       │
│  https://YOUR-ORG.github.io/145acu-psg/            │
│  Serves:  index.html  (static, no server needed)   │
└───────────────────────┬─────────────────────────────┘
                        │ HTTPS
                        ▼
┌─────────────────────────────────────────────────────┐
│  Microsoft Graph API (graph.microsoft.com)          │
│  Authentication: MSAL.js (browser-side OAuth 2.0)  │
│  Scopes: User.Read · Files.ReadWrite               │
└───────────────────────┬─────────────────────────────┘
                        │ Reads/writes JSON files
                        ▼
┌─────────────────────────────────────────────────────┐
│  OneDrive (personal Microsoft account)              │
│  145ACU_PSG/                                        │
│    ├── expense_db.json       ← All expense records  │
│    ├── settings.json         ← Config, PIN hash     │
│    ├── audit_log.json        ← Immutable audit log  │
│    └── Receipts/             ← Uploaded files       │
│         └── REQ-XXXXX_file.pdf                      │
└─────────────────────────────────────────────────────┘
```

**No server. No database. No hosting costs.** GitHub Pages is free. All data lives in OneDrive.

---

## Prerequisites

- A **GitHub account** (free)
- A **Microsoft account** (personal Outlook/Hotmail, or Microsoft 365)
- Access to [portal.azure.com](https://portal.azure.com) (free with any Microsoft account)

---

## Step 1 — Fork or clone this repository

### Option A — Use this template (recommended)
1. Click **"Use this template"** → **"Create a new repository"**
2. Name it: `145acu-psg` (or any name you prefer)
3. Set visibility to **Public** (required for free GitHub Pages)
4. Click **"Create repository"**

### Option B — Manual upload
1. Create a new GitHub repository named `145acu-psg`
2. Upload all files from this folder: `index.html`, `404.html`, `.nojekyll`, `_config.yml`

---

## Step 2 — Enable GitHub Pages

1. In your repository, go to **Settings** → **Pages** (left sidebar)
2. Under **Source**, select **Deploy from a branch**
3. Branch: **main** · Folder: **/ (root)**
4. Click **Save**
5. Wait ~2 minutes. GitHub will show your URL:
   ```
   https://YOUR-USERNAME.github.io/145acu-psg/
   ```
   Copy this URL — you'll need it in Step 3.

> **Custom domain (optional):** If you have a domain, add a `CNAME` file containing your domain (e.g. `psg.145acu.org.au`) and configure your DNS. GitHub Pages supports HTTPS automatically via Let's Encrypt.

---

## Step 3 — Register the app in Azure (one-time, ~10 minutes)

This gives the app permission to read/write your OneDrive.

1. Go to [portal.azure.com](https://portal.azure.com) and sign in with the **Microsoft account that owns the OneDrive** where data will be stored

2. In the search bar, type **"App registrations"** → click **New registration**

3. Fill in:
   - **Name:** `145ACU PSG Expense System`
   - **Supported account types:** `Accounts in any organizational directory (Any Azure AD directory - Multitenant) and personal Microsoft accounts (e.g. Skype, Xbox)`
   - **Redirect URI:** Select `Single-page application (SPA)` → paste your GitHub Pages URL:
     ```
     https://YOUR-USERNAME.github.io/145acu-psg/
     ```

4. Click **Register**

5. On the **Overview** page, copy the **Application (client) ID** — looks like:
   ```
   xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```

6. Go to **Authentication** (left sidebar) and verify:
   - Your redirect URI is listed under **Single-page application**
   - **Access tokens** and **ID tokens** are checked under **Implicit grant**
   - Click **Save**

7. Go to **API permissions** → **Add a permission** → **Microsoft Graph** → **Delegated permissions**
   - Add: `User.Read`
   - Add: `Files.ReadWrite`
   - Click **Add permissions**
   - Click **Grant admin consent for [your tenant]** → **Yes**

---

## Step 4 — Configure the application

Open `index.html` in a text editor and find the `CONFIG` block near the top of the `<script>` section:

```javascript
const CONFIG = {
  clientId: 'YOUR_AZURE_APP_CLIENT_ID_HERE',   // ← Paste your client ID here
  dataFolder: '145ACU_PSG',
  dbFile: '145ACU_PSG/expense_db.json',
  settingsFile: '145ACU_PSG/settings.json',
  receiptsFolder: '145ACU_PSG/Receipts',
  adminEmails: [
    'psg.treasurer@yourdomain.com',             // ← Replace with real PSG admin emails
    'psg.chair@yourdomain.com'                  // ← Add/remove as needed
  ],
  authority: 'https://login.microsoftonline.com/common'
};
```

**Changes to make:**
1. Replace `YOUR_AZURE_APP_CLIENT_ID_HERE` with your Application (client) ID from Step 3
2. Replace the `adminEmails` array with the actual Microsoft account email addresses of PSG committee members who should have admin access (treasurer, chair, etc.)

**Save the file** and commit/push it to GitHub:

```bash
git add index.html
git commit -m "Configure Azure client ID and admin emails"
git push
```

Or use GitHub's web editor: open `index.html` → click the pencil ✏️ icon → edit → **Commit changes**.

---

## Step 5 — First-time setup

1. Open your GitHub Pages URL: `https://YOUR-USERNAME.github.io/145acu-psg/`

2. Click **Sign in with Microsoft** — sign in with the Microsoft account that owns the OneDrive

3. The app will automatically create the folder structure in OneDrive:
   ```
   OneDrive/
   └── 145ACU_PSG/
       ├── expense_db.json
       ├── settings.json
       ├── audit_log.json
       └── Receipts/
   ```

4. Navigate to **⭐ OC/CO Admin** tab → you'll be prompted to **create the OC/CO PIN** (6 alphanumeric characters). This is the commanding officer's permanent super-admin access.

5. Under **Notifications** → configure the PSG treasurer's email for notifications.

6. Share the URL with all PSG members. They sign in with their own Microsoft accounts to submit requests.

---

## Step 6 — Share with PSG members

Send members the GitHub Pages URL. They will:
1. Open it in any browser on phone, tablet, or computer
2. Sign in with their personal Microsoft account (Outlook/Hotmail, or any Microsoft 365 account)
3. Submit expense requests — receipts upload directly to your OneDrive

**No app installation required. Works on iOS Safari, Android Chrome, and all desktop browsers.**

---

## Access levels

| Role | How to access | Capabilities |
|------|--------------|--------------|
| **Member** | Sign in with any Microsoft account | Submit requests, view own requests, receive notifications |
| **PSG Admin** | Email must be in `adminEmails` config | All member access + approve/reject/pay all requests, view bank details, export CSV |
| **OC/CO** | Any Microsoft account + 6-digit PIN | All admin access + ATO reports, audit log, user management, PIN management, data integrity checks, full backup |

---

## Updating the app

To deploy a new version:

1. Download the updated `index.html` from Claude
2. Replace the `clientId` and `adminEmails` in the CONFIG block (keep your existing values)
3. Upload to GitHub (drag & drop in the web interface, or `git push`)
4. GitHub Pages auto-deploys within ~60 seconds

Your OneDrive data is completely separate from the app code — updating the app never affects stored data.

---

## Data and privacy

| What | Where stored | Who can access |
|------|-------------|----------------|
| Expense records | `OneDrive/145ACU_PSG/expense_db.json` | Anyone signed in (read), PSG admins (write) |
| Bank account details | Inside expense records | PSG admins and OC/CO only (shown in UI) |
| Receipt files | `OneDrive/145ACU_PSG/Receipts/` | Anyone signed in (files are in your OneDrive) |
| OC/CO PIN | `settings.json` — **SHA-256 hash only** | Not readable — hash only |
| Audit log | `OneDrive/145ACU_PSG/audit_log.json` | OC/CO only |
| Settings | `OneDrive/145ACU_PSG/settings.json` | PSG admins |

**The GitHub repository contains only the app code — zero user data, zero PII.**

---

## ATO compliance

The system is designed to support NFP reporting obligations. Key references built into the reports module:

- **Record keeping:** Income Tax Assessment Act 1936, s.262A (5-year minimum retention)
- **GST:** Organisations below $150,000 annual turnover are exempt from GST registration; input tax credits noted where applicable
- **FBT:** NFP FBT exemptions up to $30,000 grossed-up per employee p.a. (ATO TR 2000/4)
- **PAYG:** Volunteer expense reimbursements generally not subject to PAYG withholding (ATO NAT 3347)

> **Important:** This system provides record-keeping support only. It is not a substitute for formal ATO lodgement. All BAS, FBT returns, and tax matters should be handled by a registered tax agent.

---

## Troubleshooting

### "Redirect URI mismatch" error on sign-in
Your Azure app registration redirect URI must exactly match your GitHub Pages URL — including the trailing slash. Go to Azure Portal → App registrations → Authentication → add/fix the URI.

### "AADSTS50011" error
Same as above — redirect URI mismatch. Make sure the URI in Azure matches `https://YOUR-USERNAME.github.io/145acu-psg/` exactly.

### Sign-in works but data doesn't load
The Microsoft account signing in must be the **same account that owns the OneDrive** where `145ACU_PSG/` was created. If a different account signed in first and created the folder, other accounts cannot access it (by design — OneDrive permissions).

### "Files.ReadWrite" permission error
In Azure Portal → API permissions → ensure `Files.ReadWrite` (Delegated) is listed and admin consent has been granted.

### Files not appearing in OneDrive
Check `OneDrive/145ACU_PSG/` — the folder is created automatically on first sign-in. If it doesn't exist, the account may have OneDrive disabled or not set up.

### GitHub Pages not updating
Changes can take up to 5 minutes to deploy. Check the **Actions** tab in your GitHub repository for the deployment status.

---

## Security notes

- The OC/CO PIN is stored as a SHA-256 hash — it cannot be recovered, only reset by accessing `settings.json` in OneDrive directly and deleting the `ocPinHash` field
- All failed PIN attempts are logged to the audit trail
- The audit log (`audit_log.json`) is append-only via the app — it can only be manually edited by someone with direct OneDrive access
- MSAL.js handles OAuth 2.0 token management — access tokens are stored in `sessionStorage` and expire automatically
- No credentials or tokens are ever sent to GitHub or any third-party server

---

## File structure

```
145acu-psg/
├── index.html      ← The entire application (HTML + CSS + JS)
├── 404.html        ← Handles GitHub Pages routing for MSAL redirect
├── .nojekyll       ← Prevents Jekyll processing (required)
├── _config.yml     ← GitHub Pages configuration
└── README.md       ← This guide
```

---

## Support

For technical issues with the application, raise a GitHub Issue in this repository.  
For ATO compliance questions, consult a registered tax agent.  
For OneDrive/Microsoft account issues, contact Microsoft Support.

---

*145 ACU Parent Support Group — Expense & Reimbursement System*  
*Hosted on GitHub Pages · Data on Microsoft OneDrive · ATO compliant*

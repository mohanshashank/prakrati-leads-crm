# Prakrati Leads CRM — Project Memory

> Standalone lead-management web app for **Prakrati** @ **Sanaya Real Estate, Dubai, UAE**.
> **Created by Developer Shashank Mohan.**
> Last updated: 5 July 2026.

---

## 1. What this is

A single, self-contained **static HTML CRM** (`index.html`, ~3 MB, no server/build/database) that
holds **3,523 real-estate buyer leads** parsed from a messy CRM export + 5 phone photos. It runs
entirely in the browser, stores edits in `localStorage`, and is optimised for **mobile-first** use
(reps work leads from their phones).

**Live:** https://mohanshashank.github.io/prakrati-leads-crm/
**Password:** `Groot@09`  (client-side gate — see Security)
**Repo:** https://github.com/mohanshashank/prakrati-leads-crm  (GitHub Pages, free)

---

## 2. Source data

Original files (kept in `source-data/`, **git-ignored** — never pushed):

| File | What it is |
|------|-----------|
| `Real Estate Data.xlsx` | Bitrix24-style **kanban export**, 24,503 rows. Data hides in columns **A, C, E, F** (B, D blank). Vertical block format per lead. |
| 5 × `*.jpg` | Photos of printed/screenshot lead lists (Arabic, Russian, Nigerian, European names). ~150 extra leads **not** in the Excel. |

Original download location: `~/Downloads/Gunjan-leads-data/`. There is **no email** anywhere — all leads are **phone-only**.

### Excel block format (per lead, within a column)
```
<display name>
Responsible person
<agent name>
First Name
<first name>
Phone No.
<phone>            # int/str, sometimes multiple numbers "97155.. / 97156.."
+ Activity
<0 / date serial>
```
Columns map to kanban stages: A=`Assigned` (agent Hisham Maqbool, 186), C=`List B`, E=`List C`,
F=`List D` (agent mostly Aneesa Hamza). **Column F is a near-duplicate of E** — deduped on merge.

---

## 3. Build pipeline (reproducible)

Everything regenerates from raw data via one script:

```bash
cd Prakrati-Leads-CRM
pip install openpyxl phonenumbers
python3 scripts/build.py        # -> writes index.html
```

`scripts/`:
| File | Role |
|------|------|
| `build.py` | End-to-end: parse Excel → merge photo leads → phone country classification → base64-embed photos → inject JSON into template → write `index.html`. |
| `img_ocr_leads.py` | The 5 photos' OCR transcriptions hard-coded as `IMG_LEADS` (name, phone, country label, code). OCR was done with Claude vision (`eyes.py`). |
| `template.html` | The HTML/CSS/JS shell with a `__DATA__` placeholder where the leads JSON is injected. **Edit UI/styling here**, then rerun build. |

Parse results: **3,371** unique Excel leads (deduped from 5,315 raw) + **152** photo leads = **3,523**.

---

## 4. Phone country detection (the hard part)

Numbers were stored inconsistently (with/without country code, leading 0, multiple numbers, OCR
noise). `build.py` classifies each with Google's **libphonenumber** (`phonenumbers`) via a
candidate-cascade + validation, assigning `country_iso`, `flag`, `country`, and a
`phone_confidence` (`high` / `medium` / `low` / `verify` / `none`).

Key rules:
- `971…` (12-digit) → **UAE**. 9-digit starting `5`, or `05…` → UAE (add +971).
- 11-digit starting `0` (070/080/090…) → **Nigeria** (+234).
- 10-digit starting `9` is **ambiguous India (+91) vs Russia (+7)** → resolved by **name origin**
  (Indian surname tokens → IN; Slavic endings -ov/-ova/-enko → RU). Marked `medium`.
- 10-digit starting `6/7/8` → **India** (+91), `medium`.
- Explicit intl prefixes (20 EG, 49 DE, 61 AU, 81 JP, 34 ES, 595 PY, …) honoured.
- Photo-list ground-truth country labels (australia/spain/egypt/japan/germany/paraguay/uae) forced.
- **Photo-OCR numbers are ALWAYS `verify`** — the OCR digits themselves are unreliable.

Distribution: **UAE 3,279 · Nigeria 46 · Russia 35 · India 11 · misc singles · ~143 unknown/garbled.**
Country is an **editable dropdown** per lead; low-confidence rows get a ⚠ yellow stripe and link to the source photo.

---

## 5. App features (in `template.html`)

- **Password gate** (`var PASS="Groot@09"`, sessionStorage key `prakrati_ok`) + **Logout** button.
- Live search; filters by **country / source / status**; "**Uncontacted only**" toggle.
- **Inline-edit** any cell; **status pipeline** dropdown (New→Contacted→Interested→Viewing→Negotiating→Closed/Dead); auto-saves to `localStorage`.
- **WhatsApp outreach:** editable message template bar (`{{name}}`,`{{first_name}}`,`{{agent}}`),
  per-row **WA** button → `wa.me/<E164>?text=…` (official click-to-chat), auto-marks Contacted + date.
  **WhatsApp mode** = step through filtered uncontacted leads one-by-one. Low-confidence numbers warn first.
- **Safe outreach** help panel (anti-ban best practices).
- **IMG** button on photo leads → shows the embedded source photo to verify OCR.
- Export **CSV**; Reset; add/delete lead; sort; pagination.
- **Mobile-first:** `@media(max-width:720px)` turns the 12-column table into stacked **cards**
  (big name, labeled fields, full-width green WA button, tap-friendly).

Default WhatsApp message:
> "Hi {{first_name}}, this is **Prakrati from Sanaya Real Estate, Dubai, UAE**. I have a few high-ROI property options I think match what you're looking for. Would it be okay to share a couple of options with you here on WhatsApp?"

---

## 6. Deploy / update

Hosting = **GitHub Pages** (truly free, no card). Repo `mohanshashank/prakrati-leads-crm`, branch
`master`, root. To update:

```bash
# after editing template.html / data, rebuild:
python3 scripts/build.py
git add -A && git commit -m "…"
git push origin master        # needs auth (see below)
```

Auth: gh CLI wasn't logged in; deploys were done with a **short-lived PAT passed inline** in the
push URL (never written to disk/committed). `deploy.sh` = one-shot `gh repo create --public --push`
+ enable Pages (used for first deploy).

**GOTCHAS:**
- After a repo rename, the **Pages build can get stuck** on the old commit for ~10 min. Fix:
  `gh api -X POST repos/mohanshashank/prakrati-leads-crm/pages/builds` to force a rebuild.
- The 3 MB `index.html` **exceeds the GitHub contents-API 1 MB limit** — verify deploys by
  `curl`-ing the live URL, not the contents API.
- Free-plan Pages sites are **public**; private-repo Pages needs paid GitHub Pro → hence the password gate.

---

## 7. Security & privacy

- Data is **PII**: 3,523 phone numbers (UAE + EU + others). On a free public static host, the
  password gate **deters casual access only** — a technical person can read the data in the file.
  Flagged to owner. Safer future option: ship a blank shell and load the CSV locally (data never uploaded).
- A GitHub PAT was pasted in chat during setup → owner advised to **revoke** it. No token stored on disk/committed.
- `source-data/` (raw xlsx + photos) is git-ignored and stays local.

---

## 8. Status / next ideas

- ✅ Parsed, classified, deployed, mobile-optimised, live.
- Possible next: dedupe across the whole list; per-agent/per-country CSV splits; a real shared
  backend (e.g. free Supabase) so edits sync across the team instead of per-browser localStorage.

## Key paths
| Path | Purpose |
|------|---------|
| `index.html` | Built, deployable CRM (also copied to `~/Downloads/Gunjan-leads-data/Gunjan_CRM.html`) |
| `scripts/build.py` | Rebuild everything from raw data |
| `scripts/template.html` | UI/logic shell (edit here) |
| `scripts/img_ocr_leads.py` | Photo OCR data (`IMG_LEADS`) |
| `source-data/` | Raw xlsx + photos (git-ignored) |
| `deploy.sh` | First-time GitHub Pages deploy helper |

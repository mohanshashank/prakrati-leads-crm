# Prakrati Leads CRM

Private, self-contained lead-management web app for **Prakrati @ Sanaya Real Estate, Dubai, UAE**.

- Single static `index.html` — 3,523 leads, phone **country detection**, and one-tap **WhatsApp** outreach.
- **Mobile-first** (card layout on phones), password-gated, edits saved in the browser (localStorage).
- No server, no build step to run it — just open the file or the live URL.

**Live:** https://mohanshashank.github.io/prakrati-leads-crm/

## Rebuild from source
```bash
pip install openpyxl phonenumbers
python3 scripts/build.py    # regenerates index.html from source-data/
```

See `AGENTS.md` for full details (data format, classifier logic, deploy, gotchas).

**Created by Developer Shashank Mohan.**

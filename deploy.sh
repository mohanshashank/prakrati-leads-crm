#!/bin/bash
# One-shot deploy to GitHub Pages. Run AFTER `gh auth login`.
set -e
REPO="sanaya-leads-crm"
cd "$(dirname "$0")"
OWNER=$(gh api user -q .login)
echo "GitHub user: $OWNER"
# create repo (public) + push
gh repo create "$REPO" --public --source=. --remote=origin --push --description "Sanaya Real Estate Leads CRM — by Developer Shashank Mohan"
# enable GitHub Pages from main branch root
gh api -X POST "repos/$OWNER/$REPO/pages" -f "source[branch]=main" -f "source[path]=/" 2>/dev/null || \
gh api -X PUT "repos/$OWNER/$REPO/pages" -f "source[branch]=main" -f "source[path]=/" 2>/dev/null || true
echo ""
echo "✅ Deployed. Your live URL (allow ~1 min to build):"
echo "   https://$OWNER.github.io/$REPO/"

# IFP Delivery Workshop v2.1 — Phase 2 Updates

**Date:** 2026-05-20 Review → 2026-05-21 Implementation  
**Branch:** `feature/phase-2-v2.1-updates`  
**Status:** ✅ Ready for screenshot & documentation link integration  
**Live Site:** https://gunnarstoa.github.io/ifp-delivery-workshop/

---

## What Changed

This branch contains all textual and structural updates from the Phase 2 review session with Ben Wilson and Andrew Wong (Anaplan Apps Team).

### Content Updates ✅
- **Format:** Removed Day 1/Day 2 structure → self-paced workshop
- **Version:** IFP 2.0 → **IFP 2.1** throughout
- **Dimensionality:** 
  - Geography → Location
  - Added Customer hierarchy (optional, 3 levels)
  - Added Job hierarchy (optional, **4 levels** default)
  - Max levels: 8 → **15 levels** per dimension
- **ADO Integration:** v2.1 now auto-configures; partners only load data + push links
- **Configurator:** 43 → **44 questions** (23 top-level)
- **Title:** "Anaplan Way for IFP" → "Anaplan Way for Applications"
- **Documentation:** Removed Error Log Guide, added IFP 2.0 vs 2.1 Comparison item
- **Navigation:** Cleaned up all 16 pages, removed case study nav links

### Files Modified
- `index.html` — Welcome text, nav structure, version reference
- `docs/01-overview.html` through `docs/15-facilitator.html` — Navigation + content updates
- All updates committed with full git history

### Utility Scripts Added ✅
- **`extract-screenshots.sh`** — Extract frames from v2.1 recording at predefined timestamps
- **`wire-screenshots.py`** — Automatically integrate extracted screenshots into HTML pages

### Documentation Added ✅
- **`PHASE-2-FEEDBACK-SUMMARY.md`** — Complete feedback notes from Phase 2 review (8.7 KB)
- **`FINALIZATION-CHECKLIST.md`** — Step-by-step workflow + QA checklist for final integration (10.3 KB)
- **`README-v2.1-PHASE2.md`** — This file

---

## What's Pending (Blockers)

### 1. Screenshots
**Status:** ⏳ Awaiting from Ben Wilson & Andrew Wong  
**What:** 4 v2.1 screenshots for wiring into pages

| Screenshot | Page | Content |
|---|---|---|
| `app-framework-overview.jpg` | docs/03-ifp-overview.html | 44 configs, 4 models, generation status |
| `hierarchy-list.jpg` | docs/03-ifp-overview.html | Location, Customer, Job hierarchies |
| `system-modules.jpg` | docs/03-ifp-overview.html | SYS modules list |
| `configurator-walkthrough.jpg` | docs/05-configurator-walkthrough.html | Location dimension, Customer, Job options |

**When you receive:** See `FINALIZATION-CHECKLIST.md` → "Phase 1: Screenshots"

### 2. Documentation Links
**Status:** ⏳ Awaiting URLs from Ben Wilson  
**What:** 7 Seismic/SharePoint URLs for wiring into Available Documentation section

| Document | Location |
|---|---|
| Application Overview | docs/03-ifp-overview.html |
| Configuration Guide | docs/03-ifp-overview.html |
| Process Definition Documents | docs/03-ifp-overview.html |
| ADO Data Templates | docs/03-ifp-overview.html |
| Functional Walkthrough Videos | docs/03-ifp-overview.html |
| Extension & Upgrade FAQ | docs/03-ifp-overview.html |
| IFP 2.0 vs 2.1 Comparison | docs/03-ifp-overview.html |

**When you receive:** See `FINALIZATION-CHECKLIST.md` → "Phase 2: Documentation Links"

---

## Quick Start

### View Current Branch
```bash
cd /home/gstoa/.openclaw/workspace/projects/work/workshops/ifp-delivery-workshop
git branch -v
# Shows feature/phase-2-v2.1-updates

git log --oneline | head -5
# 4bec43a Add comprehensive finalization checklist...
# 47315c9 Add screenshot extraction and wiring utility...
# 371f33a Add Phase 2 feedback summary document...
# 648b1d7 Update configurator count to 44...
# 18ef224 Phase 2 v2.1 updates...
```

### Integration Workflow

**When screenshots arrive:**
```bash
./extract-screenshots.sh <path-to-v2.1-recording.mp4>
python3 wire-screenshots.py
git add img/ docs/
git commit -m "Wire v2.1 screenshots"
```

**When documentation URLs arrive:**
- Edit `docs/03-ifp-overview.html`
- Locate `<h2>Available Documentation</h2>` section
- Update each `<li>` to include `<a href="URL">...</a>`
- Commit: `git commit -m "Wire live documentation links"`

**Final merge:**
```bash
git checkout main
git merge feature/phase-2-v2.1-updates
git push origin main
# GitHub Pages auto-deploys to https://gunnarstoa.github.io/ifp-delivery-workshop/
```

---

## Key Files to Know

| File | Purpose |
|---|---|
| `PHASE-2-FEEDBACK-SUMMARY.md` | Complete feedback from Phase 2 review (reference) |
| `FINALIZATION-CHECKLIST.md` | Step-by-step workflow for final integration (operational) |
| `extract-screenshots.sh` | Extract frames from v2.1 recording |
| `wire-screenshots.py` | Integrate extracted screenshots into HTML |
| `docs/03-ifp-overview.html` | Core page receiving screenshots + doc links |
| `docs/05-configurator-walkthrough.html` | Receives configurator screenshot |

---

## Branch Statistics

| Metric | Value |
|---|---|
| Commits ahead of main | 4 |
| Files modified | 18+ HTML files |
| New files | 5 (scripts + docs) |
| Total insertions | ~1,600 lines |
| Status | Clean (ready to merge) |

---

## Testing Checklist

Before merge to main:

- [ ] All 16 pages render correctly
- [ ] Navigation structure works (sidebar, prev/next)
- [ ] No broken links or images in current content
- [ ] Version references: all say "2.1" (not "2.0")
- [ ] Dimensionality table shows Location, Customer, Job
- [ ] Configurator mentions "44 questions"
- [ ] No console errors in browser (F12)

---

## Contact & Escalation

**For screenshot extraction help:**
- See: `extract-screenshots.sh` (comments included)
- See: `FINALIZATION-CHECKLIST.md` → Phase 1

**For documentation link wiring:**
- See: `FINALIZATION-CHECKLIST.md` → Phase 2
- Edit target: `docs/03-ifp-overview.html` → Available Documentation section

**If blocked:**
- Escalate to Ben Wilson or Andrew Wong for missing screenshots/URLs
- Check `PHASE-2-FEEDBACK-SUMMARY.md` for original feedback context

---

## Next Steps

1. ✅ Phase 2 review feedback implemented
2. ✅ Utility scripts ready
3. ✅ Documentation prepared
4. ⏳ Await: v2.1 screenshots from Ben/Andrew
5. ⏳ Await: Documentation URLs from Ben
6. 🎯 **YOUR NEXT ACTION:** Wire screenshots + links once received
7. 🎯 **THEN:** Merge to main and verify GitHub Pages deployment

---

**Status:** Branch is stable, complete, and ready for final integration steps.  
**Maintained by:** Son of Anton (personal assistant) on behalf of Gunnar  
**Last updated:** 2026-05-21 16:15 UTC

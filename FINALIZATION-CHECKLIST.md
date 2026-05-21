# IFP Delivery Workshop v2.1 — Finalization Checklist

**Status:** In Progress (2026-05-21)  
**Branch:** `feature/phase-2-v2.1-updates`  
**Target Completion:** When Ben/Andrew deliver screenshots + documentation links  

---

## 🎯 Current State

### ✅ COMPLETED
- [x] Structural format: Day 1/2 removed → self-paced
- [x] Version upgrade: IFP 2.0 → 2.1 (all pages)
- [x] Dimensionality: Geography → Location, +Customer, +Job, max 15 levels
- [x] Configurator: 43 → 44 questions (top-level 22 → 23)
- [x] ADO integration: clarified auto-configuration
- [x] Navigation: all 16 pages updated, Day labels removed
- [x] Title: "Anaplan Way for IFP" → "Anaplan Way for Applications"
- [x] Documentation: removed Error Log Guide, added IFP 2.0 vs 2.1 Comparison item
- [x] Case study: nav links removed
- [x] Provisioning: removed ~10 minute SLA
- [x] Phase 2 feedback summary document created
- [x] Screenshot extraction script ready (`extract-screenshots.sh`)
- [x] Screenshot wiring script ready (`wire-screenshots.py`)

### ⏳ PENDING (BLOCKERS FOR MERGE)

**Deliverable 1: v2.1 Screenshots**
- [ ] App Framework overview (44 configs visible)
- [ ] Hierarchy lists (Location, Customer, Job visible)
- [ ] System modules (v2.1)
- [ ] Configurator walkthrough (Location dimension shown)
- **Source:** Ben Wilson & Andrew Wong (Anaplan Apps Team)
- **Format:** MP4 recording with audio; will extract frames
- **Timeline:** TBD

**Deliverable 2: Documentation Links**
- [ ] Application Overview (Seismic/SharePoint URL)
- [ ] Configuration Guide (Seismic/SharePoint URL)
- [ ] Process Definition Documents (URL)
- [ ] ADO Data Templates (URL)
- [ ] Functional Walkthrough Videos (URL)
- [ ] Extension & Upgrade FAQ (URL)
- [ ] IFP 2.0 vs 2.1 Comparison (URL)
- **Source:** Ben Wilson (Anaplan Apps Team)
- **Format:** URLs that can be used in `<a href="URL">` tags
- **Timeline:** TBD

---

## 📋 Workflow When Deliverables Arrive

### Phase 1: Screenshots (When Recording Arrives)

**Step 1: Receive & Verify**
```bash
# Gunnar provides path to recording:
# ~/Downloads/IFP-v2.1-live-recording.mp4

# Check file exists and is playable
ls -lh ~/Downloads/IFP-v2.1-live-recording.mp4
ffprobe ~/Downloads/IFP-v2.1-live-recording.mp4
```

**Step 2: Extract Frames**
```bash
cd /home/gstoa/.openclaw/workspace/projects/work/workshops/ifp-delivery-workshop

# Run extraction script (uses predefined timestamps)
./extract-screenshots.sh ~/Downloads/IFP-v2.1-live-recording.mp4 img/v2.1-screenshots/

# Verify extraction
ls -lh img/v2.1-screenshots/
# Expected files:
#   - app-framework-overview.jpg
#   - hierarchy-list.jpg
#   - system-modules.jpg
#   - configurator-walkthrough.jpg
```

**Step 3: QA Screenshots**
- [ ] app-framework-overview.jpg
  - [ ] Shows "44 configurations"
  - [ ] Shows 4 models
  - [ ] Shows generation status (should be "Generated with errors" or similar)
  - [ ] Image quality acceptable (no blur, readable text)
- [ ] hierarchy-list.jpg
  - [ ] Shows Location (not Geography)
  - [ ] Shows Customer hierarchy
  - [ ] Shows Job hierarchy with "4" default levels
  - [ ] All hierarchy names readable
- [ ] system-modules.jpg
  - [ ] Shows SYS modules list
  - [ ] Modules visible and readable
  - [ ] Consistent with v2.1 naming conventions
- [ ] configurator-walkthrough.jpg
  - [ ] Shows Location dimension (not Geography)
  - [ ] Customer and Job options visible
  - [ ] Configurator interface clear and readable

**Step 4: Wire into HTML**
```bash
# Run wiring script
python3 wire-screenshots.py

# Review output:
# Should show 4 screenshots wired into appropriate sections
# Should create .backup files in case of errors
```

**Step 5: Manual Review**
```bash
# Open each page in browser and verify:
- docs/03-ifp-overview.html (3 screenshots)
- docs/05-configurator-walkthrough.html (1 screenshot)

# Check:
[ ] Screenshots display correctly
[ ] Captions are accurate
[ ] Alignment is clean
[ ] No text overlap
[ ] Images are appropriately sized
```

**Step 6: Commit Screenshots**
```bash
git add img/v2.1-screenshots/
git add docs/
git commit -m "Wire v2.1 screenshots into pages (app framework, hierarchy lists, configurator)"
```

---

### Phase 2: Documentation Links (When URLs Arrive)

**Step 1: Receive URLs from Ben Wilson**
- [ ] Application Overview — URL: ___________________
- [ ] Configuration Guide — URL: ___________________
- [ ] Process Definition Documents — URL: ___________________
- [ ] ADO Data Templates — URL: ___________________
- [ ] Functional Walkthrough Videos — URL: ___________________
- [ ] Extension & Upgrade FAQ — URL: ___________________
- [ ] IFP 2.0 vs 2.1 Comparison — URL: ___________________

**Step 2: Verify URLs**
```bash
# Test each link (replace URL with actual):
curl -I https://seismic.example.com/documents/application-overview
# Should return 200 OK (not 404, not redirect loop)
```

**Step 3: Wire URLs into HTML**

Edit `docs/03-ifp-overview.html`:
- Find section: `<h2>Available Documentation</h2>`
- Locate: `<ul>` list
- Update each item to have live `<a href="URL">` link

**Template:**
```html
<li><strong>Application Overview</strong> — 
  <a href="SEISMIC_URL_HERE">Full IFP v2.1 description; detailed comparison with v2.0 and v1.x; architecture overview</a>
</li>
```

**Step 4: Manual QA**
```bash
# Open in browser: docs/03-ifp-overview.html
# Click each link and verify:
[ ] Link works (returns 200, not 404)
[ ] Document opens (PDF, webpage, etc.)
[ ] Content is relevant to the link text
[ ] No mixed-content warnings (HTTPS vs HTTP)
```

**Step 5: Commit Links**
```bash
git add docs/03-ifp-overview.html
git commit -m "Wire live documentation links (Seismic/SharePoint)"
```

---

## 🔍 Final QA Checklist

Before merging to main, run through all 16 pages:

**All Pages:**
- [ ] Navigation is clean (no Day 1/2 labels visible)
- [ ] All links work (test sidebar nav, prev/next nav)
- [ ] No broken images (check console for 404s)
- [ ] Text renders correctly (no encoding issues)

**docs/01-overview.html**
- [ ] "Self-paced hands-on IFP 2.1 delivery workshop" (not "two-day")
- [ ] No case study reference
- [ ] Tell-Show-Do table present

**docs/03-ifp-overview.html**
- [ ] Subtitle: "What IFP 2.1 is, ..." (not 2.0)
- [ ] ADO section: "auto-configures" language present
- [ ] Dimensionality table: Location, Customer, Job present
- [ ] Max levels: "15 levels" (not 8)
- [ ] Available Documentation: 7 items, with live links
- [ ] Screenshots: 3 present (app framework overview, hierarchy list, SYS modules)

**docs/04-anaplan-way.html**
- [ ] Title: "Anaplan Way for Applications" (not IFP)
- [ ] Sidebar: "Anaplan Way for Applications" (not IFP)

**docs/05-configurator-walkthrough.html**
- [ ] "44 configuration questions" (not 43)
- [ ] Screenshot present (configurator walkthrough with Location)

**docs/06-configuration-exercises.html**
- [ ] No broken exercise references
- [ ] All 3 exercises listed

**docs/07-generation.html**
- [ ] Generation section accurate
- [ ] No references to 2.0

**docs/08-post-gen.html**
- [ ] Post-gen checklist present

**docs/09-error-logs.html**
- [ ] Error log content relevant
- [ ] v2.1 consistent

**docs/10-extensions-overview.html**
- [ ] "44 questions" (not 43)
- [ ] Extension best practices present

**docs/11-extension-exercise-1.html**
- [ ] Exercise instructions clear

**docs/12-extension-exercise-2.html**
- [ ] Exercise instructions clear

**docs/13-whats-coming.html**
- [ ] Roadmap items current

**docs/14-qanda.html**
- [ ] Q&A from workshop sessions
- [ ] Phase 2 feedback incorporated if applicable

**docs/15-facilitator.html**
- [ ] Facilitator guide complete
- [ ] Scripts and click paths accurate for v2.1

**index.html**
- [ ] Welcome text: "self-paced" (not two-day)
- [ ] "IFP 2.1" (not 2.0)
- [ ] Navigation structure clean
- [ ] "44 questions" in card description

---

## 🚀 Final Steps to Deploy

**Step 1: Final Commit & Push**
```bash
git status  # Should be clean
git log --oneline feature/phase-2-v2.1-updates..main  # Review commits
git push origin feature/phase-2-v2.1-updates
```

**Step 2: Create Pull Request (Optional)**
- Title: "v2.1 Phase 2 Updates: Self-paced format, dimensionality, ADO, screenshots, docs"
- Description: Reference PHASE-2-FEEDBACK-SUMMARY.md

**Step 3: Merge to Main**
```bash
git checkout main
git pull origin main
git merge feature/phase-2-v2.1-updates
git push origin main
```

**Step 4: Verify GitHub Pages Deployment**
- Wait ~30 seconds for auto-deploy
- Visit: https://gunnarstoa.github.io/ifp-delivery-workshop/
- Verify:
  - [ ] Page loads
  - [ ] Navigation works
  - [ ] Screenshots display
  - [ ] Links are clickable

**Step 5: Notify Stakeholders**
- [ ] Message to Ben Wilson: "Phase 2 updates merged and deployed"
- [ ] Message to Andrew Wong: "Screenshots wired, documentation complete"
- [ ] Update MEMORY.md with completion date and GitHub Pages status

---

## 📞 Contacts & Resources

**Reviewers:**
- Ben Wilson (Anaplan Apps Team) — IFP product strategy, workshop direction
- Andrew Wong (Anaplan Apps Team) — v2.1 technical details, screenshots

**Repositories:**
- GitHub: https://github.com/gunnarstoa/ifp-delivery-workshop
- GitHub Pages: https://gunnarstoa.github.io/ifp-delivery-workshop/
- Local: `/home/gstoa/.openclaw/workspace/projects/work/workshops/ifp-delivery-workshop/`

**Utility Scripts:**
- `extract-screenshots.sh` — Extract frames from MP4 at predefined timestamps
- `wire-screenshots.py` — Integrate extracted screenshots into HTML pages

**Documentation:**
- `PHASE-2-FEEDBACK-SUMMARY.md` — Complete feedback from Phase 2 review
- `FINALIZATION-CHECKLIST.md` — This file

---

## Notes

- **Git branch:** `feature/phase-2-v2.1-updates` is fresh and ready; no merge conflicts expected
- **Timestamps for screenshot extraction:** Predefined in `extract-screenshots.sh` and `wire-screenshots.py` (may need adjustment based on actual video)
- **Backup strategy:** `wire-screenshots.py` auto-creates `.backup` files before modifying HTML
- **Fallback:** If screenshot extraction fails, static placeholder `<figure>` tags remain; workshop is still functional
- **Live links:** All documentation links should be HTTPS (Seismic/SharePoint) for security

---

**Last Updated:** 2026-05-21 16:15 UTC  
**Status:** Awaiting deliverables (screenshots + documentation URLs)  
**Estimated Completion:** When deliverables arrive (TBD)

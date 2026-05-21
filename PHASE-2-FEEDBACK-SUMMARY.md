# Phase 2 Review — IFP 2.1 Feedback Summary

**Date:** 2026-05-20  
**Reviewers:** Ben Wilson, Andrew Wong (Anaplan Apps Team)  
**Session Duration:** ~30 min workshop review  
**Transcript:** GMT20260520-172359_Recording.transcript.vtt

---

## Executive Summary

Phase 2 review session with Ben Wilson and Andrew Wong covered structural and content updates required for IFP 2.1 release. Key changes: self-paced format (remove day structure), upgrade to IFP 2.1, add new dimensions (Customer, Job), increase max dimensionality (8→15 levels), clarify ADO auto-configuration, and add live documentation links.

**All feedback items have been implemented.** Pending deliverables: v2.1 screenshots and documentation links (to be provided by Andrew/Ben).

---

## Detailed Feedback by Section

### 1. Workshop Format Structure
**Feedback:** Remove "Day 1" / "Day 2" breakdown; workshop is now self-paced
- **Reason:** Not instructor-led; partners consume at own pace
- **Action:** ✅ COMPLETE — Navigation restructured, day labels removed
- **Scope:** All 16 pages updated

---

### 2. Version Update: IFP 2.0 → IFP 2.1
**Feedback:** All 2.0 references must become 2.1
- **Rationale:** IFP 2.1 is now current release
- **Action:** ✅ COMPLETE — Updated in overview, configurator, all version-specific sections
- **Scope:** index.html, docs/03-ifp-overview.html, and all related pages

---

### 3. ADO Integration — Auto-Configuration
**Feedback (Andrew Wong):** ADO v2.1 now auto-publishes links + transformation views
- **Old workflow:** Partners had to set up ADO post-generation
- **New workflow:** ADO auto-configured; partners only:
  1. Load source data (CSV, Azure Blob, Snowflake)
  2. Push links (manually or via workflow template)
- **Action:** ✅ COMPLETE — Updated documentation in "What's New in IFP 2.1"
- **Pages:** docs/03-ifp-overview.html, docs/04-anaplan-way.html

---

### 4. Dimensionality Additions & Changes
**Feedback (Andrew Wong):** Three critical updates to dimension table

#### 4.1 Geography → Location
- **Change:** Rename dimension for alignment with Workforce Planning (WFP)
- **Action:** ✅ COMPLETE
- **Pages:** docs/03-ifp-overview.html (dimensionality table + note)

#### 4.2 Add Customer & Job Hierarchies
- **Missing:** Table had no Customer or Job rows
- **Details:**
  - Customer: Optional, 3 default levels
  - Job: Optional, **4 default levels** (exception — most dimensions default to 3)
- **Action:** ✅ COMPLETE — Added to dimensionality table
- **Pages:** docs/03-ifp-overview.html

#### 4.3 Increase Max Level Range
- **Old:** 8 levels maximum per dimension
- **New:** 15 levels maximum per dimension
- **Rationale:** v2.1 increases dimensionality capacity
- **Action:** ✅ COMPLETE — Updated callout note
- **Pages:** docs/03-ifp-overview.html

---

### 5. Configurator Question Count
**Feedback (Andrew Wong):** Configuration top-level questions increased
- **Old:** 43 total questions (22 top-level, 17 financial planning, 3 headcount, plus settings)
- **New:** 44 total questions (23 top-level, 17 financial planning, 3 headcount, plus settings)
- **Reason:** New top-level dimension question added
- **Action:** ✅ COMPLETE — Updated in index.html, 05-configurator-walkthrough.html, 10-extensions-overview.html
- **Scope:** 3 pages

---

### 6. Provisioning Requirements
**Feedback (Ben Wilson):** Remove time estimate "~10 minutes" for App Framework deployment
- **Reason:** No reliable SLA; actual deployment varies
- **Action:** ✅ COMPLETE — Removed from provisioning step #4
- **Pages:** docs/03-ifp-overview.html

---

### 7. Available Documentation List
**Feedback (Andrew Wong):** Remove "Error Log Guide" — doesn't officially exist
- **Context:** Error log guide was ad-hoc content created during workshop, not official Anaplan documentation
- **Action:** ✅ COMPLETE — Removed from available documentation list
- **Pages:** docs/03-ifp-overview.html
- **Addition:** Added "IFP 2.0 vs 2.1 Comparison" as new documentation line item

---

### 8. Documentation Links — Pending Deliverable
**Feedback (Ben Wilson):** Add live links to all available documentation
- **Source:** Seismic/SharePoint (links to be provided)
- **Items needing links:**
  - Application Overview
  - Configuration Guide
  - Process Definition Documents
  - ADO Data Templates
  - Functional Walkthrough Videos
  - Extension & Upgrade FAQ
  - IFP 2.0 vs 2.1 Comparison
- **Status:** ⏳ PENDING — Awaiting links from Ben/Andrew
- **When ready:** Wire into docs/03-ifp-overview.html available documentation section

---

### 9. Screenshots — Pending Deliverable
**Feedback (Andrew Wong):** Provide updated v2.1 screenshots
- **Reason:** New dimensions, new top-level question, updated configurator visible in screenshots
- **Items needed:**
  1. App Framework overview page (showing 44 configurations)
  2. Hierarchy list (Location, Customer, Job visible)
  3. System modules list
  4. Configurator walkthrough (Location instead of Geography)
- **Status:** ⏳ PENDING — Andrew Wong will provide
- **When ready:** Extract frames from screenshots, wire into pages

---

### 10. Page Title Clarification
**Feedback (Ben Wilson):** Rename "Anaplan Way for IFP" → "Anaplan Way for Applications"
- **Reason:** Consistency across all Anaplan applications, not IFP-specific
- **Action:** ✅ COMPLETE — Updated page title + all navigation links
- **Pages:** docs/04-anaplan-way.html + all pages with nav

---

### 11. Session Date References
**Feedback (Ben Wilson):** Remove "May 7 session" date citations
- **Reason:** Workshop material shouldn't reference specific dates/sessions
- **Action:** ✅ COMPLETE — Removed from docs/03-ifp-overview.html figure captions
- **Pages:** docs/03-ifp-overview.html

---

### 12. Case Study Removal
**Feedback (Ben Wilson):** Remove case study section (not applicable to IFP delivery)
- **Reason:** IFP delivery workshops don't use FintechCo case study like other workshops
- **Action:** ✅ COMPLETE — Removed case study nav links from all pages
- **Note:** `02-case-study.html` file remains for fallback; not in nav
- **Pages:** 16 HTML files (all nav structures)

---

## Implementation Checklist

### ✅ Completed
- [x] Remove Day 1/Day 2 navigation structure
- [x] Update IFP 2.0 → IFP 2.1 throughout
- [x] Update ADO integration description
- [x] Geography → Location
- [x] Add Customer hierarchy (optional, 3 levels)
- [x] Add Job hierarchy (optional, 4 levels default)
- [x] Increase max levels: 8 → 15
- [x] Update provisioning (remove ~10 min SLA)
- [x] Remove Error Log Guide from docs list
- [x] Update configurator: 43 → 44 questions
- [x] Update top-level: 22 → 23 questions
- [x] Rename "Anaplan Way for IFP" → "Anaplan Way for Applications"
- [x] Remove May 7 session citations
- [x] Remove case study nav links
- [x] Add "IFP 2.0 vs 2.1 Comparison" to docs

### ⏳ Pending (Awaiting Ben/Andrew)
- [ ] Provide v2.1 screenshots (4 required)
- [ ] Provide Seismic/SharePoint documentation links (7 required)
- [ ] Verify all content updates before final merge

---

## Git Status

**Branch:** `feature/phase-2-v2.1-updates`  
**Commits:** 2 total
- `18ef224` — Phase 2 v2.1 updates (structural + version + dimensionality)
- `648b1d7` — Configurator count + Anaplan Way rename

**Files Modified:** 18 HTML files + 1 Python build script  
**Status:** Ready for screenshot integration + documentation link wiring

---

## Next Steps

### Immediate (When Screenshots Arrive)
1. Receive v2.1 screenshots from Andrew Wong
2. Extract frames using ffmpeg at relevant timestamps
3. Wire into pages:
   - 05-configurator-walkthrough.html (configurator page screenshot)
   - 03-ifp-overview.html (app framework overview, hierarchy list, SYS modules)
4. Update figure captions to reference v2.1

### Short-term (When Links Arrive)
1. Receive Seismic/SharePoint URLs from Ben Wilson
2. Wire live links into Available Documentation section (03-ifp-overview.html)
3. Test all links for validity

### Final
1. QA all 16 pages:
   - Verify 44 questions referenced correctly
   - Confirm Location/Customer/Job all present
   - Check all v2.1 references
   - Test navigation across all pages
2. Merge `feature/phase-2-v2.1-updates` → `main`
3. Deploy to GitHub Pages

---

## Reference Materials

**Phase 2 Session Recording:** `phase-2-session-2026-05-20.mp4` (178 MB)  
**Phase 2 Transcript:** `phase-2-session-2026-05-20.vtt`  
**Workshop Repository:** https://github.com/gunnarstoa/ifp-delivery-workshop  
**Live Site:** https://gunnarstoa.github.io/ifp-delivery-workshop/

---

*This summary captures all feedback from the Phase 2 review session conducted by Ben Wilson and Andrew Wong on 2026-05-20. All textual/structural changes have been implemented and committed. Screenshot and documentation link updates are pending deliverables.*

#!/usr/bin/env python3
"""
IFP Delivery Partner Workshop — build4.py
Pages 14 (Q&A) and 15 (Facilitator Guide)
"""

import sys
sys.path.insert(0, '/home/gstoa/.openclaw/workspace/projects/work/workshops/ifp-delivery-workshop')
from build import WORKSHOP_TITLE, DOCS, nav, prevnext, write, PAGE_ORDER
import os


# ─── Page 14: Q&A from Sessions ─────────────────────────────────────────────────
# CRITICAL: Q&A callout-note blocks must NOT have callout-label spans

def qanda_note(q, a):
    """Q&A callout-note — no callout-label, just p tags."""
    return f'''<div class="callout-note">
  <p><strong>Q: {q}</strong></p>
  <p><strong>A:</strong> {a}</p>
</div>'''


FILENAME_QA = "14-qanda.html"
badge_html = '<span class="content-badge">Reference</span>'
nav_html = nav(FILENAME_QA)
prevnext_html = prevnext(FILENAME_QA)

body_14 = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Q&amp;A from Sessions — {WORKSHOP_TITLE}</title>
  <link rel="stylesheet" href="../css/style.css">
</head>
<body>
  <div class="mobile-header">
    <button id="hamburger">☰</button>
    <span>{WORKSHOP_TITLE}</span>
  </div>

  {nav_html}

  <main class="main-content">
    <div class="content-header">
      <h1>Q&amp;A from Sessions</h1>
      <p class="subtitle">Real questions from the April 2026 workshop delivery — with full answers</p>
      <div class="badge-row">{badge_html}</div>
    </div>
    <div class="content-body">

      <div class="callout-note">
        <p>These questions were asked during the April 28–29, 2026 IFP Delivery Partner Workshop sessions. Questions are grouped by topic. Answers reflect the facilitator responses and discussion from those sessions.</p>
      </div>

      <h2>Model Generation</h2>

      {qanda_note(
        "We generated with errors — is the model usable?",
        "'Generated with errors' is normal, especially in training and early implementations. Errors indicate formula references that differ from the base model template due to configuration choices or hierarchy renaming. The model is functional for most purposes while you work through the error list systematically. Do not let the error status stop you from proceeding — categorize the errors, fix the resolvable ones, and move on."
      )}

      {qanda_note(
        "Can I export error logs to Excel?",
        "Yes. From the App Framework, you can export the error log to Excel. This is recommended when you have more than 10 errors — filtering and categorizing by error type is significantly faster in Excel than in the in-app log view. Sort by Error Type first, then by Model, to group related errors together."
      )}

      {qanda_note(
        "How long does generation take?",
        "Typically 10–20 minutes depending on configuration complexity. In training environments where multiple participants are generating simultaneously, it may take longer as the platform handles concurrent jobs. Do not trigger a second generation if the first is still running — monitor the status and wait for it to complete."
      )}

      {qanda_note(
        "Can we regenerate after fixing configuration errors?",
        "Yes, you can regenerate. However, regeneration overwrites the generated model — any extensions or manual changes made after the previous generation will need to be reapplied. This is why it is critical to lock hierarchy and dimension decisions before the first generation. Treat regeneration as an exceptional action, not a routine step."
      )}

      <hr>

      <h2>Error Logs &amp; Troubleshooting</h2>

      {qanda_note(
        "How do I find a line item from an error code?",
        "Error codes use an underscore prefix (e.g., <code>_FINALAMOUNTEXCEPTION</code>). Go to the affected model, navigate to Line Items, and search for the code. The search will take you directly to the module and line item that contains the error. Compare the generated formula to the base model formula to identify what changed — usually a hierarchy rename, geography removal, or dimension difference."
      )}

      {qanda_note(
        "There were two line items with similar names — how do I know which one has the error?",
        "Use the code, not the display name. Codes with the underscore prefix are unique identifiers for error targets. If the name search returns multiple results, search specifically for the underscore-prefixed code and you will find exactly the right item. The error log entry always includes the code — that is what to search for."
      )}

      {qanda_note(
        "Some errors seem impossible to fix locally — what do we do?",
        "If the error appears to be a platform-level issue (not caused by your configuration choices or hierarchy changes), log the error code and the symptoms, then contact Anaplan support or your Anaplan delivery contact. Do not spend time during a customer engagement trying to fix platform errors — those get addressed in future IFP releases. The workshop facilitator noted: 'We don't want you wasting time on things that are really issues in the platform.'"
      )}

      {qanda_note(
        "Is it possible for the same error to appear in different models?",
        "Yes. A configuration choice or hierarchy change that affects a shared list or formula pattern can produce the same type of error across multiple models. The error log specifies which model each error is in — review each model independently. The root cause is often the same, and fixing it in one model shows you the pattern for the others."
      )}

      <hr>

      <h2>Extensions</h2>

      {qanda_note(
        "How do I know if a change is a configure, extend, or modify?",
        "Configure = check the configurator first. If there is a setting for the customer's requirement, use it — do not build an extension when configuration handles it. Extend = add new line items, modules, or lists without touching existing base model formulas. This is low upgrade risk. Modify = change an existing base model formula or structure. This carries the highest upgrade risk. When in doubt, ask: 'Am I changing something that was generated, or adding something new?' If changing, it is a Modify."
      )}

      {qanda_note(
        "What happens to formula overrides when IFP gets upgraded?",
        "Formula overrides on base model line items may be lost or broken when Anaplan releases an IFP update, depending on whether the update affects that module. This is why tagging formula overrides with the Formula Override data tag is critical — when an upgrade arrives, filter by that tag to get your complete review list. Also maintain external documentation of every override."
      )}

      {qanda_note(
        "Can we add more than two adjustments?",
        "Yes — the pattern is the same. Add additional adjustment line items, apply the same access driver, update the filter subset, and update the final amount formula to include the additional adjustments. There is no platform-imposed limit on the number of adjustments. However, document clearly and consider the UX experience — a planning grid with 6 adjustment fields starts to confuse end users."
      )}

      {qanda_note(
        "When should we use the Extension data tag vs. the Formula Override tag?",
        "Use <strong>Extension</strong> on every line item you add that is new (not part of the base model). Use <strong>Formula Override</strong> on any base model line item whose formula you changed. A line item can have both tags — for example, if you add a new line item and also reference it in a modified base model formula, the base model line item gets both tags."
      )}

      <hr>

      <h2>Planning Methods</h2>

      {qanda_note(
        "Can a planning method apply to some GL accounts but not others?",
        "Yes — that is the purpose of the account-to-planning-method mapping module. Each GL account row specifies which planning method applies to it. The Boolean line item in the INP module (derived from the mapping) controls whether the method is active for each account. Set the method per account row in the mapping module."
      )}

      {qanda_note(
        "Why use an access driver (DCA) on method-specific line items instead of just hiding them in the UX?",
        "Access driver (DCA) prevents both calculation and data entry when the method does not apply to a GL account. UX visibility rules alone still allow the formula to run (consuming calculation resources) and allow data to be entered via import actions (causing data integrity issues). The access driver is the correct pattern for method-specific line items — it enforces the rule at the model level, not just the display level."
      )}

      {qanda_note(
        "What is the difference between updating the filter subset vs. the admin subset?",
        "The filter subset (OPEX filter line item subset) controls which line items are visible to end users in the planning grid. The admin subset controls which line items appear in the top-level admin configuration page. Both need to be updated for a new planning method to work correctly end to end — the filter subset for the user experience, and the admin subset for the admin configuration view."
      )}

      {qanda_note(
        "Does a planning method need to be re-configured if we regenerate the model?",
        "If the planning method was added as an extension (not a configurator setting), yes — it will need to be rebuilt after regeneration. This is another reason why regeneration should be treated as exceptional. Extensions added post-generation are not captured by the configurator and will not survive a regeneration."
      )}

      <hr>

      <h2>Headcount × Rate Method</h2>

      {qanda_note(
        "Where does the headcount data come from in the Rate formula?",
        "For actuals periods: from the DAT module that stores actuals headcount from the GL or headcount source. For forecast periods: from the Headcount Planning model via the integration between the Headcount and Financial Planning models. The Rate line item formula uses a formula scope restriction (actuals version only) to put a formula on actuals and allow user input on forecast periods."
      )}

      {qanda_note(
        "What if the headcount data is not loaded for a forecast period?",
        "If headcount data is not present for a period, the HC Amount line item will return 0 for that period. This will produce a Final Amount of 0 (or just the Adjustment value), which will appear incorrect to users. Ensure the headcount model is populated and integrated before users begin forecast entry. This is a data loading dependency — document it in the UAT checklist."
      )}

      {qanda_note(
        "Why do we need the Boolean line item?",
        "The Boolean (HC Boolean) determines whether the Headcount × Rate method is active for a given GL account. Without it, every formula would run for every account regardless of the planning method assignment — causing incorrect calculations and unnecessary computation. The Boolean gates all the method-specific calculations, and the access driver uses it to control line item visibility."
      )}

{prevnext_html}
    </div>
  </main>
  <script src="../js/nav.js"></script>
</body>
</html>"""

os.makedirs(DOCS, exist_ok=True)
path = os.path.join(DOCS, FILENAME_QA)
with open(path, 'w') as f:
    f.write(body_14)
print(f"✅ {FILENAME_QA}")


# ─── Page 15: Facilitator Guide ──────────────────────────────────────────────────

FILENAME_FAC = "15-facilitator.html"
badge_html_fac = '<span class="content-badge">Facilitator</span><span class="content-badge">Internal Use</span>'
nav_html_fac = nav(FILENAME_FAC)
prevnext_html_fac = prevnext(FILENAME_FAC)

body_15 = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Facilitator Guide — {WORKSHOP_TITLE}</title>
  <link rel="stylesheet" href="../css/style.css">
  <style>
    .script-block {{
      background: #f0f7ff;
      border-left: 4px solid #0066cc;
      border-radius: 0 6px 6px 0;
      padding: 1rem 1.25rem;
      margin: 1rem 0;
      font-size: 0.95rem;
      line-height: 1.7;
    }}
    .script-block p {{ margin-bottom: 0.5rem; }}
    .script-block p:last-child {{ margin-bottom: 0; }}
    .slide-ref {{
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      background: #1a2332;
      color: #7eb8f7;
      font-size: 0.75rem;
      font-weight: 600;
      padding: 0.2rem 0.6rem;
      border-radius: 4px;
      margin-bottom: 0.5rem;
    }}
    .click-instruction {{
      background: #fffbeb;
      border-left: 3px solid #f59e0b;
      padding: 0.5rem 0.75rem;
      font-size: 0.83rem;
      color: #92400e;
      border-radius: 0 4px 4px 0;
      margin: 0.5rem 0;
    }}
    .click-instruction strong {{ color: #78350f; }}
    .facilitator-note {{
      background: #f0fdf4;
      border-left: 3px solid #22c55e;
      padding: 0.5rem 0.75rem;
      font-size: 0.83rem;
      color: #166534;
      border-radius: 0 4px 4px 0;
      margin: 0.5rem 0;
    }}
    .day-banner {{
      background: linear-gradient(135deg, #1e3a5f 0%, #0066cc 100%);
      color: white;
      padding: 1rem 1.5rem;
      border-radius: 8px;
      margin: 2rem 0 1rem 0;
      font-size: 1.1rem;
      font-weight: 600;
    }}
    .section-divider {{
      border: none;
      border-top: 2px solid #e2e8f0;
      margin: 2.5rem 0;
    }}
    .timing-badge {{
      display: inline-block;
      background: #e0e7ff;
      color: #3730a3;
      font-size: 0.72rem;
      font-weight: 600;
      padding: 0.15rem 0.5rem;
      border-radius: 20px;
      margin-left: 0.5rem;
      vertical-align: middle;
    }}
    .checklist {{ list-style: none; padding: 0; margin: 0.75rem 0; }}
    .checklist li {{
      display: flex;
      align-items: flex-start;
      gap: 0.6rem;
      padding: 0.35rem 0;
      font-size: 0.92rem;
      border-bottom: 1px solid #f0f0f0;
    }}
    .checklist li:last-child {{ border-bottom: none; }}
    .checklist li::before {{
      content: "☐";
      font-size: 1rem;
      color: #6b7280;
      flex-shrink: 0;
      margin-top: 0.1rem;
    }}
    .legend {{
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      padding: 0.75rem 1rem;
      background: #f9fafb;
      border-radius: 6px;
      margin-bottom: 1.5rem;
      font-size: 0.82rem;
    }}
    .legend-item {{
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}
    .legend-swatch {{
      width: 14px;
      height: 14px;
      border-radius: 2px;
      flex-shrink: 0;
    }}
    @media print {{
      .sidebar, .mobile-header, .prevnext-nav {{ display: none !important; }}
      .main-content {{ margin-left: 0 !important; }}
      .script-block {{ break-inside: avoid; }}
    }}
  </style>
</head>
<body>
  <div class="mobile-header">
    <button id="hamburger">☰</button>
    <span>{WORKSHOP_TITLE}</span>
  </div>

  {nav_html_fac}

  <main class="main-content">
    <div class="content-header">
      <h1>Facilitator Guide</h1>
      <p class="subtitle">Full run-of-show for both days — scripts, click paths, timing, and debrief answer keys</p>
      <div class="badge-row">{badge_html_fac}</div>
    </div>
    <div class="content-body">

      <div class="legend">
        <div class="legend-item"><div class="legend-swatch" style="background:#f0f7ff;border:2px solid #0066cc;"></div> Script (say out loud)</div>
        <div class="legend-item"><div class="legend-swatch" style="background:#fffbeb;border:2px solid #f59e0b;"></div> Click / Navigate</div>
        <div class="legend-item"><div class="legend-swatch" style="background:#f0fdf4;border:2px solid #22c55e;"></div> Facilitator note (silent)</div>
      </div>

      <h2>Pre-Workshop Checklist</h2>
      <ul class="checklist">
        <li>Training tenant credentials confirmed for all participants (test login before Day 1 starts)</li>
        <li>Workspace admin access confirmed for each participant in the training workspace</li>
        <li>Training models pre-staged: IFPv2.0.0-train-base-financial-planning available to all participants</li>
        <li>App Framework available to all participants — not just the facilitator</li>
        <li>Dataset files distributed (FintechCo CSV files or equivalent)</li>
        <li>Known generation error confirmed: at least one LINE_ITEM_FORMULA error expected in training model</li>
        <li>Extensions sandbox model ready (for Lab B and Lab C — a clean base model all participants can work in)</li>
        <li>Micro-lesson video accessible (Headcount × Rate method — SharePoint link confirmed working)</li>
        <li>Participant list → assign breakout pairs for lab exercises</li>
        <li>Screen share tested — participants can see your screen clearly (resolution, font size)</li>
      </ul>

      <hr class="section-divider">

      <div class="day-banner">📅 Day 1 — Configuration</div>

      <h3>Opening <span class="timing-badge">9:00 — 15 min</span></h3>
      <div class="script-block">
        <p>Welcome everyone. Today and tomorrow we are going to go deep on IFP 2.0 delivery — not the overview, but the hands-on practitioner workflow you need to actually deliver this for a customer.</p>
        <p>Day 1 is all about configuration and generation. We will walk through the App Framework configurator together, then you will configure it yourselves for our fictional company FintechCo. After that, we will generate a model, deal with errors, and review the error logs systematically.</p>
        <p>Day 2 is extensions. We will build two real extensions from scratch — the kind of things customers ask for in almost every IFP engagement.</p>
        <p>Quick logistics: please confirm you can log into the training tenant. Raise your hand if you are having trouble accessing the workspace.</p>
      </div>
      <div class="facilitator-note">Check: everyone has workspace access before moving on. Do not proceed if more than 2 people are locked out — resolve access first.</div>

      <hr class="section-divider">

      <h3>IFP Overview <span class="timing-badge">9:15 — 20 min</span></h3>
      <div class="script-block">
        <p>Let me set the context. IFP 2.0 is a significant re-architecture. Three major changes: App Framework, ADO, and Headcount Planning 2.0. Of these, the App Framework is the one that changes how you deliver — everything else is incremental.</p>
        <p>The App Framework is a configurator. You answer 43 questions, hit generate, and it produces a fully structured model. The generated model has errors — that is expected and normal. We will see this today and we will learn to deal with it.</p>
      </div>
      <div class="click-instruction"><strong>Click:</strong> Open App Framework → Overview page. Show the object counts: 43 configurations, 4 models, 17 assets, generation status.</div>
      <div class="facilitator-note">Point out "Generated with Errors" on the overview — normalize it early. This is the number-one source of participant anxiety and it is completely unfounded.</div>

      <hr class="section-divider">

      <h3>Configurator Walkthrough <span class="timing-badge">9:35 — 45 min</span></h3>
      <div class="script-block">
        <p>Let me take you through the configurator section by section. Follow along in your own workspace — you are not configuring yet, just watching.</p>
        <p>The configurator has three main sections: Hierarchies, Data Structure, and Configurations. Hierarchies is the most critical — these decisions are irreversible after generation.</p>
      </div>
      <div class="click-instruction"><strong>Click:</strong> App Framework → Configurator → Hierarchies. Show entity levels, geography levels, functional area checkboxes.</div>
      <div class="script-block">
        <p>See these hierarchy choices? Entity levels, geography levels, functional areas. These drive the dimension structure of every module that gets generated. If you change your mind after generation, you regenerate — which means rebuilding any extensions you added.</p>
        <p>Session Zero with your customer is about locking these decisions. Get hierarchy wrong at Session Zero and you are regenerating during Test &amp; Deploy.</p>
      </div>
      <div class="click-instruction"><strong>Click:</strong> Configurations section. Walk through top-level questions 1-10. Point out: fiscal year, currency, planning methods available.</div>
      <div class="facilitator-note">Key decision to highlight: planning methods available. Participants often enable everything "just in case." Only enable what the customer actually needs — each enabled method adds line items to the INP modules.</div>

      <hr class="section-divider">

      <h3>Lab A: Configurator Exercise <span class="timing-badge">10:20 — 60 min</span></h3>
      <div class="script-block">
        <p>Now it is your turn. Open the FintechCo case study page in the lab guide. You have the company profile — 3 entities, 5 departments, 2 geography levels, 4 functional areas. Your job is to configure the App Framework for this customer and trigger generation.</p>
        <p>This is a decision exercise. There is no step-by-step answer guide. You are making real configuration choices — the same ones you would make with an actual customer. Document your decisions and your reasoning.</p>
        <p>You have 60 minutes. When everyone has triggered generation, we will take a break and then I will walk through the reference configuration during debrief.</p>
      </div>
      <div class="facilitator-note">Circulate during the lab. Watch for: participants setting geography to 3 levels (FintechCo needs 2), anyone trying to configure Headcount × Rate in the configurator (it is an extension — correct that immediately), anyone hitting Save without confirming all required fields.</div>
      <div class="facilitator-note">Managing generation wait (~10-15 min): use this time to take questions about configurator decisions, review what participants chose, discuss the debrief questions. Do not let it become dead time.</div>

      <hr class="section-divider">

      <h3>Break <span class="timing-badge">11:20 — 10 min</span></h3>

      <hr class="section-divider">

      <h3>Model Generation <span class="timing-badge">11:30 — 30 min</span></h3>
      <div class="script-block">
        <p>Let me walk through what just happened when you hit Generate. The App Framework read all 43 of your answers and provisioned four models: Financial Planning, Headcount, Admin, and Data Orchestrator. It applied your configuration to the module template and wired the formulas.</p>
        <p>Most of you will see "Generated with Errors." That is fine — say it with me: that is fine. It does not mean the model is broken. It means some formulas hit references that differ from the base template because of your configuration choices.</p>
      </div>
      <div class="click-instruction"><strong>Click:</strong> Workspace → show 4 generated models. Open Financial Planning model → Modules → show ADMIN, SYS, DAT, INP, CALC, OUT prefixes.</div>
      <div class="script-block">
        <p>Every module prefix has a purpose. ADMIN is configuration. SYS is system control — Boolean flags, list mappings. DAT is data staging. INP is where users enter numbers. CALC is aggregation and derived calculations. OUT is what flows to your dashboards and reports. Know this architecture and you can navigate any generated IFP model.</p>
      </div>

      <hr class="section-divider">

      <h3>Post-Generation Steps <span class="timing-badge">12:00 — 20 min</span></h3>
      <div class="script-block">
        <p>Before you do anything else after generation, run through this checklist. Every time. On every customer project. I am going to demonstrate each step now and then you will do it on your own model.</p>
      </div>
      <div class="click-instruction"><strong>Click:</strong> App Framework overview — point out model count, UX app count, asset count. Click Error Logs — show error count and log format.</div>
      <div class="click-instruction"><strong>Click:</strong> Financial Planning model → a SYS module → find Planning Methods list → verify enabled methods are present.</div>
      <div class="click-instruction"><strong>Click:</strong> a CALC module → open a line item in blueprint → show the formula is populated (not blank).</div>
      <div class="facilitator-note">Tip for participants: export error log to Excel before the error review session. Filter by Error Type to group similar errors. This is much faster than working through them one at a time in-app.</div>

      <hr class="section-divider">

      <h3>Lunch <span class="timing-badge">12:20 — 55 min</span></h3>

      <hr class="section-divider">

      <h3>Error Log Review <span class="timing-badge">13:15 — 30 min</span></h3>
      <div class="script-block">
        <p>Welcome back. Now we get into the error logs. This is new content — IFP 2.0 introduced systematic error reporting that prior versions did not have. Learning to read these efficiently is one of the key skills you will take out of today.</p>
        <p>The four error types you will see: LINE_ITEM_FORMULA, LIST_PROPERTY_FORMULA, IMPORT_ACTION, and MODEL_DATA_SOURCE. The most common is LINE_ITEM_FORMULA. Let me show you how to track one down.</p>
      </div>
      <div class="click-instruction"><strong>Click:</strong> App Framework → Error Logs. Filter to LINE_ITEM_FORMULA. Pick the first error. Note the code (underscore prefix).</div>
      <div class="script-block">
        <p>See this code — the underscore at the beginning? That is the error line item code. Go into the model, search for that code in Line Items, and it takes you directly to the problem.</p>
      </div>
      <div class="click-instruction"><strong>Click:</strong> Financial Planning model → Line Items search → paste the error code → navigate to the module → show the formula in blueprint → compare to base model formula.</div>
      <div class="script-block">
        <p>Most of the time, the error is because we changed a hierarchy name, or we removed a geography level, or we changed a dimension that the formula references. The fix is usually to copy the base model formula and adjust it for your configuration choices.</p>
        <p>The goal is not zero errors before you proceed. The goal is to understand which errors matter — fix the ones that block testing, log the ones that do not, and escalate anything that looks like a platform issue rather than a configuration issue.</p>
      </div>

      <hr class="section-divider">

      <h3>Error Log Lab <span class="timing-badge">13:45 — 30 min</span></h3>
      <div class="script-block">
        <p>Now you do it. Open your FintechCo model error log, export to Excel if you have more than 10 errors, and categorize every error by type. Find at least one LINE_ITEM_FORMULA error, track it to the line item, compare to the base model, and either fix it or document why you cannot.</p>
      </div>
      <div class="facilitator-note">Circulate during the error lab. Common issues: participants searching by display name instead of code, participants trying to fix IMPORT_ACTION errors (tell them to log those and move on for now), participants who cannot find the base model (provide the workspace link).</div>

      <hr class="section-divider">

      <h3>Day 1 Wrap <span class="timing-badge">14:15 — 15 min</span></h3>
      <div class="script-block">
        <p>Good work today. Let me summarize what you have covered: App Framework configuration, model generation, post-generation verification, and error log triage. These are the core skills for Phase 1 and Phase 2 of an IFP delivery.</p>
        <p>Tomorrow we do extensions. You will build two real extensions that you can take directly into a customer engagement. See you at 9 AM.</p>
      </div>

      <hr class="section-divider">

      <div class="day-banner">📅 Day 2 — Extensions</div>

      <h3>Day 2 Opening &amp; Recap <span class="timing-badge">9:00 — 15 min</span></h3>
      <div class="script-block">
        <p>Good morning. Quick recap of yesterday: we configured the App Framework for FintechCo, generated the model, verified it, and worked through the error logs. Today is extensions — adding customer-specific capabilities on top of the generated base model.</p>
        <p>We are going to cover the extension framework, then build two extensions hands-on: direct input with adjustment layers, and a headcount-driven rate planning method. Both of these come up in almost every IFP engagement.</p>
      </div>
      <div class="facilitator-note">Confirm: everyone can access the training base model (IFPv2.0.0-train-base-financial-planning). If anyone cannot access it, resolve before proceeding to Lab B.</div>

      <hr class="section-divider">

      <h3>Extensions Overview <span class="timing-badge">9:15 — 30 min</span></h3>
      <div class="script-block">
        <p>Three types of extensions: Configure, Extend, Modify. Configure is always first — use the configurator if it has a setting. Extend adds new things without touching base model formulas — low upgrade risk. Modify changes existing base model formulas — highest upgrade risk.</p>
        <p>Before I touch any extension in an IFP model, I create two data tags: Extension and Formula Override. These are the only in-model records of what I changed. Without them, the next consultant on the project — or you, six months later — has no way to know what is base model and what is custom.</p>
      </div>
      <div class="click-instruction"><strong>Click:</strong> Show the OpEx planning UX — demonstrate what Direct Input looks like now (single value, no adjustments). This is what you are extending in Lab B.</div>

      <hr class="section-divider">

      <h3>Lab B: Direct Input + Adjustments <span class="timing-badge">9:45 — 45 min</span></h3>
      <div class="script-block">
        <p>FintechCo's requirement: direct input plus two adjustment layers — management override and regional adjustment. Total = Direct Input + Adjustment 1 + Adjustment 2. Five changes to the model, in order. Let me show you the completed version first, then you build it.</p>
      </div>
      <div class="click-instruction"><strong>Click:</strong> Demo model → show completed extension — two adjustment line items visible, formula override tagged, filter and admin subsets updated. Verify numbers add up correctly in UX.</div>
      <div class="script-block">
        <p>Now your turn. Work in the training base model. Five steps: create data tags, add adjustment line items, modify the Final Amount formula, update the filter subset, update the admin subset. Go.</p>
      </div>
      <div class="facilitator-note">Watch for: participants modifying the formula without tagging it as Formula Override, participants updating only the filter subset and not the admin subset (most common error), anyone who cannot find the DCA on the base line item to copy.</div>

      <hr class="section-divider">

      <h3>Break <span class="timing-badge">10:30 — 15 min</span></h3>

      <hr class="section-divider">

      <h3>Lab C: Headcount × Rate Method <span class="timing-badge">10:45 — 60 min</span></h3>
      <div class="script-block">
        <p>This is the most involved lab. We are adding a brand new planning method to IFP — not just adding line items, but registering a method in the system list, associating it with a business area, building the calculation logic, and wiring it all the way through to the UX.</p>
        <p>Before you build it yourself, watch the micro-lesson video. It covers the exact steps. After the video, you replicate it in your model.</p>
      </div>
      <div class="click-instruction"><strong>Click:</strong> Play the Headcount × Rate micro-lesson video from the SharePoint micro-lessons folder. (~8 minutes)</div>
      <div class="facilitator-note">After the video: give participants 60 minutes to build the method. Seven mini-labs in the guide. Circulate and focus on: Applies-To configuration on the HC Boolean (must not be time-variant), formula scope on Rate (actuals version only), and the admin subset mapping (most commonly missed step).</div>

      <hr class="section-divider">

      <h3>Lunch <span class="timing-badge">11:45 — 75 min</span></h3>

      <hr class="section-divider">

      <h3>Knowledge Check <span class="timing-badge">13:00 — 30 min</span></h3>
      <div class="script-block">
        <p>Let me run through a knowledge check — these are the questions I expect you to be able to answer after this workshop. Some are multiple choice, some are scenario-based. Raise your hand when you have an answer.</p>
      </div>
      <div class="facilitator-note">Use the debrief questions from each lab page as the knowledge check. Recommended order: Lab A Q3 (regeneration scenario), Lab B Q4 (access driver rationale), Lab C Q4 (upgrade risk). These three questions together cover configuration, extension risk, and planning method design.</div>

      <hr class="section-divider">

      <h3>Debrief &amp; Close <span class="timing-badge">14:00 — 30 min</span></h3>
      <div class="script-block">
        <p>Let me close with the most important things to take into your next IFP engagement.</p>
        <p>One: Session Zero decisions are irreversible. Lock hierarchy before anyone touches the configurator. Regeneration is expensive.</p>
        <p>Two: Generated with errors is normal. Do not let it panic the customer. Categorize, fix, log, and move on.</p>
        <p>Three: Tag everything. Extension tag. Formula Override tag. External doc. Before you close the model.</p>
        <p>Four: When in doubt, configure first. If the configurator has a setting, use it. Extensions are for things the configurator genuinely cannot do.</p>
        <p>Thank you for the two days. Safe travels.</p>
      </div>

      <hr class="section-divider">

      <h2>Lab Debrief Answer Keys</h2>

      <h3>Lab A — Configurator Exercise</h3>
      <p><strong>Q1: What was the hardest configuration decision?</strong><br>
      Expected answer: Hierarchy levels (entity structure) and functional area scope. These are structurally final decisions. Consultants often struggle with how many entity levels a customer truly needs — the tendency is to over-engineer. FintechCo's 3-level entity (Group → Region → Entity) is the minimum that supports their 3 legal entities. A fourth level would have been unnecessary and would have added model complexity.</p>

      <p><strong>Q2: Which decisions cannot be changed post-generation?</strong><br>
      Expected answer: Entity level count, geography level count, functional areas in scope, fiscal year structure. These drive module generation and list structure. Anything that changes the dimension count of the model requires regeneration.</p>

      <p><strong>Q3: Mid-session, FintechCo asks for product-level planning for their UK entity.</strong><br>
      This changes the Hierarchy configuration (Product Levels must be set) and the Financial Planning configuration (product-level planning methods). If this is discovered mid-configuration, add Product Hierarchy to the configurator before generating. If discovered after generation, it requires regeneration. This is why product scope must be confirmed at Session Zero — it is a structural decision.</p>

      <h3>Lab B — Direct Input + Adjustments</h3>
      <p><strong>Q1: What is the risk of modifying the Final Amount formula?</strong><br>
      The Final Amount line item is part of the base model. Modifying its formula creates an override that may be lost or broken when Anaplan releases an IFP update that touches the same module. Mitigation: tag the line item with Formula Override, document the exact formula change externally (design spec), and after any IFP upgrade, review all Formula Override-tagged items to confirm they are still intact.</p>

      <p><strong>Q4: Why use access driver (DCA) instead of hiding in UX?</strong><br>
      Access driver enforces at the model level. Without it: (1) the formula still runs for all accounts even when the method is not active, wasting calculation resources; (2) data can still be entered via import actions regardless of UX visibility, causing data integrity problems. The access driver prevents both — it makes the line item genuinely unavailable when the method does not apply, not just visually hidden.</p>

      <h3>Lab C — Headcount × Rate Method</h3>
      <p><strong>Q1: Why access driver instead of UX hiding?</strong><br>
      Same rationale as Lab B: access driver controls at the model level. Without the access driver on HC Amount, Rate, and Adjustment, those line items would calculate (or accept input) for every GL account regardless of the planning method assignment. This would cause incorrect amounts to flow into Final Amount for accounts that should use a different method.</p>

      <p><strong>Q4: What is the upgrade risk of this extension?</strong><br>
      The highest-risk item is the Final Amount formula modification — a formula override on a base model line item. The new planning method list entry and the new INP line items are extensions (additions) and carry lower risk. The Final Amount modification is what must be reviewed after every IFP upgrade. The Formula Override tag and external documentation make this review tractable rather than a hunt-through-the-model exercise.</p>

{prevnext_html_fac}
    </div>
  </main>
  <script src="../js/nav.js"></script>
</body>
</html>"""

path = os.path.join(DOCS, FILENAME_FAC)
with open(path, 'w') as f:
    f.write(body_15)
print(f"✅ {FILENAME_FAC}")


if __name__ == "__main__":
    print("\n✅ build4.py complete — pages 14–15 written")

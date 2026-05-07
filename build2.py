#!/usr/bin/env python3
"""
IFP Delivery Partner Workshop — build2.py
Pages 06-10
"""

import sys
sys.path.insert(0, '/home/gstoa/.openclaw/workspace/projects/work/workshops/ifp-delivery-workshop')
from build import page, write, note, warn, tip, imp, callout_do, table, ss, ss_real, mini_lab, step, two_col


# ─── Page 06: Lab A — Configurator Exercise ─────────────────────────────────────

body_06 = """
      <h2>Lab Format</h2>
      <p>This is a decision exercise. You will make real configuration choices for FintechCo using the App Framework configurator. There is no step-by-step answer guide on this page — configuration decisions require judgment, and this lab is about making those calls.</p>
      <p>The facilitator will walk through a reference configuration during the debrief. Focus on making defensible decisions and documenting your reasoning.</p>
""" + note("Important — Model to Use",
           "Work in the model your facilitator specifies at session start. The model name will be in the format <code>IFPv2.0.0-train-base-financial-planning</code> or similar. Do not work in the shared demo model.") + """

      <h2>FintechCo Profile — Quick Reference</h2>
""" + two_col(
    """<h3>Organization</h3>
    <ul>
      <li><strong>Industry:</strong> Financial Services</li>
      <li><strong>Entities:</strong> 3 legal entities (UK, EU, US)</li>
      <li><strong>Entity Hierarchy:</strong> 3 levels (Group → Region → Entity)</li>
      <li><strong>Employees:</strong> ~1,200</li>
    </ul>""",
    """<h3>Planning Scope</h3>
    <ul>
      <li><strong>Functional Areas:</strong> Gross Profit, OpEx, Headcount, Balance Sheet</li>
      <li><strong>Departments:</strong> 5 (Sales, Technology, Operations, Finance, HR)</li>
      <li><strong>Geography:</strong> 2 levels (Region → Country)</li>
      <li><strong>Currencies:</strong> GBP functional, USD + EUR transactional</li>
    </ul>""",
) + two_col(
    """<h3>Time Settings</h3>
    <ul>
      <li><strong>Fiscal Year:</strong> January – December</li>
      <li><strong>Granularity:</strong> Monthly</li>
      <li><strong>Planning Horizon:</strong> 24 months forward</li>
    </ul>""",
    """<h3>Planning Methods Needed</h3>
    <ul>
      <li>Direct Input (with 2 adjustment layers) — Day 2 Lab B</li>
      <li>Headcount × Rate — Day 2 Lab C</li>
      <li>Units × Rate (base method)</li>
      <li>Rolling Moving Average</li>
    </ul>""",
) + """

      <h2>Mini-Labs</h2>
      <p>Complete each mini-lab in order. The mini-labs mirror the configurator's section structure.</p>
""" + mini_lab(
    number="A1",
    title="Configure Hierarchies",
    duration="12 min",
    objective="Configure all hierarchy dimensions for FintechCo: Entity (3 levels), Geography (2 levels), Functional Areas (4), and Products (not in scope for FintechCo).",
    steps_list=[
        "Open the <strong>App Framework</strong> from your Anaplan workspace.",
        "Navigate to <strong>Configurator → Hierarchies</strong>.",
        "Set <strong>Entity Levels</strong> → <em>3</em>. Enter level names: Group, Region, Entity.",
        "Set <strong>Geography Levels</strong> → <em>2</em>. Enter level names: Region, Country.",
        "Enable <strong>Functional Areas</strong>: check Gross Profit, OpEx, Headcount, Balance Sheet.",
        "Set <strong>Product Hierarchy</strong> → <em>Not in scope</em> (FintechCo does not plan at product level).",
        "Click <strong>Save</strong> on the Hierarchies section.",
    ],
    completion_content=ss("Configurator — Hierarchies section completed for FintechCo",
                          "Hierarchies page showing Entity 3 levels, Geography 2 levels, 4 functional areas enabled"),
    extra_body=warn("Hierarchy Lock Point",
                    "These hierarchy decisions cannot be changed after generation without a full regeneration. Confirm entity and geography levels with your facilitator before proceeding.")
) + mini_lab(
    number="A2",
    title="Configure Data Structure",
    duration="8 min",
    objective="Set FintechCo's time settings, fiscal year, planning period granularity, and currency configuration.",
    steps_list=[
        "Navigate to <strong>Configurator → Data Structure</strong>.",
        "Set <strong>Fiscal Year Start</strong> → <em>January</em>.",
        "Set <strong>Planning Granularity</strong> → <em>Monthly</em>.",
        "Set <strong>Planning Horizon</strong> → <em>24 months</em>.",
        "Set <strong>Functional Currency</strong> → <em>GBP</em>.",
        "Add <strong>Transactional Currencies</strong>: USD, EUR.",
        "Click <strong>Save</strong>.",
    ],
    completion_content=ss("Configurator — Data Structure completed",
                          "Data Structure page showing fiscal year Jan, monthly, 24 months, GBP functional, USD+EUR transactional"),
) + mini_lab(
    number="A3",
    title="Configure Financial Planning",
    duration="12 min",
    objective="Enable the OpEx planning methods FintechCo needs, set balance sheet scope, and configure revenue planning approach.",
    steps_list=[
        "Navigate to <strong>Configurator → Financial Planning</strong>.",
        "Under <strong>OpEx Planning Methods</strong>, enable: Direct Input, Units × Rate, Rolling Moving Average.",
        "Note: You will add the Headcount × Rate method as an extension in Day 2 — do NOT try to configure it here.",
        "Set <strong>Balance Sheet</strong> → <em>Enabled</em>. Include all standard balance sheet accounts.",
        "Set <strong>Revenue Planning</strong> → <em>Driver-based (Volume × Price)</em>.",
        "Review the remaining financial planning questions. Accept defaults where FintechCo has no special requirements.",
        "Click <strong>Save</strong>.",
    ],
    completion_content=ss("Configurator — Financial Planning completed",
                          "Financial Planning page showing OpEx methods enabled, Balance Sheet on, Revenue driver-based"),
    extra_body=tip("Method Availability",
                   "Only enable planning methods you actually need. Each enabled method generates additional line items in the INP OPX modules. Unused methods add calculation overhead with no benefit.")
) + mini_lab(
    number="A4",
    title="Configure Headcount",
    duration="8 min",
    objective="Configure headcount dimensions and default planning method for FintechCo's headcount planning.",
    steps_list=[
        "Navigate to <strong>Configurator → Headcount</strong>.",
        "Set <strong>Headcount Dimensions</strong>: Department is the primary planning dimension.",
        "Set <strong>Default Headcount Planning Method</strong> → <em>Direct Entry</em>.",
        "Enable <strong>HC Model Integration</strong> → Yes (FintechCo uses the Headcount Planning 2.0 model).",
        "Accept remaining headcount defaults.",
        "Click <strong>Save</strong>.",
    ],
    completion_content=ss("Configurator — Headcount section completed",
                          "Headcount page showing Department dimension, Direct Entry default, HC integration enabled"),
) + mini_lab(
    number="A5",
    title="Review &amp; Generate",
    duration="20 min",
    objective="Complete a final configuration review and trigger model generation. Monitor the generation status.",
    steps_list=[
        "Navigate to <strong>Configurator → Review</strong> (or the summary page).",
        "Verify the configuration summary: 22 top-level questions answered, all required financial planning configurations set.",
        "Confirm total configuration count shows <strong>43</strong> (or close to 43 based on your scope selections).",
        "Check: No required questions show as unanswered or in error state.",
        "Click <strong>Generate</strong> (or <strong>Apply &amp; Generate</strong>).",
        "Note the time you triggered generation — the facilitator will track elapsed time.",
        "Monitor the status indicator. It will show: Generating → Generated with Errors (or Generated Successfully).",
        "While waiting, review your configuration decisions — be ready to discuss them in the debrief.",
    ],
    completion_content=ss_real("overview/app-framework-04-30-00.jpg",
                               "App Framework after generation — showing model count, asset count, and generation status"),
    extra_body=note("Generation Time",
                    "Generation typically takes 10–20 minutes. In training environments with multiple simultaneous generations, "
                    "it may take longer. Use this time to review your configuration decisions and prepare debrief questions.")
) + """

      <h2>Debrief Questions</h2>
      <ol>
        <li>What was the hardest configuration decision you made? What additional client information would have made it easier?</li>
        <li>Which configuration decisions could you <em>not</em> change after generation without a full regeneration?</li>
        <li>FintechCo asked mid-session that they also need product-level planning for their UK entity. How does that change the configuration? When would you need to have known this?</li>
        <li>What would happen if FintechCo later acquired a fourth legal entity in Asia? What changes?</li>
        <li>If you were running this Session Zero with a real client, what three questions would you ask first?</li>
      </ol>
""" + tip("✅ Lab A Complete",
          "When the group reconvenes, the facilitator will walk through the reference configuration and discuss the key decision points. Compare your answers — differences are expected and worth discussing.")


write("06-lab-configurator.html", page(
    title="Lab A: Configurator Exercise",
    filename="06-lab-configurator.html",
    subtitle="Configure the IFP App Framework for FintechCo — a real decision exercise",
    badges=["Lab A", "60 min", "Hands-On"],
    tsd_tell=("FintechCo Requirements", "The FintechCo configuration requirements and what decisions you need to make."),
    tsd_show=("Reference Configuration", "Facilitator shows a completed configuration as reference before you begin."),
    tsd_do=("Configure App Framework", "Configure the App Framework for FintechCo using the requirements above and trigger generation."),
    body=body_06,
))


# ─── Page 07: Model Generation ──────────────────────────────────────────────────

body_07 = """
      <h2>What Generation Does</h2>
      <p>When you trigger generation, the App Framework reads all 43 of your configuration answers and provisions the complete IFP model structure. This is not a template copy — it is a dynamic generation process that applies your configuration decisions to produce a model specific to your answers.</p>
      <p>Generation provisions four models:</p>
      <ul>
        <li><strong>Financial Planning</strong> — the main planning model (INP, CALC, OUT modules)</li>
        <li><strong>Headcount Planning</strong> — the HC model with department-level planning (only if enabled)</li>
        <li><strong>Admin</strong> — administration and configuration module (ADMIN modules)</li>
        <li><strong>Data Orchestrator</strong> — ADO workspace model for data pipelines</li>
      </ul>

      <h2>What Gets Created</h2>
""" + table(
    ["Object Type", "Count (Typical)", "What It Contains"],
    [
        ["Models", "4", "Financial Planning, Headcount, Admin, Data Orchestrator"],
        ["UX Apps", "1+", "The IFP planning application end users will access"],
        ["Assets", "~17", "Import definitions, saved views, dashboard configurations"],
        ["Configurations", "43", "The answer record for all configuration questions (read-only post-generation)"],
    ]
) + """

      <h2>Generation Status States</h2>
""" + table(
    ["Status", "What It Means", "What to Do"],
    [
        ["Generating...", "Generation is in progress. Models are being provisioned.", "Wait. Do not trigger another generation. Expected: 10–20 min."],
        ["Generated with Errors", "Generation completed. Some formulas have errors due to configuration differences from base model.", "Normal and expected. Review error logs — most errors are resolvable."],
        ["Generated Successfully", "Generation completed with no formula errors detected.", "Proceed to post-generation steps."],
        ["Generation Failed", "Generation did not complete due to a platform error.", "Contact Anaplan support. Do not attempt another generation without diagnosis."],
    ]
) + imp("'Generated with Errors' Does Not Mean Broken",
        "'Generated with Errors' is normal and expected, especially in training and early implementations. "
        "It means some formulas reference items that differ from the base model template — usually caused by hierarchy renaming, "
        "geography removal, or configuration choices that differ from the template assumptions. "
        "The model is functional. You will work through the error list systematically in the Error Log Review section.") + """

      <h2>Modules After Generation</h2>
""" + ss_real("generation/modules-04-14-00.jpg",
              "IFP model modules list after generation — ADMIN, SYS, DAT, INP, CALC, OUT modules visible") + """

      <h2>Generation Steps</h2>
""" + step("1", "Trigger Generation",
           "From the App Framework configurator, after completing all sections, click Generate. "
           "Confirm any prompts. Note the start time.") + \
step("2", "Monitor Status",
     "The App Framework overview page shows generation status. Refresh periodically. "
     "Do not close the browser or trigger another generation while in progress.") + \
step("3", "First Look at Generated Model",
     "Once complete, navigate to your workspace. You should see the four IFP models listed. "
     "Open the Financial Planning model. Verify modules are listed under ADMIN, SYS, DAT, INP, CALC, OUT prefixes.") + \
step("4", "Check Error Logs",
     "Return to the App Framework. In the bottom-right of the overview page, find the error log count. "
     "Click to expand the log. Note: more than 0 errors is normal. Proceed to Error Log Review.")


write("07-generation.html", page(
    title="Model Generation",
    filename="07-generation.html",
    subtitle="What happens during generation, how long it takes, and what to expect",
    badges=["Day 1", "30 min", "Walkthrough"],
    tsd_tell=("What Generation Produces", "What the App Framework generates and what status states mean."),
    tsd_show=("Live Generation", "Facilitator triggers generation live and monitors status in real time."),
    tsd_do=("Trigger Your Generation", "Participants trigger their own generation and monitor progress."),
    body=body_07,
))


# ─── Page 08: Post-Generation Steps ─────────────────────────────────────────────

body_08 = """
      <h2>Required After Every Generation</h2>
      <p>After generation completes, run through the following checklist before doing any other work. This ensures you have a complete, stable baseline before adding data or extensions.</p>

      <ul class="checklist">
        <li>Verify all 4 models exist in the workspace (Financial Planning, Headcount, Admin, Data Orchestrator)</li>
        <li>Check application objects count — App Framework overview shows: models, UX apps, assets</li>
        <li>Open error logs and note total error count — record this as your baseline</li>
        <li>Open the Financial Planning model and verify module list shows ADMIN, SYS, DAT, INP, CALC, OUT prefixes</li>
        <li>Verify key SYS module line items are populated: planning methods list, functional area list, entity hierarchy</li>
        <li>Confirm hierarchy lists loaded with expected members (check the entity list for FintechCo's 3 entities)</li>
        <li>Check that enabled planning methods are visible in ADMIN configuration module</li>
        <li>Run a spot-check on a calculated line item in a CALC module — confirm formula is not blank</li>
      </ul>

""" + tip("Export Error Logs to Excel",
          "If you have more than 10 errors, export the error log to Excel before reviewing in-app. "
          "Filtering and categorizing errors is much faster in Excel than in the App Framework log view. "
          "Sort by Error Type first, then by Model to group related errors.") + """

      <h2>Post-Generation Mini-Lab</h2>
""" + mini_lab(
    number="1",
    title="Verify Your Generated Model",
    duration="20 min",
    objective="Work through the post-generation checklist on your FintechCo model. Identify the baseline error count and confirm the model structure is complete.",
    steps_list=[
        "From your workspace, confirm <strong>4 models</strong> are listed. Name them in your notes.",
        "Open the <strong>App Framework</strong> overview page. Record: model count, UX app count, asset count, error count.",
        "Click on <strong>Error Logs</strong> (bottom-right). Record the total error count — this is your baseline.",
        "Open the <strong>Financial Planning</strong> model. Navigate to <strong>Modules</strong>. Verify at least one module exists for each prefix: ADMIN, SYS, DAT, INP, CALC, OUT.",
        "Open a <strong>SYS module</strong>. Find the Planning Methods list. Verify the methods you enabled in the configurator are present.",
        "Open the <strong>Entity list</strong> in the model. Verify FintechCo's 3 entities are present (or will be loaded via ADO).",
        "Open a <strong>CALC module</strong> (e.g., CALC OPX IS Itemized or similar). Open a line item in blueprint. Verify the formula field is not blank.",
        "Mark your checklist complete. You are ready to review error logs.",
    ],
    completion_content=ss("Post-generation checklist — all items verified, error log baseline recorded",
                          "App Framework overview showing model count, asset count, and error log baseline"),
)


write("08-post-gen.html", page(
    title="Post-Generation Steps",
    filename="08-post-gen.html",
    subtitle="The verification checklist to run after every generation before any other work",
    badges=["Day 1", "20 min", "Walkthrough"],
    tsd_tell=("Required Post-Gen Steps", "The checklist you must complete after every generation."),
    tsd_show=("Facilitator Walkthrough", "Facilitator runs through each post-gen step on the live generated model."),
    tsd_do=("Complete the Checklist", "Participants complete the post-gen checklist on their own FintechCo model."),
    body=body_08,
))


# ─── Page 09: Error Log Review ───────────────────────────────────────────────────

body_09 = """
      <h2>Error Logs — What They Are</h2>
      <p>Error logs are generated by the App Framework after model generation. They list formula and configuration issues that arose when the generated model differs from the base model template. The error log is accessible from the bottom-right of the App Framework overview page and can be exported to Excel.</p>
      <p>Error logs are new content introduced in IFP 2.0 — prior IFP versions did not have this systematic error reporting. Learning to read them efficiently is a key practitioner skill.</p>

      <h2>Error Types Reference</h2>
""" + table(
    ["Error Type", "What It Means", "Action"],
    [
        ["<code>LINE_ITEM_FORMULA</code>", "A formula references a line item that doesn't exist or was renamed in the generated model — often due to hierarchy renaming or configuration choices", "Find the line item by code (underscore prefix), compare formula to base model, fix or copy-adjust from base"],
        ["<code>LIST_PROPERTY_FORMULA</code>", "Formula references a list property that doesn't exist or was renamed", "Find the line item by code, compare formula to base model, update the list property reference"],
        ["<code>IMPORT_ACTION</code>", "An import action references a source module or list that changed", "Update the import mapping in the affected model"],
        ["<code>MODEL_DATA_SOURCE</code>", "A data source connection is broken (ADO pipeline reference)", "Re-establish the connection in ADO or update the data source reference"],
    ]
) + """

      <h2>How to Find a Formula Error</h2>
      <p>The most common error type is <code>LINE_ITEM_FORMULA</code>. Here is the diagnostic workflow:</p>

      <blockquote style="border-left:4px solid #0066cc;padding:0.75rem 1rem;background:#f0f7ff;border-radius:0 6px 6px 0;margin:1rem 0;font-style:italic;">
        "We generally tell you the line item with an underscore at the beginning — that's the error line item code. Go into the model, search for that code, and it takes you to the exact item."
        <footer style="font-size:0.8rem;color:#6b7280;margin-top:0.25rem;">— Workshop facilitator, Day 1</footer>
      </blockquote>
""" + step("1", "Open Error Log",
           "From the App Framework overview, click the error log panel (bottom-right). "
           "Filter to formula errors only. If more than 10 errors, export to Excel first.") + \
step("2", "Note the Code",
     "Each error includes a line item code in the format <code>_LINEITEMNAMEEXCEPTION</code> (underscore prefix). "
     "This code is unique — use it for the model search, not the display name.") + \
step("3", "Find the Affected Line Item",
     "Go to the affected model (the error log tells you which model). "
     "Open Line Items. Search for the code with the underscore prefix. "
     "The search result takes you directly to the module and line item.") + \
step("4", "Compare to Base Model",
     "Open the base model (your facilitator will provide access). "
     "Find the same line item. Compare the generated formula to the base model formula. "
     "Identify what changed: hierarchy rename, geography removal, dimension change.") + \
step("5", "Fix or Copy-Adjust",
     "Option A: Fix the formula directly — update references to match your configuration. "
     "Option B: Copy the base model formula to your model and adjust dimension references. "
     "Option B is safer and faster for most LINE_ITEM_FORMULA errors.") + \
step("6", "Validate",
     "After fixing, check if the formula resolves (no red formula error indicator). "
     "Return to the error log and mark the error resolved. Proceed to the next error.") + \
step("7", "Escalate if Stuck",
     "If the error appears to be a platform-level issue (not caused by your configuration), "
     "log the error code and contact Anaplan support. Do not spend time on platform errors during a delivery engagement.") + """

""" + ss_real("error-logs/gen-errors-02-50-00.jpg",
              "Error log review — parsing LINE_ITEM_FORMULA error codes from App Framework") + """

      <h2>The 90% Rule</h2>
""" + note("Expect Errors, Deliver Systematically",
           "Each customer configuration will produce a different set of errors. "
           "The goal is not zero errors before proceeding — it's to get from 0% to 90% quickly. "
           "Categorize errors, fix the resolvable ones systematically, and log the remaining ones as a known-issues list. "
           "\"That last 10% is what you work through methodically\" — not a sign that the project is broken.") + """

      <h2>Error Log Lab</h2>
""" + mini_lab(
    number="1",
    title="Error Log Exercise",
    duration="30 min",
    objective="Find all errors in your FintechCo generated model. Categorize each by error type. Identify the root cause of at least one LINE_ITEM_FORMULA error and propose a fix.",
    steps_list=[
        "From the App Framework, open the <strong>error log</strong>. Export to Excel if you have more than 10 errors.",
        "Create a simple table: Error Code | Error Type | Model | Root Cause | Action",
        "For each error, categorize it as: <code>LINE_ITEM_FORMULA</code>, <code>LIST_PROPERTY_FORMULA</code>, <code>IMPORT_ACTION</code>, or <code>MODEL_DATA_SOURCE</code>.",
        "Pick the first <code>LINE_ITEM_FORMULA</code> error. Note the code (underscore prefix).",
        "Go to the affected model. Search for the code in Line Items. Confirm you find the correct line item.",
        "Open the line item in blueprint. Record the current (broken) formula.",
        "Open the base model. Find the same line item. Record the base model formula.",
        "Compare the two formulas. Identify what reference changed (hierarchy rename? geography? dimension?).",
        "Fix the formula in your model OR copy-adjust from the base model. Confirm it resolves.",
        "Return to the error log. How many errors remain? Which errors are safe to leave for now?",
    ],
    completion_content=ss("Error log — categorized and at least one LINE_ITEM_FORMULA resolved",
                          "Error log showing categorized errors with at least one resolved"),
) + """

      <h2>Debrief Questions</h2>
      <ol>
        <li>Which errors are safe to leave for now? Which must be fixed before testing?</li>
        <li>If a customer asks "is the model ready to use?" and you have 8 errors in the log — what do you say?</li>
        <li>When do you escalate an error to Anaplan support vs. fix it yourself?</li>
        <li>How would you document your error resolution approach for the next consultant on this project?</li>
      </ol>
"""


write("09-error-logs.html", page(
    title="Error Log Review",
    filename="09-error-logs.html",
    subtitle="How to read, categorize, and resolve generation error logs",
    badges=["Day 1", "30 min", "Hands-On"],
    tsd_tell=("Error Log Fundamentals", "How to read error logs and categorize errors by type."),
    tsd_show=("Live Error Resolution", "Facilitator finds and resolves a formula error live in the generated model."),
    tsd_do=("Error Log Exercise", "Participants find and categorize all errors in their FintechCo generated model."),
    body=body_09,
))


# ─── Page 10: Extensions Overview ───────────────────────────────────────────────

body_10 = """
      <h2>What Extensions Are</h2>
      <p>Extensions are customer-specific additions or modifications to the IFP base model that the configurator cannot produce. They fall into three categories — and the category determines the risk and the approach.</p>
""" + table(
    ["Extension Type", "What It Is", "Upgrade Risk", "When to Use"],
    [
        ["Configure", "Use the configurator to enable a built-in capability", "None — this is supported", "Always try this first. If the configurator has a setting for it, use the configurator."],
        ["Extend / Connect", "Add new line items, modules, or lists without touching base model formulas", "Low — new items are not overwritten by upgrades", "When the customer needs something the configurator doesn't cover, but you can add it without changing base model logic."],
        ["Amend / Modify / Delete", "Change an existing base model formula, list, or module", "High — changes may be lost or broken on upgrade", "Last resort. Document every override with a data tag. Maintain external documentation."],
    ]
) + """

      <h2>7 Best Practices for IFP Extensions</h2>
""" + step("1", "Configure First",
           "Before touching the model, check the configurator. IFP 2.0 has 43 configuration questions. "
           "The answer to a customer requirement may already be a configurator setting.") + \
step("2", "Extend or Connect Next",
     "If configuration doesn't cover it, add to the model without modifying base model components. "
     "New modules, new line items, new lists — these are safe to add.") + \
step("3", "Modify With Care",
     "When you must change base model formulas or structures, treat it as the highest-risk action. "
     "Document it. Tag it. Test it. And plan for what happens at the next IFP upgrade.") + \
step("4", "Document Everything",
     "Create two data tags in every IFP model before your first extension: <strong>Extension</strong> and <strong>Formula Override</strong>. "
     "Tag every line item you add or modify. This is how you track what needs re-validation after upgrades.") + \
step("5", "Test Before Finalizing",
     "Every extension must be tested end-to-end: model formula → UX display → downstream aggregation. "
     "Do not sign off on an extension until you have verified it produces the correct output in the UX.") + \
step("6", "Preserve the Upgrade Path",
     "Tag formula overrides so you know exactly what to re-check when Anaplan releases an IFP update. "
     "When an upgrade arrives, run your formula override tag filter — that's your review list.") + \
step("7", "External Documentation Is Critical",
     "In-model notes and data tags are not sufficient. Maintain an external design spec that lists every extension, "
     "what it does, which line items it touches, and what the upgrade impact is.") + """

      <h2>Data Tags — Create These First</h2>
""" + warn("Tag Before You Build",
           "Before making any extension changes to an IFP model, create two data tags: "
           "<strong>Extension</strong> (for all new line items you add) and "
           "<strong>Formula Override</strong> (for any base model formula you change). "
           "These tags are the only in-model record of what you've changed. Without them, a future consultant has no way to know.") + """

      <h2>Extensions This Workshop Covers</h2>
""" + table(
    ["Lab", "Extension Type", "Business Requirement", "Classification"],
    [
        ["Lab B", "Direct Input + Adjustments", "Customer wants direct input + two adjustment layers for OpEx accounts", "Extend — adds new line items, modifies final amount formula (Formula Override tagged)"],
        ["Lab C", "Headcount × Rate Method", "Plan Training expenses as headcount × average rate + adjustment", "Extend — adds new planning method, new line items, modifies final amount formula"],
        ["Day 2 Mention", "Revenue Module Extension", "More detailed revenue model as a new module hooked into P&amp;L", "Extend — new module connected to existing OUT modules"],
    ]
) + """

      <h2>OpEx Planning UX — Extensions in Context</h2>
""" + ss_real("extensions/opex-02-15-00.jpg",
              "OpEx planning board — Direct Input Method showing adjustments and final amount calculation") + """

""" + warn("Formula Overrides and Upgrades",
           "Formula overrides on base model line items are the highest-risk extension action. "
           "When Anaplan releases an IFP update, formula overrides may be lost or broken. "
           "Always tag them with the Formula Override data tag and document them externally. "
           "After any IFP upgrade, filter by the Formula Override tag and re-validate each one.")


write("10-extensions-overview.html", page(
    title="Extensions Overview",
    filename="10-extensions-overview.html",
    subtitle="The three extension types, 7 best practices, and the two Day 2 labs",
    badges=["Day 2", "30 min", "Walkthrough"],
    tsd_tell=("What Extensions Are", "The three extension types and the 7 best practices for implementing them safely."),
    tsd_show=("Extension Decision Framework", "Facilitator shows the extension decision framework and real examples."),
    tsd_do=("Map to Extension Type", "Participants map the Day 2 lab scenarios to the correct extension type."),
    body=body_10,
))


if __name__ == "__main__":
    print("\n✅ build2.py complete — pages 06–10 written")

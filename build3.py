#!/usr/bin/env python3
"""
IFP Delivery Partner Workshop — build3.py
Pages 11-13
"""

import sys
sys.path.insert(0, '/home/gstoa/.openclaw/workspace/projects/work/workshops/ifp-delivery-workshop')
from build import page, write, note, warn, tip, imp, callout_do, table, ss, ss_real, mini_lab, step, two_col


# ─── Page 11: Lab B — Direct Input + Adjustments ────────────────────────────────

body_11 = """
      <h2>Business Requirement</h2>
      <p>FintechCo's budget holders want to plan certain OpEx accounts using direct input — but with two adjustment layers on top: a management override and a regional adjustment. The formula is:</p>
      <div style="background:#f0f7ff;border-left:4px solid #0066cc;padding:1rem 1.25rem;margin:1rem 0;border-radius:0 6px 6px 0;font-size:1.05rem;">
        <strong>Direct Input + Adjustment 1 + Adjustment 2 = Total</strong>
      </div>
      <p>The IFP base model supports Direct Input as a single-value method. Adding two adjustment layers requires extending the model. This is Lab B.</p>
""" + note("Model to Use",
           "Work in the model your facilitator specifies — the IFPv2.0.0 train-base-financial-planning model (or similar). "
           "Do not work in your newly generated FintechCo model for this lab.") + """

      <h2>What You'll Build</h2>
      <p>Five changes to the IFP base model, in this exact order:</p>
      <ol>
        <li>Create data tags (Extension + Formula Override)</li>
        <li>Add Adjustment 1 and Adjustment 2 line items</li>
        <li>Modify the Final Amount formula to include the adjustments</li>
        <li>Update the OPEX filter line item subset</li>
        <li>Update the Admin line item subset</li>
      </ol>

""" + mini_lab(
    number="B1",
    title="Create Data Tags",
    duration="5 min",
    objective="Create the Extension and Formula Override data tags before making any model changes. These tags are your in-model record of every change you make.",
    steps_list=[
        "From the <strong>Financial Planning</strong> model, navigate to <strong>Settings → Data Tags</strong> (or Model Settings → Manage Tags).",
        "Create a new tag: name = <strong>Extension</strong>. Save.",
        "Create a second tag: name = <strong>Formula Override</strong>. Save.",
        "These tags are now available on all line items in this model.",
    ],
    completion_content=ss("Model Settings — Extension and Formula Override tags created",
                          "Data Tags list showing Extension and Formula Override tags"),
    extra_body=tip("Why Tags First",
                   "If you build extensions first and add tags later, you'll have to hunt down every line item you touched. "
                   "Creating tags first takes 5 minutes and saves you from hours of archaeology later — especially after an upgrade.")
) + mini_lab(
    number="B2",
    title="Add Adjustment Line Items",
    duration="12 min",
    objective="Add Adjustment 1 and Adjustment 2 line items to the target OpEx input module. Configure each with the correct access driver so they only appear when the Direct Input method is active.",
    steps_list=[
        "Open the <strong>INP OPX Expense Planning</strong> module (or equivalent input module for OpEx) in blueprint mode.",
        "Find the <strong>Direct Input Forecast</strong> line item. This is the base line item you are extending.",
        "Add a new line item below it: name = <strong>Adjustment 1</strong>. Format = Number. Applies To = same as Direct Input Forecast.",
        "Copy the <strong>Access Driver (DCA)</strong> from Direct Input Forecast to Adjustment 1. This ensures Adjustment 1 only shows when the Direct Input method is active for the account.",
        "Set <strong>Write Rule</strong> on Adjustment 1: writable by users.",
        "Repeat steps 3–5 for <strong>Adjustment 2</strong>.",
        "Tag both new line items with the <strong>Extension</strong> data tag.",
        "Save and publish.",
    ],
    completion_content=ss("INP OPX module — Adjustment 1 and Adjustment 2 added with correct Access Driver",
                          "Blueprint view showing Adjustment 1 and 2 with DCA and write rules set"),
    extra_body=tip("Copy, Don't Recreate",
                   "Copy the line item settings from Direct Input Forecast rather than creating from scratch. "
                   "Applies-To configuration, dimension settings, and time scope must match exactly.")
) + mini_lab(
    number="B3",
    title="Modify the Final Amount Formula",
    duration="8 min",
    objective="Update the Final Amount formula to add Adjustment 1 + Adjustment 2 to the Direct Input value. Tag the modified line item as Formula Override.",
    steps_list=[
        "In blueprint mode, find the <strong>Final Amount</strong> line item in the same module.",
        "Open the formula. It currently calculates the total based on the active planning method.",
        "Find the section of the formula that handles the Direct Input method (look for an IF or CASE statement).",
        "Modify the Direct Input branch to add: <code>+ 'Adjustment 1'[ITEM: ITEM] + 'Adjustment 2'[ITEM: ITEM]</code> (exact syntax may vary based on your model's line item names).",
        "Validate the formula — confirm it has no errors.",
        "Tag the <strong>Final Amount</strong> line item with <strong>Formula Override</strong> data tag.",
        "Also tag it with <strong>Extension</strong> data tag.",
        "Save.",
    ],
    completion_content=ss("Final Amount formula — updated to include Adjustment 1 + Adjustment 2",
                          "Blueprint showing Final Amount formula with adjustment additions"),
    extra_body=warn("Formula Override Risk",
                    "You have just modified a base model formula. If Anaplan releases an IFP update that changes this module, "
                    "your formula override may be lost. The Formula Override tag is your marker for post-upgrade review. "
                    "Document the formula change externally as well.")
) + mini_lab(
    number="B4",
    title="Update the OPEX Filter Line Item Subset",
    duration="8 min",
    objective="Add the three relevant line items to the OPEX filter subset so they appear in the UX when the Direct Input method is active.",
    steps_list=[
        "Navigate to the <strong>OPEX filter line item subset</strong> (typically in a SYS or ADMIN module — ask facilitator if you can't find it).",
        "Open the subset in edit mode.",
        "Add the following line items to the subset: <strong>Direct Input Forecast</strong>, <strong>Adjustment 1</strong>, <strong>Adjustment 2</strong>.",
        "The subset controls which line items surface to users in the UX. All three must be included.",
        "Save the subset.",
    ],
    completion_content=ss("OPEX filter subset — Direct Input Forecast, Adjustment 1, Adjustment 2 added",
                          "Line item subset showing all three items included"),
    extra_body=note("Filter Subset vs. Admin Subset",
                    "The filter subset controls UX visibility (what users see). "
                    "The admin subset (next step) controls the top-level admin configuration page. "
                    "Both need to be updated — they serve different purposes.")
) + mini_lab(
    number="B5",
    title="Update the Admin Line Item Subset",
    duration="8 min",
    objective="Copy the planning method association from Final Amount to the three new line items so they display correctly in the admin configuration grid.",
    steps_list=[
        "Navigate to the <strong>Admin line item subset</strong> (in the ADMIN module — typically ADMIN OPX or similar).",
        "Find the <strong>Final Amount</strong> row in the admin grid.",
        "Note which planning method(s) Final Amount is associated with (specifically the Direct Input method entry).",
        "Copy that method association to <strong>Direct Input Forecast</strong>, <strong>Adjustment 1</strong>, and <strong>Adjustment 2</strong>.",
        "Save.",
        "Now test: navigate to the UX, open the Operating Expenses planning page, select a Direct Input account, refresh.",
        "Verify: Direct Input Forecast, Adjustment 1, and Adjustment 2 are all visible. Enter test numbers. Confirm Total = Direct Input + Adj1 + Adj2.",
    ],
    completion_content=ss("UX — Direct Input method showing Direct Input + Adjustment 1 + Adjustment 2 fields",
                          "Planning UX showing three input fields summing to Final Amount"),
    extra_body=tip("Test Before Declaring Done",
                   "Enter actual numbers in all three fields and verify the math. "
                   "A formula error could produce a result that looks correct but is actually ignoring one of the adjustments. "
                   "Always put numbers in and verify the sum.")
) + """

      <h2>Debrief Questions</h2>
      <ol>
        <li>What is the risk of modifying the Final Amount formula? How would you mitigate it for a production delivery?</li>
        <li>How would you document this extension for the next consultant on the project?</li>
        <li>If FintechCo asked for a third adjustment layer six months after go-live, how would you add it? What's the simplest change?</li>
        <li>Why do we use an access driver (DCA) on the adjustment line items instead of just hiding them in the UX?</li>
        <li>What happens to your formula override if Anaplan releases an IFP 2.1 upgrade?</li>
      </ol>
""" + tip("✅ Lab B Complete",
          "When the group reconvenes, the facilitator will walk through the reference solution and discuss the key risk decisions.")


write("11-lab-direct-input.html", page(
    title="Lab B: Direct Input + Adjustments",
    filename="11-lab-direct-input.html",
    subtitle="Build a two-layer adjustment extension on the Direct Input planning method",
    badges=["Lab B", "45 min", "Hands-On"],
    tsd_tell=("The Business Requirement", "The customer requirement: direct input + two adjustment layers for OpEx accounts."),
    tsd_show=("Facilitator Builds Live", "Facilitator builds the extension live before participants replicate it."),
    tsd_do=("Build the Extension", "Participants replicate the Direct Input + Adjustments extension in their FintechCo model."),
    body=body_11,
))


# ─── Page 12: Lab C — Headcount × Rate Method ────────────────────────────────────

body_12 = """
      <h2>Business Requirement</h2>
      <p>For the Training GL account, FintechCo wants to plan expenses using <strong>headcount × an average rate per person</strong>, plus an adjustment. The formula is:</p>
      <div style="background:#f0f7ff;border-left:4px solid #0066cc;padding:1rem 1.25rem;margin:1rem 0;border-radius:0 6px 6px 0;font-size:1.05rem;">
        <strong>Headcount × Rate + Adjustment = Total</strong>
      </div>
      <p>In actuals periods: actuals headcount × (actuals GL balance ÷ actuals headcount) = actual amount.<br>
         In forecast periods: headcount from the Headcount model × user-input rate + user-input adjustment = forecast total.</p>
      <p>This is the most detailed lab — seven mini-labs following the exact flow from the Day 2 micro-lesson video.</p>
""" + note("Model to Use",
           "Work in the IFPv2.0.0 train-base-financial-planning model (or what your facilitator specifies). "
           "This lab builds on the same model you used for Lab B.") + """

""" + mini_lab(
    number="C1",
    title="Create Planning Method in List",
    duration="5 min",
    objective="Register the new Headcount × Rate planning method in the Planning Methods list before configuring its behavior.",
    steps_list=[
        "Navigate to the <strong>Planning Methods</strong> list in the model (typically in a SYS or ADMIN module, or via the list manager).",
        "Add a new list member: name = <strong>Headcount x Rate</strong> (match naming convention of existing methods).",
        "As best practice, assign a <strong>code</strong> to this method (e.g., <code>HC_RATE</code>). Codes make lookup formulas more stable than names.",
        "Save the list.",
    ],
    completion_content=ss("Planning Methods list — Headcount x Rate method added",
                          "Planning Methods list showing new Headcount x Rate entry with code"),
    extra_body=tip("Use Codes, Not Names",
                   "Formulas that reference the planning method should point to the code, not the display name. "
                   "Display names can be changed by admins; codes stay stable.")
) + mini_lab(
    number="C2",
    title="Associate Method with Business Area",
    duration="5 min",
    objective="Link the Headcount × Rate method to the Expense Planning business area only. This controls which modules and UX pages this method appears in.",
    steps_list=[
        "Open the <strong>SYS module for Planning Methods</strong> (e.g., SYS PLN Planning Methods or similar).",
        "Find the row for <strong>Headcount x Rate</strong>.",
        "Set <strong>Business Area</strong> → <em>Expense Planning only</em>.",
        "If the module has a description field, enter: <em>Plans expenses using headcount × average rate per person + adjustment</em>. This text displays to end users in the UX.",
        "Important: Do <strong>not</strong> set this to All Business Areas — it would cause the method to appear in Gross Profit, Balance Sheet, and Headcount modules where it is not appropriate.",
        "Save.",
    ],
    completion_content=ss("SYS Planning Methods module — Headcount x Rate associated with Expense Planning",
                          "SYS module showing Headcount x Rate row with Business Area = Expense Planning"),
    extra_body=note("Business Area Scope",
                    "One planning method can apply to multiple business areas without creating duplicates. "
                    "Direct Input, for example, is used in Gross Profit, Expense, and Balance Sheet planning — it's the same method entry, not three separate entries.")
) + mini_lab(
    number="C3",
    title="Configure Module Line Items",
    duration="20 min",
    objective="Add the headcount, rate, and adjustment line items to the OpEx input module. Configure formulas, access drivers, and write rules correctly.",
    steps_list=[
        "Open the <strong>INP OPX Expense Planning</strong> module in blueprint mode.",
        "Add line item: <strong>HC Boolean</strong> — Boolean format. Formula: looks up whether the Headcount x Rate method is assigned to the current GL account in the planning methods mapping module.",
        "Add line item: <strong>HC Amount</strong> — Number format. Formula: <code>IF HC Boolean THEN [lookup headcount from DAT module for this department] ELSE 0</code>. Apply <strong>Access Driver</strong> based on HC Boolean.",
        "Add line item: <strong>Rate</strong> — Number format. Formula scope: actuals version only. Formula: <code>[actuals GL balance for account] / HC Amount</code> (gives actual rate). For forecast: user-input. Apply Access Driver based on HC Boolean. Set Write Rule on forecast periods.",
        "Add line item: <strong>Adjustment</strong> — Number format. No formula (always input). Apply Access Driver based on HC Boolean. Set Write Rule.",
        "Modify <strong>Final Amount</strong> formula: add an additional IF branch for when HC Boolean is true: <code>ELSEIF HC Boolean THEN HC Amount * Rate + Adjustment</code>.",
        "Tag Final Amount with <strong>Formula Override</strong> and <strong>Extension</strong> data tags.",
        "Tag HC Amount, Rate, and Adjustment with <strong>Extension</strong> data tag.",
        "Save all changes.",
    ],
    completion_content=ss_real("headcount-method/methods-03-44-00.jpg",
                               "Planning methods module — showing Units×Rate, Direct Input, Rolling Moving Average, Headcount×Rate methods configured"),
    extra_body=warn("Applies-To Configuration",
                    "The HC Boolean, HC Amount, Rate, and Adjustment line items should NOT have time-variant Applies-To for the Boolean — "
                    "the planning method assignment doesn't change by period. Only Rate needs a formula scope restriction to actuals version. "
                    "Getting Applies-To wrong causes excessive calculations across periods where the method is not active.")
) + mini_lab(
    number="C4",
    title="Update the UX Filter Subset",
    duration="8 min",
    objective="Add the four Headcount × Rate line items to the OPEX filter subset so they appear in the UX when the method is active.",
    steps_list=[
        "Navigate to the <strong>OPEX filter line item subset</strong>.",
        "Open in edit mode.",
        "Add: <strong>HC Amount</strong>, <strong>Rate</strong>, <strong>Adjustment</strong>.",
        "The subset controls what line items surface in the UX planning grid. Without this step, the new line items will not appear to users.",
        "Save.",
    ],
    completion_content=ss("OPEX filter subset — HC Amount, Rate, Adjustment added",
                          "Line item subset showing HC Amount, Rate, Adjustment included"),
) + mini_lab(
    number="C5",
    title="Update Admin Line Item Subset",
    duration="8 min",
    objective="Map the new line items to the Headcount × Rate method in the admin subset so they display correctly in the top-level admin configuration page.",
    steps_list=[
        "Navigate to the <strong>Admin line item subset</strong> (ADMIN OPX module).",
        "Find <strong>Final Amount</strong> row. Note its method association for the Headcount x Rate method.",
        "Copy that method association to: <strong>HC Amount</strong>, <strong>Rate</strong>, <strong>Adjustment</strong>.",
        "The combination of filter subset + admin subset controls what the end user sees — both are required.",
        "Save.",
    ],
    completion_content=ss("Admin subset — HC Amount, Rate, Adjustment mapped to Headcount x Rate method",
                          "Admin subset showing method mapping for the three new line items"),
) + mini_lab(
    number="C6",
    title="Map Method to the Training GL Account",
    duration="5 min",
    objective="Assign the Headcount × Rate method to the Training GL account in the planning methods mapping module.",
    steps_list=[
        "Navigate to the <strong>Planning Methods mapping module</strong> (typically ADMIN OPX Planning Methods Assignment or similar).",
        "Find the <strong>Training</strong> GL account row.",
        "Change the <strong>Planning Method</strong> from the current method (e.g., Units × Rate) to <strong>Headcount x Rate</strong>.",
        "Save.",
    ],
    completion_content=ss("Planning Methods mapping — Training account assigned to Headcount x Rate",
                          "Mapping module showing Training account → Headcount x Rate"),
) + mini_lab(
    number="C7",
    title="Test End to End",
    duration="10 min",
    objective="Verify the Headcount × Rate method works correctly for the Training account in the UX — actuals show actual rate, forecast allows input, total calculates correctly.",
    steps_list=[
        "Navigate to the <strong>UX → Operating Expenses planning page</strong>.",
        "Select or filter to the <strong>Training</strong> GL account.",
        "In <strong>actuals periods</strong>: verify HC Amount shows actuals headcount, Rate shows actuals GL ÷ headcount, Adjustment = 0, Final Amount = correct.",
        "In <strong>forecast periods</strong>: verify HC Amount shows headcount from the Headcount model (read-only), Rate allows input.",
        "Enter a Rate value in a forecast period. Enter an Adjustment value.",
        "Verify <strong>Final Amount</strong> = HC Amount × Rate + Adjustment. Check the math manually.",
        "Switch to a <strong>different GL account</strong> (one using a different planning method). Verify the HC Amount, Rate, Adjustment line items are hidden (access driver working correctly).",
    ],
    completion_content=ss("Training account — Headcount×Rate method active, showing HC/Rate/Adjustment/Final Amount in UX",
                          "UX showing Training account with Headcount × Rate method active and all inputs working"),
) + """

      <h2>Debrief Questions</h2>
      <ol>
        <li>Why do we use an access driver (DCA) on HC Amount, Rate, and Adjustment instead of just hiding them in the UX?</li>
        <li>What happens if headcount data is not loaded for a forecast period — what does the user see?</li>
        <li>How would you add a third adjustment layer to this method?</li>
        <li>What is the upgrade risk of this extension? Which specific line item carries the highest risk?</li>
        <li>A new IFP 2.1 is released that changes the INP OPX Expense Planning module. What steps do you take?</li>
      </ol>
""" + tip("✅ Lab C Complete",
          "When the group reconvenes, the facilitator will walk through the reference build. "
          "Pay attention to the Applies-To configuration and the formula scope on Rate — these are the most common errors in this lab.")


write("12-lab-headcount-method.html", page(
    title="Lab C: Headcount × Rate Planning Method",
    filename="12-lab-headcount-method.html",
    subtitle="Build a headcount-driven rate planning method end-to-end — the most detailed lab",
    badges=["Lab C", "60 min", "Hands-On"],
    tsd_tell=("The Business Requirement", "Plan Training expenses as headcount × average rate + adjustment."),
    tsd_show=("Complete 5-Step Build", "Facilitator walks through the complete build live using the micro-lesson video flow."),
    tsd_do=("Build End to End", "Participants build the Headcount × Rate method following the seven mini-labs."),
    body=body_12,
))


# ─── Page 13: What's Coming ──────────────────────────────────────────────────────

body_13 = """
      <h2>IFP Roadmap — April 2026 Snapshot</h2>
      <p>The following reflects what was shared at the April 2026 workshop delivery. Anaplan's IFP roadmap evolves frequently — verify current status on Anapedia and the Anaplan Community before sharing with customers.</p>

""" + note("Content Currency",
           "This page is frozen to the April 2026 workshop delivery. For the current IFP roadmap, check <strong>Anapedia</strong> (Anaplan's documentation hub) "
           "and the <strong>Anaplan Community Partner portal</strong>. Roadmap items mentioned at a partner workshop may be earlier than public announcements.") + """

      <h2>Upcoming IFP Capabilities</h2>
""" + step("1", "CapEx Planning Application",
           "\"Later this year we're coming out with an application for CapEx projects — if you have a customer engagement in the next 6 months, it will be bespoke for now.\" "
           "A purpose-built CapEx planning application is on the IFP roadmap. Until it is available, CapEx requirements are addressed as a custom extension or a separate Anaplan build.") + \
step("2", "ADO Evolution",
     "Anaplan Data Orchestrator is expected to see continued investment in IFP 2.0 — specifically around pre-built data pipelines for common ERP sources and improved error reporting in pipeline runs. "
     "Current ADO setup in IFP requires manual pipeline configuration in most customer environments.") + \
step("3", "Headcount Planning 2.0 Roadmap",
     "Headcount Planning 2.0 (released with IFP 2.0) is being iterated. Planned enhancements include additional planning method types and tighter integration with workforce planning scenarios. "
     "Watch the Anaplan Community for release notes.") + \
step("4", "App Framework Enhancements",
     "The App Framework configurator is expected to expand its configuration coverage — reducing the number of cases where customers need custom extensions for requirements that could be handled via configuration. "
     "Each IFP release has added new configuration questions.") + """

      <h2>How to Stay Current</h2>
""" + table(
    ["Resource", "What It Has", "How to Access"],
    [
        ["Anapedia", "Official Anaplan documentation — IFP configuration guides, release notes", "anapedia.anaplan.com"],
        ["Anaplan Community", "Partner portal, product news, roadmap announcements", "community.anaplan.com"],
        ["IFP Partner Enablement", "Workshop recordings, micro-lessons, delivery guides", "Ask your Anaplan partner contact for the SharePoint link"],
        ["Release Notes", "What changed in each IFP release — critical for upgrade impact assessment", "Anapedia → IFP section → Release Notes"],
    ]
)


write("13-whats-coming.html", page(
    title="What's Coming",
    filename="13-whats-coming.html",
    subtitle="IFP roadmap items and upcoming capabilities — frozen to April 2026 delivery",
    badges=["Reference"],
    tsd_tell=None,
    tsd_show=None,
    tsd_do=None,
    body=body_13,
))


if __name__ == "__main__":
    print("\n✅ build3.py complete — pages 11–13 written")

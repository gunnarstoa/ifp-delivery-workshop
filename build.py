#!/usr/bin/env python3
"""
IFP Delivery Partner Workshop — build.py
Core framework + pages 01-05
"""

import os

# ─── Configuration ─────────────────────────────────────────────────────────────

WORKSHOP_TITLE = "IFP Delivery Partner Workshop"
ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")

# ─── Navigation Definition ─────────────────────────────────────────────────────

NAV_ITEMS = [
    ("s", "Getting Started"),
    ("l", "Workshop Overview", "01-overview.html"),
    ("l", "Case Study", "02-case-study.html"),
    ("l", "IFP Overview", "03-ifp-overview.html"),
    ("l", "Anaplan Way for IFP", "04-anaplan-way.html"),
    ("s", "Day 1 — Configuration"),
    ("l", "App Framework Configurator", "05-configurator-walkthrough.html"),
    ("l", "Lab A: Configurator Exercise", "06-lab-configurator.html"),
    ("l", "Model Generation", "07-generation.html"),
    ("l", "Post-Generation Steps", "08-post-gen.html"),
    ("l", "Error Log Review", "09-error-logs.html"),
    ("s", "Day 2 — Extensions"),
    ("l", "Extensions Overview", "10-extensions-overview.html"),
    ("l", "Lab B: Direct Input + Adjustments", "11-lab-direct-input.html"),
    ("l", "Lab C: Headcount × Rate Method", "12-lab-headcount-method.html"),
    ("s", "Reference"),
    ("l", "What's Coming", "13-whats-coming.html"),
    ("l", "Q&A from Sessions", "14-qanda.html"),
    ("l", "Facilitator Guide", "15-facilitator.html"),
]

PAGE_ORDER = [item[2] for item in NAV_ITEMS if item[0] == "l"]


# ─── Core Functions ─────────────────────────────────────────────────────────────

def nav(active):
    lines = [
        '<nav class="sidebar">',
        '  <div class="sidebar-header">',
        f'    <div class="sidebar-title">{WORKSHOP_TITLE}</div>',
        '  </div>',
        '  <ul class="nav-list">',
    ]
    in_section = False
    for item in NAV_ITEMS:
        if item[0] == "s":
            if in_section:
                lines.append('    </ul>')
            lines.append(f'    <li class="nav-section-title">{item[1]}</li>')
            lines.append('    <ul class="nav-submenu">')
            in_section = True
        else:
            _, label, href = item
            cls = "nav-link active" if href == active else "nav-link"
            lines.append(f'      <li><a class="{cls}" href="./{href}">{label}</a></li>')
    if in_section:
        lines.append('    </ul>')
    lines += [
        '  </ul>',
        '  <div class="lang-switcher">',
        '    <span class="lang-switcher-label">🌐 Language</span>',
        '    <select id="lang-select" class="lang-select">',
        '      <option value="en">🇺🇸 English</option>',
        '      <option value="ja">🇯🇵 日本語</option>',
        '      <option value="es">🇪🇸 Español</option>',
        '      <option value="fr">🇫🇷 Français</option>',
        '      <option value="de">🇩🇪 Deutsch</option>',
        '      <option value="pt">🇧🇷 Português</option>',
        '      <option value="ko">🇰🇷 한국어</option>',
        '      <option value="zh">🇨🇳 中文</option>',
        '    </select>',
        '  </div>',
        '</nav>',
    ]
    return "\n".join(lines)


def prevnext(active):
    try:
        idx = PAGE_ORDER.index(active)
    except ValueError:
        return ""
    prev = f'<a class="prevnext-btn" href="./{PAGE_ORDER[idx-1]}">← Previous</a>' if idx > 0 else '<span></span>'
    nxt = f'<a class="prevnext-btn" href="./{PAGE_ORDER[idx+1]}">Next →</a>' if idx < len(PAGE_ORDER) - 1 else '<span></span>'
    return f'<div class="prevnext-nav">{prev}{nxt}</div>'


def page(title, filename, subtitle, badges, tsd_tell, tsd_show, tsd_do, body):
    badge_html = "".join(f'<span class="content-badge">{b}</span>' for b in badges)

    tsd_html = ""
    if tsd_tell:
        tsd_html = f"""
      <div class="tsd-banner">
        <div class="tsd-step tsd-step-tell">
          <span class="tsd-step-label">📖 Tell</span>
          <span class="tsd-step-heading">{tsd_tell[0]}</span>
          <span class="tsd-step-desc">{tsd_tell[1]}</span>
        </div>
        <div class="tsd-step tsd-step-show">
          <span class="tsd-step-label">👁 Show</span>
          <span class="tsd-step-heading">{tsd_show[0]}</span>
          <span class="tsd-step-desc">{tsd_show[1]}</span>
        </div>
        <div class="tsd-step tsd-step-do">
          <span class="tsd-step-label">✅ Do</span>
          <span class="tsd-step-heading">{tsd_do[0]}</span>
          <span class="tsd-step-desc">{tsd_do[1]}</span>
        </div>
      </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — {WORKSHOP_TITLE}</title>
  <link rel="stylesheet" href="../css/style.css">
</head>
<body>
  <div class="mobile-header">
    <button id="hamburger">☰</button>
    <span>{WORKSHOP_TITLE}</span>
  </div>

  {nav(filename)}

  <main class="main-content">
    <div class="content-header">
      <h1>{title}</h1>
      <p class="subtitle">{subtitle}</p>
      <div class="badge-row">{badge_html}</div>
    </div>
    <div class="content-body">
{tsd_html}
{body}
{prevnext(filename)}
    </div>
  </main>
  <script src="../js/nav.js"></script>
</body>
</html>"""
    return html


def write(filename, content):
    os.makedirs(DOCS, exist_ok=True)
    path = os.path.join(DOCS, filename)
    with open(path, 'w') as f:
        f.write(content)
    print(f"✅ {filename}")


# ─── Content Helpers ────────────────────────────────────────────────────────────

def note(label, body):
    return f'<div class="callout-note"><span class="callout-label">ℹ {label}</span><p>{body}</p></div>'

def warn(label, body):
    return f'<div class="callout-warning"><span class="callout-label">⚠ {label}</span><p>{body}</p></div>'

def tip(label, body):
    return f'<div class="callout-tip"><span class="callout-label">💡 {label}</span><p>{body}</p></div>'

def imp(label, body):
    return f'<div class="callout-important"><span class="callout-label">🚨 {label}</span><p>{body}</p></div>'

def callout_do(label, body):
    return f'<div class="callout-do"><span class="callout-label">✅ {label}</span><p>{body}</p></div>'

def table(headers, rows):
    ths = "".join(f"<th>{h}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'<div class="table-wrap"><table><thead><tr>{ths}</tr></thead><tbody>{trs}</tbody></table></div>'

def ss(label, desc=""):
    d = f'<div class="ss-desc">{desc}</div>' if desc else ""
    return f'<div class="screenshot-placeholder"><div class="ss-icon">📸</div><div class="ss-label">{label}</div>{d}</div>'

def ss_real(src, caption):
    return (f'<figure class="screenshot">'
            f'<img src="../img/{src}" alt="{caption}" style="width:100%;border-radius:6px;border:1px solid #e2e8f0;">'
            f'<figcaption style="font-size:0.8rem;color:#6b7280;margin-top:0.4rem;text-align:center;">{caption}</figcaption>'
            f'</figure>')

def step(num, heading, body):
    return (f'<div class="step">'
            f'<div class="step-badge">{num}</div>'
            f'<div class="step-content"><h3>{heading}</h3><p>{body}</p></div>'
            f'</div>')

def two_col(*cards):
    inner = "".join(f'<div class="card">{c}</div>' for c in cards)
    return f'<div class="two-col">{inner}</div>'

def mini_lab(number, title, duration, objective, steps_list, completion_content, extra_body=""):
    steps_html = ""
    for i, step_text in enumerate(steps_list, 1):
        steps_html += f'      <li><span class="mini-lab-step-num">{i}</span>{step_text}</li>\n'

    return f"""
<div class="mini-lab">
  <div class="mini-lab-header">
    <div class="mini-lab-number">{number}</div>
    <div class="mini-lab-title">{title}</div>
    <div class="mini-lab-duration">⏱ {duration}</div>
  </div>
  <div class="mini-lab-body">
    <div class="mini-lab-objective"><strong>Objective</strong> {objective}</div>
    <ol class="mini-lab-steps">
{steps_html}    </ol>
{extra_body}
  </div>
  <div class="mini-lab-completion">
    <div class="mini-lab-completion-label">✅ What it should look like when complete</div>
    {completion_content}
  </div>
</div>"""


# ─── Page 01: Workshop Overview ─────────────────────────────────────────────────

body_01 = """
      <h2>What This Workshop Is</h2>
      <p>This is a two-day hands-on IFP 2.0 delivery workshop for Anaplan partner practitioners. Day 1 covers the full App Framework configuration workflow — from configurator walk-through through model generation, post-generation steps, and error log review. Day 2 focuses on extensions, with two hands-on labs building real IFP planning method extensions from scratch.</p>
      <p>The workshop uses a training tenant with pre-staged IFP models. All configuration and extension work happens in these training models — not in production.</p>

      <h2>Who It's For</h2>
      <p>Anaplan delivery consultants at partner firms who are implementing IFP for customers or expect to in the next 12 months. This is a practitioner workshop — not a product overview session.</p>
      <p><strong>Prerequisites:</strong></p>
      <ul>
        <li>Active Anaplan workspace admin access (confirmed before Day 1)</li>
        <li>Model Builder (MB), Solution Architect (SA), or Master Anaplanner certification</li>
        <li>Prior experience building or configuring Anaplan models</li>
        <li>Familiarity with financial planning concepts (P&amp;L, balance sheet, headcount)</li>
      </ul>

      <h2>What You'll Be Able to Do</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>#</th><th>Verifiable Outcome</th></tr></thead>
          <tbody>
            <tr><td>1</td><td>Configure the IFP App Framework end-to-end and generate a functional IFP model</td></tr>
            <tr><td>2</td><td>Read, interpret, and resolve generation error logs without escalating basic formula errors</td></tr>
            <tr><td>3</td><td>Build two extensions from scratch: a multi-adjustment direct input method and a headcount-driven rate method</td></tr>
          </tbody>
        </table>
      </div>

      <h2>Workshop Structure</h2>
""" + table(
    ["Day", "Section", "Topic", "Format", "Time"],
    [
        ["Day 1", "Getting Started", "IFP Overview + Anaplan Way", "Tell/Show", "35 min"],
        ["Day 1", "Configuration", "App Framework Configurator Walkthrough", "Walkthrough", "45 min"],
        ["Day 1", "Lab A", "Configurator Exercise — FintechCo", "Hands-On", "60 min"],
        ["Day 1", "Configuration", "Model Generation", "Walkthrough + Do", "30 min"],
        ["Day 1", "Configuration", "Post-Generation Steps", "Walkthrough + Do", "20 min"],
        ["Day 1", "Configuration", "Error Log Review + Lab", "Hands-On", "60 min"],
        ["Day 2", "Extensions", "Extensions Overview + Best Practices", "Walkthrough", "30 min"],
        ["Day 2", "Lab B", "Direct Input + Adjustments", "Hands-On", "45 min"],
        ["Day 2", "Lab C", "Headcount × Rate Planning Method", "Hands-On", "60 min"],
        ["Day 2", "Reference", "Knowledge Check + Debrief", "Discussion", "60 min"],
    ]
) + """

      <h2>Tell · Show · Do Engagement</h2>
""" + table(
    ["Mode", "What Happens", "Your Role"],
    [
        ["📖 Tell", "Facilitator explains the concept and why it matters for IFP delivery", "Listen, take notes, ask clarifying questions"],
        ["👁 Show", "Facilitator demonstrates live in the training tenant", "Follow along in your own workspace"],
        ["✅ Do", "You complete the activity independently in the training model", "Work through steps, raise blockers, compare with neighbors"],
    ]
) + warn("Training Tenant Access",
         "This workshop uses training tenant credentials provided at session start. Do not use production models. "
         "Your facilitator will confirm access before Day 1 begins.")


write("01-overview.html", page(
    title="Workshop Overview",
    filename="01-overview.html",
    subtitle="Objectives, prerequisites, structure, and how to use this guide",
    badges=["Getting Started", "15 min"],
    tsd_tell=None,
    tsd_show=None,
    tsd_do=None,
    body=body_01,
))


# ─── Page 02: Case Study ─────────────────────────────────────────────────────────

body_02 = imp("🚧 Case Study Placeholder",
              "A fictional company profile will be defined here. All lab exercises currently reference <strong>FintechCo</strong> as a temporary placeholder name. "
              "Replace with the confirmed case study company before delivering this workshop.") + """

      <div class="callout-tip">
        <span class="callout-label">💡 Keep This Page Open</span>
        <p>During the lab exercises, refer back to this page when you need to recall FintechCo's structure, dimensions, or planning requirements. The facilitator may add context during the session that is not in this guide.</p>
      </div>

      <h2>Company Profile</h2>
""" + two_col(
    """<h3>FintechCo Overview</h3>
    <ul>
      <li><strong>Industry:</strong> Financial Services</li>
      <li><strong>Size:</strong> Mid-size (~1,200 employees)</li>
      <li><strong>Headquarters:</strong> London, UK</li>
      <li><strong>Planning Scope:</strong> P&amp;L Planning (IFP)</li>
      <li><strong>Implementation Type:</strong> Greenfield (new workspace)</li>
    </ul>""",
    """<h3>Organizational Structure</h3>
    <ul>
      <li><strong>Legal Entities:</strong> 3 (UK, EU, US)</li>
      <li><strong>Departments:</strong> 5 (Sales, Technology, Operations, Finance, HR)</li>
      <li><strong>Geography Levels:</strong> 2 (Region → Country)</li>
      <li><strong>Functional Areas:</strong> 4 (Gross Profit, OpEx, Headcount, Balance Sheet)</li>
    </ul>""",
) + two_col(
    """<h3>Planning Requirements</h3>
    <ul>
      <li><strong>Fiscal Year:</strong> January – December</li>
      <li><strong>Planning Period:</strong> Monthly</li>
      <li><strong>Currencies:</strong> GBP (functional), USD + EUR (transactional)</li>
      <li><strong>Planning Horizon:</strong> 24 months forward</li>
    </ul>""",
    """<h3>Key Configuration Decisions</h3>
    <ul>
      <li><strong>Entity Hierarchy:</strong> 3 levels (Group → Region → Entity)</li>
      <li><strong>OpEx Methods:</strong> Direct Input + Headcount × Rate</li>
      <li><strong>Balance Sheet:</strong> Included in scope</li>
      <li><strong>Revenue:</strong> Driver-based (Volume × Price)</li>
    </ul>""",
) + """

      <h2>Your Role</h2>
      <p>You are the lead IFP delivery consultant for FintechCo's Anaplan implementation. You have completed Session Zero with the client and gathered all configuration inputs. Today you are configuring the IFP App Framework and generating the model for the first time.</p>

      <h2>Business Challenge</h2>
""" + step("1", "Disconnected Planning", "FintechCo currently runs financial planning in Excel across 3 legal entities. Consolidation takes 3 days each month. The CFO has mandated a single connected planning solution within 6 months.") + \
step("2", "Headcount Complexity", "The HR team tracks headcount in a separate system. FintechCo wants to see headcount data drive expense calculations directly in the financial plan — specifically for Training and Benefits accounts.") + \
step("3", "Multi-Adjustment Flexibility", "FintechCo's budget holders need to enter a base amount plus two adjustment layers (management override + regional adjustment) for certain OpEx accounts. Excel allows this; the new tool must too.") + """

      <h2>Dataset Files</h2>
""" + table(
    ["File", "Description", "Key Fields"],
    [
        ["FintechCo_Entities.csv", "Legal entity hierarchy (3 levels)", "Entity Code, Name, Region, Currency"],
        ["FintechCo_Departments.csv", "Department list", "Dept Code, Name, Functional Area"],
        ["FintechCo_Accounts.csv", "Chart of accounts (~400 accounts)", "Account Code, Name, Type, Planning Method"],
        ["FintechCo_Actuals.csv", "12 months actuals data", "Entity, Dept, Account, Period, Amount"],
        ["FintechCo_Headcount.csv", "Headcount by Dept + Period", "Entity, Dept, Period, HC Amount"],
    ]
) + callout_do("Your Role",
               "During the lab exercises, all configuration decisions should be based on the FintechCo profile above. "
               "When you encounter a configuration question where FintechCo's answer is unclear, "
               "make a reasonable assumption and document it — just like you would with a real client.")


write("02-case-study.html", page(
    title="Case Study",
    filename="02-case-study.html",
    subtitle="FintechCo — the fictional company powering all lab exercises",
    badges=["Getting Started", "10 min"],
    tsd_tell=None,
    tsd_show=None,
    tsd_do=None,
    body=body_02,
))


# ─── Page 03: IFP Overview ───────────────────────────────────────────────────────

body_03 = """
      <h2>What IFP Is</h2>
      <p>Integrated Financial Planning (IFP) is Anaplan's pre-built application for P&amp;L, balance sheet, and headcount planning. It provides a structured, configurator-driven approach to financial planning that eliminates months of model-building time and gives partner consultants a repeatable delivery framework.</p>
      <p>Version 2.0 is a significant re-architecture from prior versions. The headline change is the introduction of the <strong>Application Framework</strong> — a configurator-driven model generation system that replaces manual model setup. IFP 2.0 also introduced Anaplan Data Orchestrator (ADO) integration and Headcount Planning 2.0.</p>

      <h2>What's New in IFP 2.0</h2>
""" + table(
    ["Capability", "What It Is", "Why It Matters"],
    [
        ["App Framework", "Configurator-driven generation — answer questions, generate a model", "Eliminates weeks of manual module setup; standardizes delivery"],
        ["ADO Integration", "Anaplan Data Orchestrator built-in for data loading", "Replaces manual import actions with orchestrated data pipelines"],
        ["Headcount Planning 2.0", "Rebuilt HC module with IFP integration", "HC data flows directly into expense planning without manual mapping"],
        ["Extensive Re-Architecting", "Module naming, list structures, formula patterns all standardized", "Easier to maintain, extend, and hand off between consultants"],
    ]
) + """

      <h2>Module Architecture</h2>
      <p>IFP 2.0 generates a consistent module naming convention across all four models. Understanding this architecture is essential for error log troubleshooting and extension work.</p>
""" + table(
    ["Prefix", "Module Type", "Purpose"],
    [
        ["ADMIN", "Administration", "Configuration settings, planning method mapping, user access"],
        ["SYS", "System", "Cross-model system lists, hierarchy mappings, Boolean controls"],
        ["DAT", "Data", "Actuals data staging, integrations from ADO and Headcount model"],
        ["INP", "Input", "Planning input modules — where users enter forecast data"],
        ["CALC", "Calculation", "Aggregation, allocation, derived calculations from INP modules"],
        ["OUT", "Output", "Consolidated output modules — feed downstream reports and dashboards"],
    ]
) + """

      <h2>The App Framework Concept</h2>
      <p>The App Framework is the configuration and generation engine. The workflow is:</p>
""" + step("1", "Configure", "Answer all configuration questions in the App Framework configurator. These define hierarchy levels, dimensions, planning methods, and scope.") + \
step("2", "Generate", "Trigger generation. The App Framework reads your answers and provisions all four IFP models (Financial Planning, Headcount, Admin, Data Orchestrator). This takes 10–20 minutes.") + \
step("3", "Review", "Inspect the generated model and error logs. 'Generated with errors' is normal and expected — it does not mean the model is broken.") + \
step("4", "Extend", "Add customer-specific extensions on top of the generated base model. Document everything you change.") + \
imp("'Generated with Errors' is Normal",
    "Every IFP 2.0 generation in a training or early-stage environment produces errors. "
    "These are formula errors caused by configuration choices, hierarchy renaming, or geography differences from the base model template. "
    "The model is functional. You will learn to read and resolve these errors in the Error Log Review section.") + """

      <h2>App Framework Overview</h2>
""" + ss_real("overview/app-framework-04-30-00.jpg",
              "IFP Application Framework overview — 43 configurations, 4 models, 17 assets, generated with errors status")


write("03-ifp-overview.html", page(
    title="IFP Overview",
    filename="03-ifp-overview.html",
    subtitle="What IFP 2.0 is, what changed, and how the App Framework works",
    badges=["Getting Started", "20 min"],
    tsd_tell=("What IFP 2.0 Is", "What IFP 2.0 is, how it differs from prior versions, and why the App Framework changes how partners deliver."),
    tsd_show=("App Framework Demo", "Facilitator shows the App Framework overview page — configurations count, models, assets, generation status."),
    tsd_do=("No Hands-On Yet", "No hands-on activity on this page — configuration begins on the next section."),
    body=body_03,
))


# ─── Page 04: Anaplan Way for IFP ───────────────────────────────────────────────

body_04 = """
      <h2>The Six-Phase IFP Delivery Methodology</h2>
      <p>IFP delivery follows Anaplan's standard App delivery phases, adapted for the configurator-generation workflow. Understanding the phases helps you set correct expectations with customers and know which activities belong where.</p>
""" + step("1", "Pre-Project", """The engagement prep phase. Deliverables include:
        <ul>
          <li>Session Zero — configuration discovery with the customer</li>
          <li>Configuration worksheet completed (all 43 questions answered)</li>
          <li>Hierarchy decisions locked: entity levels, geography structure, functional areas</li>
          <li>Data availability confirmed: actuals source, headcount feed, currency setup</li>
          <li>Workspace provisioned, workspace admin access confirmed for the delivery team</li>
        </ul>""") + \
step("2", "Config", """The configurator phase. The delivery consultant:
        <ul>
          <li>Enters all configuration answers in the App Framework configurator</li>
          <li>Reviews top-level questions and financial planning configurations</li>
          <li>Triggers model generation</li>
          <li>Reviews error logs and resolves formula errors</li>
        </ul>""") + \
step("3", "Test &amp; Deploy", """Validation phase after a clean generation:
        <ul>
          <li>Load sample actuals data via ADO pipelines</li>
          <li>Spot-check calculated line items in CALC modules</li>
          <li>Validate planning methods in UX pages</li>
          <li>UAT with key users from the customer team</li>
        </ul>""") + \
step("4", "Extension Foundation", """Design and scope customer-specific extensions:
        <ul>
          <li>Identify gaps between IFP base model and customer requirements</li>
          <li>Classify each gap: Configure vs. Extend vs. Modify</li>
          <li>Size each extension (S/M/L/XL)</li>
          <li>Create extension tags in the model (Extension + Formula Override)</li>
        </ul>""") + \
step("5", "Iterative Extension", """Build extensions in priority order:
        <ul>
          <li>Each extension: design → build → test → document</li>
          <li>Tag every line item you add or modify</li>
          <li>Document in external design spec (not just in-model notes)</li>
          <li>Regression test base model functionality after each extension</li>
        </ul>""") + \
step("6", "Extension Test &amp; Deploy", """Final validation and handover:
        <ul>
          <li>Full UAT with all extensions in place</li>
          <li>Performance test with production data volumes</li>
          <li>Handover documentation: extension log, formula override map, upgrade checklist</li>
          <li>Training for customer admins</li>
        </ul>""") + \
note("IFP-Specific Phase Notes",
     "Session Zero is critical. Unlike custom model builds, IFP configuration decisions made at Session Zero are difficult or impossible to change after generation. "
     "Hierarchy levels, geography structure, and entity configuration must be locked before anyone touches the configurator. "
     "A missed dimension at Session Zero = a complete regeneration during Test &amp; Deploy.") + """

      <h2>Two Customer Types</h2>
""" + two_col(
    """<h3>🌱 Greenfield</h3>
    <ul>
      <li>New workspace, no existing Anaplan models</li>
      <li>IFP is the first application</li>
      <li>No integration complexity with existing models</li>
      <li>Full ADO setup from scratch</li>
      <li><strong>Risk:</strong> Session Zero discovery is the only constraint — get it right</li>
    </ul>""",
    """<h3>🔗 Existing Workspace</h3>
    <ul>
      <li>IFP deployed alongside existing live models</li>
      <li>Workspace admin must manage list conflicts</li>
      <li>ADO may need to coexist with existing import actions</li>
      <li>List naming must not collide with existing lists</li>
      <li><strong>Risk:</strong> Generation may affect existing workspace settings</li>
    </ul>""",
) + """

      <h2>Map FintechCo to the Right Phase</h2>
""" + callout_do("Phase Mapping Exercise",
                 "Based on the FintechCo case study: which phase are we in today? What should have been completed before this session? "
                 "What's the next phase after we complete the lab configuration? Discuss with your neighbor.")


write("04-anaplan-way.html", page(
    title="Anaplan Way for IFP",
    filename="04-anaplan-way.html",
    subtitle="The six-phase delivery methodology and what happens in each phase",
    badges=["Getting Started", "15 min"],
    tsd_tell=("The 6-Phase Delivery Methodology", "The six phases of IFP delivery and what belongs in each phase."),
    tsd_show=("Phase Walkthrough", "Facilitator walks through each phase with examples from real IFP engagements."),
    tsd_do=("Phase Mapping", "Map FintechCo's engagement to the correct delivery phase."),
    body=body_04,
))


# ─── Page 05: Configurator Walkthrough ──────────────────────────────────────────

body_05 = """
      <h2>What the Configurator Is</h2>
      <p>The App Framework configurator is the single interface for all IFP configuration decisions. It presents 43 configuration questions across three categories: top-level questions (22), financial planning configurations (17), and headcount configurations (3), plus additional settings. The answers to these questions determine what gets generated — module structure, list hierarchies, formula logic, and planning method availability.</p>

      <div class="callout-warning">
        <span class="callout-label">⚠ Configuration Is Final at Generation</span>
        <p>Once you trigger generation, many structural decisions cannot be changed without regenerating the model. Hierarchy levels, entity structure, and geography configuration must be locked before generation. Get these right at Session Zero — they are the hardest things to change later.</p>
      </div>

      <h2>Configuration Sections</h2>

      <h3>Hierarchies</h3>
      <p>The Hierarchies section defines the dimension structure of the generated model. Decisions made here cascade through every module and cannot be changed post-generation without a full regeneration.</p>
      <ul>
        <li><strong>Geography:</strong> How many levels? (e.g., Global → Region → Country → City). Which levels are planning levels vs. roll-up only?</li>
        <li><strong>Functional Area:</strong> Which functional areas are in scope? (Gross Profit, OpEx, Headcount, Balance Sheet). Each enabled area generates additional modules.</li>
        <li><strong>Entity:</strong> How many entity levels? What is the top-level consolidation entity?</li>
        <li><strong>Product:</strong> Is product-level planning required? Product hierarchy levels?</li>
      </ul>
""" + ss("App Framework Configurator — Overview panel showing Hierarchies, Data Structure, Configurations",
         "Navigate to the App Framework and open the configurator to follow along") + """

      <h2>Top-Level Questions (22 Questions)</h2>
      <p>The top-level questions are the most impactful. They define the structural skeleton of the IFP model.</p>
""" + table(
    ["Question Area", "What It Controls", "FintechCo Answer"],
    [
        ["Entity Levels", "How many entity hierarchy levels in the model", "3 (Group → Region → Entity)"],
        ["Department/Functional Area", "Functional area structure and planning scope", "4 areas enabled"],
        ["Geography", "Geography levels included in planning dimensions", "2 levels (Region → Country)"],
        ["Base Currency", "Functional currency for the workspace", "GBP"],
        ["Transactional Currencies", "Additional currencies for entity-level planning", "USD, EUR"],
        ["Planning Period", "Monthly, quarterly, or weekly planning granularity", "Monthly"],
        ["Fiscal Year Start", "First month of the fiscal year", "January"],
        ["Planning Horizon", "How many months of planning periods to generate", "24 months"],
        ["Balance Sheet", "Is balance sheet planning in scope?", "Yes"],
        ["Revenue Planning", "Driver-based or direct input revenue planning?", "Driver-based"],
    ]
) + ss("Configurations page — Top-level questions 1-10", "The first 10 top-level configuration questions") + """

      <h2>Financial Planning Configurations (17 Questions)</h2>
      <p>Financial planning configurations control the planning methods available, headcount settings, and OpEx behavior. These are less structural than top-level questions but still affect formula generation.</p>
""" + table(
    ["Configuration Area", "Key Decisions"],
    [
        ["OpEx Planning Methods", "Which methods are available: Direct Input, Units × Rate, Rolling Moving Average, Custom methods"],
        ["Headcount Planning", "Headcount dimensions, planning method defaults, integration with HC model"],
        ["Balance Sheet Configuration", "Which balance sheet accounts are in scope, roll-up hierarchy"],
        ["Revenue Configuration", "Driver selection, product hierarchy levels, volume × price method"],
        ["Actuals Integration", "How actuals data loads into DAT modules — ADO pipeline configuration"],
    ]
) + ss("Configurations page — Financial Planning configurations",
       "Financial planning configurations section — OpEx, Headcount, Balance Sheet settings") + """

      <h2>Before the Lab</h2>
""" + note("Preparation",
           "During Lab A, you will configure the App Framework for FintechCo. "
           "Review the FintechCo case study profile now and note any configuration decisions that feel ambiguous. "
           "The facilitator will answer questions before you begin configuring.")


write("05-configurator-walkthrough.html", page(
    title="App Framework Configurator",
    filename="05-configurator-walkthrough.html",
    subtitle="What the configurator controls and how to navigate all 43 configuration questions",
    badges=["Day 1", "45 min", "Walkthrough"],
    tsd_tell=("What the Configurator Controls", "What the configurator is and what each section controls."),
    tsd_show=("Live Configurator Demo", "Facilitator walks through all configuration sections live in the training tenant."),
    tsd_do=("Follow Along", "Participants follow along in their own workspace and note decisions for the upcoming lab."),
    body=body_05,
))


if __name__ == "__main__":
    print("\n✅ build.py complete — pages 01–05 written")

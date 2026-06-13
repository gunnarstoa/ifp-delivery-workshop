"""IFP Delivery Workshop — auth gateway and static-page server.

Serves the existing docs/, css/, data/ trees behind username/password auth.
Logs every authenticated request to page_views for later analysis.
Facilitator-only pages additionally require users.is_facilitator = 1.
"""
import calendar as calmod
import json
import os
import re
import secrets
import sqlite3
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import bcrypt
from flask import (
    Flask,
    abort,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.environ.get("WORKSHOP_DB", REPO_ROOT / "workshop.db"))
SECRET_KEY = os.environ.get("WORKSHOP_SECRET_KEY") or secrets.token_hex(32)

# Paths that require an additional is_facilitator check.
FACILITATOR_PATH_RE = re.compile(
    r"^/(docs/(15-facilitator|16-facilitator-toolkit|cohort-tracker)|data/|admin|w/[a-z0-9-]+/15-facilitator|w/[a-z0-9-]+/16-facilitator-toolkit|w/[a-z0-9-]+/cohort-tracker)"
)
# Paths that bypass auth entirely (login form, static assets, health).
PUBLIC_PREFIXES = ("/login", "/static/", "/css/", "/js/", "/img/", "/assets/", "/favicon", "/healthz", "/robots.txt")

app = Flask(__name__, static_folder=None)
app.config.update(
    SECRET_KEY=SECRET_KEY,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("WORKSHOP_PRODUCTION") == "1",
    PERMANENT_SESSION_LIFETIME=60 * 60 * 8,  # 8 hours
)


# ---------------------------- DB helpers ----------------------------

def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(str(DB_PATH))
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
        g.db.execute("PRAGMA journal_mode = WAL")
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create tables if missing. Called at startup and from `flask init-db`."""
    conn = sqlite3.connect(str(DB_PATH))
    try:
        with open(REPO_ROOT / "backend" / "schema.sql") as f:
            conn.executescript(f.read())
        conn.commit()
    finally:
        conn.close()


# ---------------------------- Auth helpers ----------------------------

def current_user():
    uid = session.get("uid")
    if uid is None:
        return None
    if "user" in g:
        return g.user
    row = get_db().execute(
        "SELECT id, username, display_name, email, is_facilitator, is_active FROM users WHERE id = ?",
        (uid,),
    ).fetchone()
    if row is None or not row["is_active"]:
        session.clear()
        return None
    g.user = row
    return row


def is_facilitator_path(path: str) -> bool:
    return bool(FACILITATOR_PATH_RE.match(path))


def is_public_path(path: str) -> bool:
    return any(path.startswith(p) for p in PUBLIC_PREFIXES)


def login_required(path: str):
    """Raise abort(401)/abort(403) if request lacks the right auth for `path`."""
    if is_public_path(path):
        return None
    user = current_user()
    if user is None:
        return redirect(url_for("login", next=path))
    if is_facilitator_path(path) and not user["is_facilitator"]:
        abort(403)
    return None


@app.before_request
def auth_gate():
    path = request.path
    redirect_or_none = login_required(path)
    if redirect_or_none is not None:
        return redirect_or_none


@app.after_request
def log_page_view(resp):
    # Only log authenticated GETs of HTML/JSON content we actually served.
    if request.method != "GET":
        return resp
    if is_public_path(request.path):
        return resp
    user = g.get("user")
    if user is None:
        return resp
    if resp.status_code >= 400 and resp.status_code != 304:
        # Still log denied access so facilitator can review
        pass
    try:
        get_db().execute(
            "INSERT INTO page_views (user_id, path, query, status, referer, user_agent) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                user["id"],
                request.path,
                request.query_string.decode("utf-8", errors="replace") or None,
                resp.status_code,
                request.referrer,
                request.user_agent.string[:500] if request.user_agent else None,
            ),
        )
        get_db().commit()
    except sqlite3.Error:
        pass
    return resp


# ---------------------------- Routes: login ----------------------------

@app.route("/")
def home():
    user = current_user()
    if user is None:
        return redirect(url_for("login"))
    if user["is_facilitator"]:
        return redirect(url_for("admin_dashboard"))
    # Send participant to the workshop of their most recent enrollment.
    row = get_db().execute(
        "SELECT w.slug FROM session_participants sp "
        "JOIN sessions s ON s.id = sp.session_id "
        "JOIN workshops w ON w.id = s.workshop_id "
        "WHERE sp.user_id = ? AND sp.removed_at IS NULL AND s.status != 'archived' "
        "ORDER BY sp.enrolled_at DESC LIMIT 1",
        (user["id"],),
    ).fetchone()
    slug = row["slug"] if row else "ifp"
    return redirect(f"/w/{slug}/01-overview.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        ok = False
        row = get_db().execute(
            "SELECT id, username, password_hash, is_active FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        if row and row["is_active"]:
            try:
                ok = bcrypt.checkpw(password.encode("utf-8"), row["password_hash"].encode("utf-8"))
            except ValueError:
                ok = False
        get_db().execute(
            "INSERT INTO login_events (username_attempted, succeeded, ip, user_agent) VALUES (?, ?, ?, ?)",
            (username, 1 if ok else 0, request.headers.get("X-Forwarded-For", request.remote_addr), request.user_agent.string[:500] if request.user_agent else None),
        )
        get_db().commit()
        if ok:
            session.clear()
            session["uid"] = row["id"]
            session.permanent = True
            get_db().execute("UPDATE users SET last_login_at = CURRENT_TIMESTAMP WHERE id = ?", (row["id"],))
            get_db().commit()
            nxt = request.args.get("next") or request.form.get("next") or "/"
            if not nxt.startswith("/") or nxt.startswith("//"):
                nxt = "/"
            return redirect(nxt)
        time.sleep(0.5)  # rate-limit failed attempts modestly
        return render_template("login.html", error="Invalid username or password.", next=request.args.get("next") or "")
    return render_template("login.html", error=None, next=request.args.get("next") or "")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------------------- Routes: static page serving ----------------------------

def _serve_repo_file(subdir: str, filename: str):
    base = (REPO_ROOT / subdir).resolve()
    target = (base / filename).resolve()
    if not str(target).startswith(str(base)):
        abort(404)
    if not target.is_file():
        abort(404)
    return send_from_directory(str(base), filename)


@app.route("/docs/<path:filename>")
def serve_docs(filename):
    # Backward-compat: if a file has been moved to docs/ifp/, 301 to the new path.
    ifp_path = (REPO_ROOT / "docs" / "ifp" / filename).resolve()
    if ifp_path.is_file() and str(ifp_path).startswith(str((REPO_ROOT / "docs" / "ifp").resolve())):
        return redirect(f"/w/ifp/{filename}", code=301)
    return _serve_repo_file("docs", filename)


@app.route("/w/<workshop_slug>/<path:filename>")
def serve_workshop(workshop_slug, filename):
    # Defense-in-depth: workshop_slug must match SLUG_RE shape; route param itself doesn't enforce it.
    if not re.fullmatch(r"[a-z0-9-]{1,40}", workshop_slug):
        abort(404)
    return _serve_repo_file(f"docs/{workshop_slug}", filename)


@app.route("/data/<path:filename>")
def serve_data(filename):
    return _serve_repo_file("data", filename)


@app.route("/css/<path:filename>")
def serve_css(filename):
    return _serve_repo_file("css", filename)


@app.route("/js/<path:filename>")
def serve_js(filename):
    return _serve_repo_file("js", filename)


@app.route("/img/<path:filename>")
def serve_img(filename):
    return _serve_repo_file("img", filename)


@app.route("/assets/<path:filename>")
def serve_assets(filename):
    return _serve_repo_file("assets", filename)


@app.route("/favicon.ico")
def favicon():
    fav = REPO_ROOT / "favicon.ico"
    if fav.is_file():
        return send_from_directory(str(REPO_ROOT), "favicon.ico")
    abort(404)


@app.route("/healthz")
def healthz():
    return "ok", 200


# ---------------------------- Routes: admin ----------------------------

def _require_facilitator():
    user = current_user()
    if user is None:
        return None, redirect(url_for("login", next=request.path))
    if not user["is_facilitator"]:
        abort(403)
    return user, None


CAL_COLORS = ["blue", "green", "purple", "orange", "teal", "pink", "amber", "indigo"]


def _parse_month_param(raw):
    """Parse a ?month=YYYY-MM query param; fall back to current month."""
    if raw:
        m = re.fullmatch(r"(\d{4})-(\d{2})", raw)
        if m:
            y, mo = int(m.group(1)), int(m.group(2))
            if 1 <= mo <= 12 and 2000 <= y <= 2100:
                return y, mo
    today = date.today()
    return today.year, today.month


def _month_grid(year, month, sessions_with_workshops):
    """Build a list of weeks; each week is a list of day dicts. Week starts Sunday."""
    today = date.today()
    cal = calmod.Calendar(firstweekday=calmod.SUNDAY)
    weeks = []
    for week in cal.monthdatescalendar(year, month):
        wrow = []
        for d in week:
            day_sessions = []
            for s in sessions_with_workshops:
                if s["_start"] <= d <= s["_end"]:
                    day_sessions.append({
                        "slug": s["slug"],
                        "name": s["name"],
                        "workshop_slug": s["workshop_slug"],
                        "workshop_name": s["workshop_name"],
                        "color": CAL_COLORS[(s["workshop_id"] - 1) % len(CAL_COLORS)],
                        "is_start": d == s["_start"],
                        "is_end": d == s["_end"],
                    })
            wrow.append({
                "date": d,
                "in_month": d.month == month,
                "is_today": d == today,
                "sessions": day_sessions,
            })
        weeks.append(wrow)
    prev_month = date(year, month, 1) - timedelta(days=1)
    next_month = (date(year, month, 28) + timedelta(days=10)).replace(day=1)
    return {
        "weeks": weeks,
        "year": year,
        "month": month,
        "month_name": calmod.month_name[month],
        "prev_param": f"{prev_month.year:04d}-{prev_month.month:02d}",
        "next_param": f"{next_month.year:04d}-{next_month.month:02d}",
        "today_param": f"{today.year:04d}-{today.month:02d}",
    }


def _sessions_overlapping_month(year, month):
    """All non-archived sessions that touch the given month, joined to workshop info."""
    first = date(year, month, 1)
    last_day = calmod.monthrange(year, month)[1]
    last = date(year, month, last_day)
    rows = get_db().execute(
        "SELECT s.id, s.slug, s.name, s.start_date, s.end_date, s.status, "
        "       w.id AS workshop_id, w.slug AS workshop_slug, w.name AS workshop_name "
        "FROM sessions s JOIN workshops w ON w.id = s.workshop_id "
        "WHERE s.status != 'archived' AND w.status != 'archived' "
        "  AND s.end_date >= ? AND s.start_date <= ? "
        "ORDER BY s.start_date ASC",
        (first.isoformat(), last.isoformat()),
    ).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        d["_start"] = date.fromisoformat(d["start_date"])
        d["_end"] = date.fromisoformat(d["end_date"])
        out.append(d)
    return out


@app.route("/admin")
def admin_dashboard():
    user, redir = _require_facilitator()
    if redir:
        return redir
    workshops = get_db().execute(
        "SELECT w.id, w.slug, w.name, w.short_description, w.contact_email, w.status, w.created_at, "
        "       u.username AS created_by_username, "
        "       (SELECT COUNT(*) FROM sessions s WHERE s.workshop_id = w.id AND s.status != 'archived') AS session_count "
        "FROM workshops w LEFT JOIN users u ON u.id = w.created_by "
        "WHERE w.status != 'archived' "
        "ORDER BY w.created_at DESC"
    ).fetchall()
    # Color per workshop for the legend; matches CAL_COLORS cycle
    workshops_for_legend = [
        {"slug": w["slug"], "name": w["name"], "color": CAL_COLORS[(w["id"] - 1) % len(CAL_COLORS)]}
        for w in workshops
    ]
    year, month = _parse_month_param(request.args.get("month"))
    sessions = _sessions_overlapping_month(year, month)
    grid = _month_grid(year, month, sessions)
    return render_template(
        "admin_dashboard.html",
        user=user,
        workshops=workshops,
        legend=workshops_for_legend,
        grid=grid,
    )


SLUG_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{1,38}[a-z0-9])?$")


@app.route("/admin/workshops/new", methods=["GET", "POST"])
def admin_workshop_new():
    user, redir = _require_facilitator()
    if redir:
        return redir
    errors = {}
    form = {"slug": "", "name": "", "short_description": "", "contact_email": ""}
    if request.method == "POST":
        form["slug"] = (request.form.get("slug") or "").strip().lower()
        form["name"] = (request.form.get("name") or "").strip()
        form["short_description"] = (request.form.get("short_description") or "").strip()
        form["contact_email"] = (request.form.get("contact_email") or "").strip()
        if not SLUG_RE.fullmatch(form["slug"]):
            errors["slug"] = "3-40 chars, lowercase letters/digits/hyphen, no leading/trailing hyphen"
        if not form["name"]:
            errors["name"] = "required"
        if not errors:
            try:
                cur = get_db().execute(
                    "INSERT INTO workshops (slug, name, short_description, contact_email, created_by) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (form["slug"], form["name"], form["short_description"] or None, form["contact_email"] or None, user["id"]),
                )
                get_db().commit()
                return redirect(url_for("admin_workshop_detail", slug=form["slug"]))
            except sqlite3.IntegrityError:
                errors["slug"] = f"workshop '{form['slug']}' already exists"
    return render_template("admin_workshop_new.html", user=user, form=form, errors=errors)


TOOLKIT_ROOT = REPO_ROOT / "toolkit"


def _parse_toolkit_file(path: Path):
    """Parse a toolkit markdown file: first '# Title' line, optional '> description',
    rest is the copyable body. Returns dict or None if file is missing/empty."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None
    lines = text.splitlines()
    title = path.stem
    description = ""
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].startswith("# "):
        title = lines[i][2:].strip()
        i += 1
    if i < len(lines) and lines[i].startswith("> "):
        description = lines[i][2:].strip()
        i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    body = "\n".join(lines[i:]).rstrip()
    return {
        "filename": path.name,
        "slug": path.stem,
        "title": title,
        "description": description,
        "body": body,
        "size_kb": round(path.stat().st_size / 1024, 1),
        "modified": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    }


def _list_toolkit_assets(workshop_slug: str):
    base = (TOOLKIT_ROOT / workshop_slug).resolve()
    if not base.is_dir() or not str(base).startswith(str(TOOLKIT_ROOT.resolve())):
        return None
    assets = []
    for p in sorted(base.glob("*.md")):
        a = _parse_toolkit_file(p)
        if a:
            assets.append(a)
    return assets


def _load_toolkit_asset(workshop_slug: str, asset_slug: str):
    base = (TOOLKIT_ROOT / workshop_slug).resolve()
    if not base.is_dir() or not str(base).startswith(str(TOOLKIT_ROOT.resolve())):
        return None
    if not re.fullmatch(r"[a-z0-9._-]{1,80}", asset_slug):
        return None
    path = (base / f"{asset_slug}.md").resolve()
    if not path.is_file() or not str(path).startswith(str(base)):
        return None
    return _parse_toolkit_file(path)


def _list_workshop_pages(workshop_slug):
    """Scan docs/<workshop_slug>/ for .html pages. Returns sorted list with mtimes."""
    base = (REPO_ROOT / "docs" / workshop_slug).resolve()
    if not base.is_dir():
        return None
    pages = []
    for p in sorted(base.glob("*.html")):
        st = p.stat()
        pages.append({
            "filename": p.name,
            "size_kb": round(st.st_size / 1024, 1),
            "modified": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "url": f"/w/{workshop_slug}/{p.name}",
        })
    return pages


@app.route("/admin/workshops/<slug>")
def admin_workshop_detail(slug):
    user, redir = _require_facilitator()
    if redir:
        return redir
    workshop = get_db().execute(
        "SELECT w.*, u.username AS created_by_username "
        "FROM workshops w LEFT JOIN users u ON u.id = w.created_by "
        "WHERE w.slug = ?",
        (slug,),
    ).fetchone()
    if workshop is None:
        abort(404)
    sessions = get_db().execute(
        "SELECT s.slug, s.name, s.start_date, s.end_date, s.status, s.created_at "
        "FROM sessions s WHERE s.workshop_id = ? AND s.status != 'archived' "
        "ORDER BY s.start_date DESC",
        (workshop["id"],),
    ).fetchall()
    pages = _list_workshop_pages(slug)
    content_root = f"docs/{slug}/"
    toolkit_assets = _list_toolkit_assets(slug)
    toolkit_root = f"toolkit/{slug}/"
    return render_template(
        "admin_workshop_detail.html",
        user=user,
        workshop=workshop,
        sessions=sessions,
        pages=pages,
        content_root=content_root,
        toolkit_assets=toolkit_assets,
        toolkit_root=toolkit_root,
    )


@app.route("/admin/workshops/<slug>/toolkit")
def admin_workshop_toolkit(slug):
    user, redir = _require_facilitator()
    if redir:
        return redir
    workshop = get_db().execute("SELECT * FROM workshops WHERE slug = ?", (slug,)).fetchone()
    if workshop is None:
        abort(404)
    assets = _list_toolkit_assets(slug)
    return render_template(
        "admin_workshop_toolkit.html",
        user=user, workshop=workshop, assets=assets,
        toolkit_root=f"toolkit/{slug}/",
    )


@app.route("/admin/workshops/<slug>/toolkit/<asset_slug>")
def admin_workshop_toolkit_asset(slug, asset_slug):
    user, redir = _require_facilitator()
    if redir:
        return redir
    workshop = get_db().execute("SELECT * FROM workshops WHERE slug = ?", (slug,)).fetchone()
    if workshop is None:
        abort(404)
    asset = _load_toolkit_asset(slug, asset_slug)
    if asset is None:
        abort(404)
    return render_template(
        "admin_workshop_toolkit_asset.html",
        user=user, workshop=workshop, asset=asset,
    )


@app.route("/admin/workshops/<slug>/sessions/new", methods=["GET", "POST"])
def admin_session_new(slug):
    user, redir = _require_facilitator()
    if redir:
        return redir
    workshop = get_db().execute("SELECT * FROM workshops WHERE slug = ?", (slug,)).fetchone()
    if workshop is None:
        abort(404)
    errors = {}
    today = date.today()
    default_end = (today + timedelta(days=4)).isoformat()
    form = {
        "slug": request.form.get("slug", "").strip().lower() if request.method == "POST" else today.isoformat(),
        "name": request.form.get("name", "").strip() if request.method == "POST" else f"{today.strftime('%B %-d, %Y')} Session",
        "start_date": request.form.get("start_date", today.isoformat()) if request.method == "POST" else today.isoformat(),
        "end_date": request.form.get("end_date", default_end) if request.method == "POST" else default_end,
        "notes": request.form.get("notes", "").strip() if request.method == "POST" else "",
    }
    if request.method == "POST":
        if not SLUG_RE.fullmatch(form["slug"]):
            errors["slug"] = "3-40 chars, lowercase letters/digits/hyphen, no leading/trailing hyphen"
        if not form["name"]:
            errors["name"] = "required"
        try:
            sd = date.fromisoformat(form["start_date"])
            ed = date.fromisoformat(form["end_date"])
            if ed < sd:
                errors["end_date"] = "end date must be on or after start date"
        except ValueError:
            errors["start_date"] = "invalid date"
        if not errors:
            try:
                get_db().execute(
                    "INSERT INTO sessions (workshop_id, slug, name, start_date, end_date, notes, created_by) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (workshop["id"], form["slug"], form["name"], form["start_date"], form["end_date"], form["notes"] or None, user["id"]),
                )
                get_db().commit()
                return redirect(url_for("admin_session_detail", slug=slug, session_slug=form["slug"]))
            except sqlite3.IntegrityError:
                errors["slug"] = f"a session with slug '{form['slug']}' already exists in this workshop"
    return render_template("admin_session_new.html", user=user, workshop=workshop, form=form, errors=errors)


@app.route("/admin/workshops/<slug>/sessions/<session_slug>")
def admin_session_detail(slug, session_slug):
    user, redir = _require_facilitator()
    if redir:
        return redir
    row = get_db().execute(
        "SELECT s.*, w.slug AS workshop_slug, w.name AS workshop_name, u.username AS created_by_username "
        "FROM sessions s JOIN workshops w ON w.id = s.workshop_id "
        "LEFT JOIN users u ON u.id = s.created_by "
        "WHERE w.slug = ? AND s.slug = ?",
        (slug, session_slug),
    ).fetchone()
    if row is None:
        abort(404)
    counts = get_db().execute(
        "SELECT COUNT(*) AS total, SUM(CASE WHEN excluded = 0 THEN 1 ELSE 0 END) AS included "
        "FROM session_participants WHERE session_id = ? AND removed_at IS NULL",
        (row["id"],),
    ).fetchone()
    return render_template(
        "admin_session_detail.html",
        user=user, session=row,
        participant_total=counts["total"] or 0,
        participant_included=counts["included"] or 0,
    )


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PARTNERS_FILE = REPO_ROOT / "data" / "cohorts" / "_partners.json"


def _load_partners():
    """Load partner directory and build a domain→partner_name lookup. Cached on app.config."""
    cached = app.config.get("partners_cached")
    if cached is not None:
        return cached
    try:
        with open(PARTNERS_FILE) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"partners": [], "excludePartners": []}
    domains = {}
    for p in data.get("partners", []):
        for d in p.get("domains", []):
            domains[d.strip().lower()] = p["name"]
    out = {"domains": domains, "exclude": set(data.get("excludePartners", []))}
    app.config["partners_cached"] = out
    return out


def _lookup_partner(email):
    """Return (partner_name|None, excluded_bool) for an email address."""
    p = _load_partners()
    domain = email.rsplit("@", 1)[-1].lower() if "@" in email else ""
    name = p["domains"].get(domain)
    if name is None:
        return None, False
    return name, name in p["exclude"]


def _parse_email_list(text):
    """Pull unique lowercased emails out of pasted text. Handles 'Name <email>'."""
    seen = set()
    out = []
    for line in (text or "").splitlines():
        m = EMAIL_RE.search(line)
        if not m:
            continue
        email = m.group(0).lower()
        if email in seen:
            continue
        seen.add(email)
        out.append(email)
    return out


def _add_participants_to_session(session_id, emails, enrolled_by_user_id):
    """For each email: create user if missing, enroll into session.
    Returns list of dicts with username, partner, status, initial_password (or None)."""
    db = get_db()
    results = []
    for email in emails:
        partner_name, excluded = _lookup_partner(email)
        existing = db.execute("SELECT id FROM users WHERE username = ?", (email,)).fetchone()
        if existing:
            user_id = existing["id"]
            initial_password = None
            user_status = "existing"
        else:
            initial_password = secrets.token_urlsafe(10)
            pw_hash = bcrypt.hashpw(initial_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            cur = db.execute(
                "INSERT INTO users (username, email, password_hash, is_facilitator, is_active) "
                "VALUES (?, ?, ?, 0, 1)",
                (email, email, pw_hash),
            )
            user_id = cur.lastrowid
            user_status = "created"
        try:
            db.execute(
                "INSERT INTO session_participants (session_id, user_id, partner, excluded, enrolled_by) "
                "VALUES (?, ?, ?, ?, ?)",
                (session_id, user_id, partner_name, 1 if excluded else 0, enrolled_by_user_id),
            )
            enroll_status = "enrolled"
        except sqlite3.IntegrityError:
            # Already enrolled — reactivate if previously removed
            cur = db.execute(
                "UPDATE session_participants SET removed_at = NULL WHERE session_id = ? AND user_id = ? AND removed_at IS NOT NULL",
                (session_id, user_id),
            )
            enroll_status = "reactivated" if cur.rowcount else "already-enrolled"
        results.append({
            "email": email,
            "partner": partner_name or "Unknown",
            "excluded": excluded,
            "user_status": user_status,
            "enroll_status": enroll_status,
            "initial_password": initial_password,
        })
    db.commit()
    return results


def _get_session_or_404(workshop_slug, session_slug):
    row = get_db().execute(
        "SELECT s.*, w.slug AS workshop_slug, w.name AS workshop_name "
        "FROM sessions s JOIN workshops w ON w.id = s.workshop_id "
        "WHERE w.slug = ? AND s.slug = ?",
        (workshop_slug, session_slug),
    ).fetchone()
    if row is None:
        abort(404)
    return row


@app.route("/admin/workshops/<slug>/sessions/<session_slug>/participants", methods=["GET", "POST"])
def admin_session_participants(slug, session_slug):
    user, redir = _require_facilitator()
    if redir:
        return redir
    sess = _get_session_or_404(slug, session_slug)
    added_results = []
    if request.method == "POST":
        emails = _parse_email_list(request.form.get("emails", ""))
        if emails:
            added_results = _add_participants_to_session(sess["id"], emails, user["id"])
    participants = get_db().execute(
        "SELECT sp.id, sp.partner, sp.excluded, sp.enrolled_at, "
        "       u.id AS user_id, u.username, u.email, u.last_login_at "
        "FROM session_participants sp JOIN users u ON u.id = sp.user_id "
        "WHERE sp.session_id = ? AND sp.removed_at IS NULL "
        "ORDER BY sp.partner IS NULL, sp.partner, u.username",
        (sess["id"],),
    ).fetchall()
    by_partner = {}
    for p in participants:
        key = p["partner"] or "Unknown"
        by_partner.setdefault(key, []).append(p)
    included = sum(1 for p in participants if not p["excluded"])
    return render_template(
        "admin_session_participants.html",
        user=user, session=sess, by_partner=by_partner,
        total=len(participants), included=included,
        added_results=added_results,
    )


@app.route("/admin/workshops/<slug>/sessions/<session_slug>/participants/<int:user_id>/remove", methods=["POST"])
def admin_session_participant_remove(slug, session_slug, user_id):
    cur_user, redir = _require_facilitator()
    if redir:
        return redir
    sess = _get_session_or_404(slug, session_slug)
    get_db().execute(
        "UPDATE session_participants SET removed_at = CURRENT_TIMESTAMP "
        "WHERE session_id = ? AND user_id = ? AND removed_at IS NULL",
        (sess["id"], user_id),
    )
    get_db().commit()
    return redirect(url_for("admin_session_participants", slug=slug, session_slug=session_slug))


@app.route("/admin/workshops/<slug>/sessions/<session_slug>/archive", methods=["POST"])
def admin_session_archive(slug, session_slug):
    user, redir = _require_facilitator()
    if redir:
        return redir
    workshop = get_db().execute("SELECT id FROM workshops WHERE slug = ?", (slug,)).fetchone()
    if workshop is None:
        abort(404)
    cur = get_db().execute(
        "UPDATE sessions SET status = 'archived', archived_at = CURRENT_TIMESTAMP "
        "WHERE workshop_id = ? AND slug = ? AND status != 'archived'",
        (workshop["id"], session_slug),
    )
    get_db().commit()
    if cur.rowcount == 0:
        abort(404)
    return redirect(url_for("admin_workshop_detail", slug=slug))


@app.route("/admin/workshops/<slug>/archive", methods=["POST"])
def admin_workshop_archive(slug):
    user, redir = _require_facilitator()
    if redir:
        return redir
    cur = get_db().execute(
        "UPDATE workshops SET status = 'archived', archived_at = CURRENT_TIMESTAMP WHERE slug = ? AND status != 'archived'",
        (slug,),
    )
    get_db().commit()
    if cur.rowcount == 0:
        abort(404)
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/users-screen")
def admin_users_screen():
    user, redir = _require_facilitator()
    if redir:
        return redir
    users = get_db().execute(
        "SELECT id, username, display_name, email, is_facilitator, is_active, created_at, last_login_at "
        "FROM users ORDER BY created_at DESC"
    ).fetchall()
    return render_template("admin.html", user=user, users=users)


@app.route("/admin/users", methods=["POST"])
def admin_create_user():
    user = current_user()
    if user is None or not user["is_facilitator"]:
        abort(403)
    username = (request.form.get("username") or "").strip().lower()
    if not re.fullmatch(r"[a-z0-9._-]{3,40}", username):
        return jsonify(error="username must be 3-40 chars, lowercase alphanumeric + . _ -"), 400
    display_name = (request.form.get("display_name") or "").strip() or None
    email = (request.form.get("email") or "").strip() or None
    is_facilitator = 1 if request.form.get("is_facilitator") == "on" else 0
    initial_password = secrets.token_urlsafe(12)
    pw_hash = bcrypt.hashpw(initial_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    try:
        get_db().execute(
            "INSERT INTO users (username, password_hash, email, display_name, is_facilitator) VALUES (?, ?, ?, ?, ?)",
            (username, pw_hash, email, display_name, is_facilitator),
        )
        get_db().commit()
    except sqlite3.IntegrityError:
        return jsonify(error=f"username '{username}' already exists"), 409
    return jsonify(username=username, initial_password=initial_password, is_facilitator=bool(is_facilitator))


@app.route("/admin/users/<int:user_id>/reset-password", methods=["POST"])
def admin_reset_password(user_id):
    user = current_user()
    if user is None or not user["is_facilitator"]:
        abort(403)
    new_pw = secrets.token_urlsafe(12)
    pw_hash = bcrypt.hashpw(new_pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    cur = get_db().execute("UPDATE users SET password_hash = ? WHERE id = ?", (pw_hash, user_id))
    get_db().commit()
    if cur.rowcount == 0:
        return jsonify(error="user not found"), 404
    return jsonify(user_id=user_id, new_password=new_pw)


@app.route("/admin/users/<int:user_id>/toggle-active", methods=["POST"])
def admin_toggle_active(user_id):
    user = current_user()
    if user is None or not user["is_facilitator"]:
        abort(403)
    cur = get_db().execute("UPDATE users SET is_active = 1 - is_active WHERE id = ?", (user_id,))
    get_db().commit()
    if cur.rowcount == 0:
        return jsonify(error="user not found"), 404
    return jsonify(user_id=user_id)


@app.route("/admin/views/<int:user_id>")
def admin_user_views(user_id):
    user = current_user()
    if user is None or not user["is_facilitator"]:
        abort(403)
    target = get_db().execute("SELECT id, username, display_name FROM users WHERE id = ?", (user_id,)).fetchone()
    if target is None:
        abort(404)
    views = get_db().execute(
        "SELECT path, status, viewed_at FROM page_views WHERE user_id = ? ORDER BY viewed_at DESC LIMIT 200",
        (user_id,),
    ).fetchall()
    return render_template("user_views.html", user=user, target=target, views=views)


# ---------------------------- CLI: bootstrap admin ----------------------------

@app.cli.command("init-db")
def cli_init_db():
    """Create the SQLite tables."""
    init_db()
    print(f"initialized {DB_PATH}")


@app.cli.command("add-admin")
def cli_add_admin():
    """Create the first facilitator account interactively."""
    import getpass
    init_db()
    username = input("Username: ").strip().lower()
    if not re.fullmatch(r"[a-z0-9._-]{3,40}", username):
        raise SystemExit("invalid username")
    display = input("Display name (optional): ").strip() or None
    email = input("Email (optional): ").strip() or None
    pw1 = getpass.getpass("Password: ")
    pw2 = getpass.getpass("Confirm: ")
    if pw1 != pw2 or len(pw1) < 8:
        raise SystemExit("passwords don't match or under 8 chars")
    pw_hash = bcrypt.hashpw(pw1.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    conn = sqlite3.connect(str(DB_PATH))
    try:
        conn.execute(
            "INSERT INTO users (username, password_hash, email, display_name, is_facilitator) VALUES (?, ?, ?, ?, 1)",
            (username, pw_hash, email, display),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise SystemExit(f"username '{username}' already exists")
    finally:
        conn.close()
    print(f"created facilitator: {username}")


# Initialize DB at import time so gunicorn workers see the schema.
init_db()

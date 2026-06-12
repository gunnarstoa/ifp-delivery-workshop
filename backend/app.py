"""IFP Delivery Workshop — auth gateway and static-page server.

Serves the existing docs/, css/, data/ trees behind username/password auth.
Logs every authenticated request to page_views for later analysis.
Facilitator-only pages additionally require users.is_facilitator = 1.
"""
import os
import re
import secrets
import sqlite3
import time
from datetime import datetime, timezone
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
    r"^/(docs/(15-facilitator|16-facilitator-toolkit|cohort-tracker)|data/|admin)"
)
# Paths that bypass auth entirely (login form, static assets, health).
PUBLIC_PREFIXES = ("/login", "/static/", "/css/", "/js/", "/images/", "/favicon", "/healthz", "/robots.txt")

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
    return redirect("/docs/01-overview.html")


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
    return _serve_repo_file("docs", filename)


@app.route("/data/<path:filename>")
def serve_data(filename):
    return _serve_repo_file("data", filename)


@app.route("/css/<path:filename>")
def serve_css(filename):
    return _serve_repo_file("css", filename)


@app.route("/js/<path:filename>")
def serve_js(filename):
    return _serve_repo_file("js", filename)


@app.route("/images/<path:filename>")
def serve_images(filename):
    return _serve_repo_file("images", filename)


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


@app.route("/admin")
def admin_dashboard():
    user, redir = _require_facilitator()
    if redir:
        return redir
    workshops = get_db().execute(
        "SELECT w.id, w.slug, w.name, w.short_description, w.contact_email, w.status, w.created_at, "
        "       u.username AS created_by_username "
        "FROM workshops w LEFT JOIN users u ON u.id = w.created_by "
        "WHERE w.status != 'archived' "
        "ORDER BY w.created_at DESC"
    ).fetchall()
    return render_template("admin_dashboard.html", user=user, workshops=workshops)


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
    return render_template("admin_workshop_detail.html", user=user, workshop=workshop)


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

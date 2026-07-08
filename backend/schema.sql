CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL COLLATE NOCASE,
  password_hash TEXT NOT NULL,
  email TEXT,
  display_name TEXT,
  is_facilitator INTEGER NOT NULL DEFAULT 0,
  is_active INTEGER NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_login_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS page_views (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  path TEXT NOT NULL,
  query TEXT,
  status INTEGER NOT NULL,
  viewed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  referer TEXT,
  user_agent TEXT,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_page_views_user_time ON page_views(user_id, viewed_at);
CREATE INDEX IF NOT EXISTS idx_page_views_path_time ON page_views(path, viewed_at);

CREATE TABLE IF NOT EXISTS login_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username_attempted TEXT NOT NULL,
  succeeded INTEGER NOT NULL,
  ip TEXT,
  user_agent TEXT,
  occurred_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_login_events_time ON login_events(occurred_at);

CREATE TABLE IF NOT EXISTS workshops (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slug TEXT UNIQUE NOT NULL COLLATE NOCASE,
  name TEXT NOT NULL,
  short_description TEXT,
  content_root TEXT,
  contact_email TEXT,
  status TEXT NOT NULL DEFAULT 'active',
  created_by INTEGER,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  archived_at TIMESTAMP,
  FOREIGN KEY (created_by) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_workshops_status ON workshops(status);

CREATE TABLE IF NOT EXISTS sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  workshop_id INTEGER NOT NULL,
  slug TEXT NOT NULL COLLATE NOCASE,
  name TEXT NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  status TEXT NOT NULL DEFAULT 'upcoming',
  notes TEXT,
  created_by INTEGER,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  archived_at TIMESTAMP,
  FOREIGN KEY (workshop_id) REFERENCES workshops(id) ON DELETE CASCADE,
  FOREIGN KEY (created_by) REFERENCES users(id),
  UNIQUE (workshop_id, slug)
);

CREATE INDEX IF NOT EXISTS idx_sessions_dates ON sessions(start_date, end_date);
CREATE INDEX IF NOT EXISTS idx_sessions_workshop ON sessions(workshop_id);
CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status);

CREATE TABLE IF NOT EXISTS session_participants (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  partner TEXT,
  excluded INTEGER NOT NULL DEFAULT 0,
  enrolled_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  enrolled_by INTEGER,
  removed_at TIMESTAMP,
  FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (enrolled_by) REFERENCES users(id),
  UNIQUE (session_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_sp_session_active ON session_participants(session_id) WHERE removed_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_sp_user ON session_participants(user_id);

CREATE TABLE IF NOT EXISTS session_surveys (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL,
  kind TEXT NOT NULL,
  filename TEXT,
  uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  uploaded_by INTEGER,
  total_rows INTEGER NOT NULL DEFAULT 0,
  is_anonymous INTEGER NOT NULL DEFAULT 0,
  headers_json TEXT,
  FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
  FOREIGN KEY (uploaded_by) REFERENCES users(id),
  UNIQUE (session_id, kind)
);

CREATE TABLE IF NOT EXISTS survey_responses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  survey_id INTEGER NOT NULL,
  participant_user_id INTEGER,
  raw_email TEXT,
  responses_json TEXT NOT NULL,
  score INTEGER,
  passed INTEGER,
  attempt_number INTEGER,
  submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (survey_id) REFERENCES session_surveys(id) ON DELETE CASCADE,
  FOREIGN KEY (participant_user_id) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_survey_responses_survey ON survey_responses(survey_id);

CREATE TABLE IF NOT EXISTS survey_templates (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  workshop_id INTEGER NOT NULL,
  kind TEXT NOT NULL,
  intro TEXT,
  questions_json TEXT NOT NULL,
  passing_score INTEGER NOT NULL DEFAULT 70,
  max_attempts INTEGER,
  questions_per_attempt INTEGER,
  shuffle_options INTEGER NOT NULL DEFAULT 1,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by INTEGER,
  FOREIGN KEY (workshop_id) REFERENCES workshops(id) ON DELETE CASCADE,
  FOREIGN KEY (updated_by) REFERENCES users(id),
  UNIQUE (workshop_id, kind)
);

-- Discussion foundation (B/19): per-session monitors, page-anchored threads,
-- replies, reactions, presence, read state, and uploads. Q&A panels and
-- monitor dashboards in later PRs all read from these tables.

CREATE TABLE IF NOT EXISTS session_monitors (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  assigned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  assigned_by INTEGER,
  removed_at TIMESTAMP,
  FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (assigned_by) REFERENCES users(id),
  UNIQUE (session_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_sm_session_active ON session_monitors(session_id) WHERE removed_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_sm_user ON session_monitors(user_id);

CREATE TABLE IF NOT EXISTS threads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL,
  page_path TEXT NOT NULL,
  author_user_id INTEGER NOT NULL,
  anonymous INTEGER NOT NULL DEFAULT 0,
  kind TEXT NOT NULL DEFAULT 'question',
  body TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  answered_at TIMESTAMP,
  answered_by INTEGER,
  hidden_at TIMESTAMP,
  hidden_by INTEGER,
  FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
  FOREIGN KEY (author_user_id) REFERENCES users(id),
  FOREIGN KEY (answered_by) REFERENCES users(id),
  FOREIGN KEY (hidden_by) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_threads_session_page ON threads(session_id, page_path);
CREATE INDEX IF NOT EXISTS idx_threads_session_status ON threads(session_id, status);
CREATE INDEX IF NOT EXISTS idx_threads_session_created ON threads(session_id, created_at);

CREATE TABLE IF NOT EXISTS replies (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  thread_id INTEGER NOT NULL,
  author_user_id INTEGER NOT NULL,
  is_monitor_reply INTEGER NOT NULL DEFAULT 0,
  body TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  hidden_at TIMESTAMP,
  hidden_by INTEGER,
  FOREIGN KEY (thread_id) REFERENCES threads(id) ON DELETE CASCADE,
  FOREIGN KEY (author_user_id) REFERENCES users(id),
  FOREIGN KEY (hidden_by) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_replies_thread ON replies(thread_id, created_at);

CREATE TABLE IF NOT EXISTS reactions (
  thread_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  kind TEXT NOT NULL DEFAULT 'me_too',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (thread_id, user_id, kind),
  FOREIGN KEY (thread_id) REFERENCES threads(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS presence (
  session_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  page_path TEXT NOT NULL,
  last_seen_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (session_id, user_id, page_path),
  FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_presence_recent ON presence(session_id, page_path, last_seen_at);

CREATE TABLE IF NOT EXISTS read_state (
  user_id INTEGER NOT NULL,
  thread_id INTEGER NOT NULL,
  last_read_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, thread_id),
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (thread_id) REFERENCES threads(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_read_state_user ON read_state(user_id, last_read_at);

CREATE TABLE IF NOT EXISTS uploads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  thread_id INTEGER,
  reply_id INTEGER,
  filename TEXT NOT NULL,
  stored_path TEXT NOT NULL,
  mime_type TEXT,
  size_bytes INTEGER,
  uploaded_by INTEGER NOT NULL,
  uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (thread_id) REFERENCES threads(id) ON DELETE CASCADE,
  FOREIGN KEY (reply_id) REFERENCES replies(id) ON DELETE CASCADE,
  FOREIGN KEY (uploaded_by) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_uploads_thread ON uploads(thread_id);
CREATE INDEX IF NOT EXISTS idx_uploads_reply ON uploads(reply_id);

CREATE TABLE IF NOT EXISTS lab_check_attempts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  session_id INTEGER NOT NULL,
  workshop_slug TEXT NOT NULL,
  page_path TEXT NOT NULL,
  check_id TEXT NOT NULL,
  passed INTEGER NOT NULL DEFAULT 0,
  attempted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_lca_session_user ON lab_check_attempts(session_id, user_id);
CREATE INDEX IF NOT EXISTS idx_lca_check ON lab_check_attempts(workshop_slug, check_id);

-- Tenant pool (one row per pre-provisioned Anaplan credential set per workshop).
-- password_enc is Fernet-encrypted with TENANT_ENCRYPTION_KEY from app.env.
CREATE TABLE IF NOT EXISTS tenants (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  workshop_id INTEGER NOT NULL,
  email TEXT NOT NULL,
  username TEXT NOT NULL,
  password_enc TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'available',    -- available | maintenance | retired
  last_refreshed_at TIMESTAMP,
  notes TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (workshop_id) REFERENCES workshops(id) ON DELETE CASCADE,
  UNIQUE (workshop_id, username)
);
CREATE INDEX IF NOT EXISTS idx_tenants_workshop ON tenants(workshop_id);
CREATE INDEX IF NOT EXISTS idx_tenants_workshop_status ON tenants(workshop_id, status);

-- Tenant assignment ledger. released_at IS NULL = active. hold_until is the
-- planned release date (default session.end_date + 1). Nightly job (added in
-- PR 2) will release when today > hold_until.
CREATE TABLE IF NOT EXISTS tenant_assignments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tenant_id INTEGER NOT NULL,
  session_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  assigned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  hold_until DATE,
  released_at TIMESTAMP,
  released_reason TEXT,                        -- session_ended | removed | extended | manual
  FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE INDEX IF NOT EXISTS idx_ta_tenant_active ON tenant_assignments(tenant_id) WHERE released_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_ta_session ON tenant_assignments(session_id);
CREATE INDEX IF NOT EXISTS idx_ta_user_active ON tenant_assignments(user_id) WHERE released_at IS NULL;

# Anaplan Workshops — Deploy & Operate

End-to-end deployment of the workshops platform at **https://anaplan-workshops.com**.
A single Lightsail instance running Caddy + Gunicorn/Flask + SQLite,
auto-HTTPS via Let's Encrypt, fronted by Route 53.

**Cost:** ~$5/mo Lightsail + ~$0.50/mo Route 53 zone.

---

## Architecture

```
                       anaplan-workshops.com
                                │
                 Route 53 A record → static IP
                                │
                         ┌──────▼──────┐
                         │    Caddy    │  :80 :443  auto Let's Encrypt
                         └──────┬──────┘
                                │ reverse_proxy
                         ┌──────▼──────┐
                         │   gunicorn  │  :8000  (systemd: workshop.service)
                         └──────┬──────┘
                         ┌──────▼──────┐
                         │    Flask    │  backend/app.py
                         └──────┬──────┘
                  /var/lib/workshop/workshop.db   (SQLite WAL)
```

**What the app does:**

| Surface | Path | Audience |
| --- | --- | --- |
| Login | `/login` | All users |
| Workshop content | `/w/<slug>/<page>.html` | Authenticated participants + facilitators |
| Native survey form | `/w/<slug>/survey/<kind>` | Authenticated participants |
| Admin dashboard | `/admin` | Facilitators only |
| Workshops CRUD | `/admin/workshops/...` | Facilitators only |
| Sessions CRUD | `/admin/workshops/<slug>/sessions/...` | Facilitators only |
| Survey template editor | `/admin/workshops/<slug>/survey-templates/...` | Facilitators only |
| Per-session reports | `/admin/workshops/<slug>/sessions/<sess>/reports/...` | Facilitators only |
| Per-workshop rollup | `/admin/workshops/<slug>/rollup` | Facilitators only |
| DB backup download | `/admin/backup.db` | Facilitators only |

**Schema:** `users`, `login_events`, `page_views`, `workshops`, `sessions`, `session_participants`, `session_surveys`, `survey_responses`, `survey_templates`. Defined in `backend/schema.sql`; auto-applied at app start; re-runnable with `sqlite3 /var/lib/workshop/workshop.db < backend/schema.sql`.

---

## One-time setup

### 1. Install AWS CLI and configure credentials

```bash
brew install awscli
aws configure
```

Paste in your Access Key ID + Secret Access Key. Default region `us-east-1`. The IAM user needs `AmazonLightsailFullAccess` + `AmazonRoute53FullAccess`.

### 2. Confirm the Route 53 hosted zone exists

```bash
aws route53 list-hosted-zones-by-name --dns-name anaplan-workshops.com
```

If empty:

```bash
aws route53 create-hosted-zone --name anaplan-workshops.com --caller-reference "$(date +%s)"
```

### 3. Run the deploy script

```bash
cd /Users/gunnarstoa/git-repos/ifp-delivery-workshop
./scripts/aws-deploy.sh
```

Creates SSH key pair (saved as `.aws-workshop-key.pem` — **keep this**), allocates a static IP, creates a 1 GB Ubuntu 22.04 Lightsail instance with cloud-init bootstrap, attaches the static IP, opens HTTP/HTTPS in the firewall, adds Route 53 A records.

~3 min for the script, ~3-5 min more for cloud-init.

### 4. Create the first facilitator account

```bash
ssh -t -i /Users/gunnarstoa/git-repos/ifp-delivery-workshop/.aws-workshop-key.pem ubuntu@<STATIC_IP> \
  'cd /srv/workshop/app && sudo -u workshop env $(sudo cat /etc/workshop/app.env | xargs) .venv/bin/flask --app backend.app add-admin'
```

Prompts for username, display name, email, password. That account gets `is_facilitator=1` and can sign in at `/login`.

### 5. Wire up GitHub Actions for push-to-deploy

The CI workflow lives in the repo as `infra/deploy-workshop.yml.template` (the PAT used to push this repo lacks `workflow` scope, so it can't write to `.github/workflows/` via API). Copy it via the GitHub web UI:

1. Open `infra/deploy-workshop.yml.template` on GitHub → **Copy raw file**
2. **Add file** → **Create new file** at the repo root
3. Name it exactly `.github/workflows/deploy-workshop.yml`
4. Paste, commit to `main`

Add two secrets at `/settings/secrets/actions`:

| Secret | Value |
| --- | --- |
| `INSTANCE_IP` | The static IP from the deploy script |
| `SSH_PRIVATE_KEY` | Full contents of `.aws-workshop-key.pem` |

After they're added every push to `main` redeploys.

---

## Day-to-day operations

### Manual redeploy (no CI needed)

```bash
ssh -i .aws-workshop-key.pem ubuntu@<IP> \
  'sudo -u workshop git -C /srv/workshop/app pull --quiet && sudo systemctl restart workshop'
```

### Sync schema (re-runnable, no destructive ops)

```bash
ssh -i .aws-workshop-key.pem ubuntu@<IP> \
  'sudo sqlite3 /var/lib/workshop/workshop.db < /srv/workshop/app/backend/schema.sql'
```

### Reload Python deps after a `requirements.txt` change

```bash
ssh -i .aws-workshop-key.pem ubuntu@<IP> \
  'sudo -u workshop /srv/workshop/app/.venv/bin/pip install --quiet -r /srv/workshop/app/backend/requirements.txt && sudo systemctl restart workshop'
```

### Live application logs

```bash
ssh -i .aws-workshop-key.pem ubuntu@<IP> 'sudo journalctl -u workshop -f'
```

### Caddy / HTTPS logs

```bash
ssh -i .aws-workshop-key.pem ubuntu@<IP> 'sudo journalctl -u caddy -f'
```

---

## Backups

The whole production DB is **one SQLite file at `/var/lib/workshop/workshop.db`**. Back it up regularly. Three ways, easiest first:

### Option A — Admin download button

`/admin` → Users & activity card → **Download backup ↓**. Streams a vacuumed snapshot through the browser. Quick + convenient.

### Option B — SSH + scp (script this into your local cron)

```bash
ssh -i .aws-workshop-key.pem ubuntu@<IP> \
  "sudo sqlite3 /var/lib/workshop/workshop.db '.backup /tmp/workshop-backup.db'"
scp -i .aws-workshop-key.pem ubuntu@<IP>:/tmp/workshop-backup.db ~/Backups/workshop-$(date +%F).db
```

### Option C — Lightsail snapshot

```bash
aws lightsail create-instance-snapshot --instance-name workshop --instance-snapshot-name workshop-$(date +%F)
```

Snapshots include the whole instance disk. Restore via `aws lightsail create-instances-from-snapshot`.

---

## Tear it all down

```bash
./scripts/aws-destroy.sh
```

Removes instance, static IP, key pair, A records. Leaves the Route 53 hosted zone (it's reusable; you'd just pay $0.50/mo for it).

---

## Adding a new workshop

1. **DB:** `/admin/workshops` → **+ New workshop** → fill slug (e.g. `fcr`), display name, dates, contact email.
2. **Content:** create the folder `docs/<slug>/` and copy IFP as a starter (`cp -r docs/ifp/ docs/<slug>/`), then edit page titles + sidebar links per workshop. Push to `main`; CI deploys.
3. **Toolkit:** create the folder `toolkit/<slug>/` similarly (`cp -r toolkit/ifp/ toolkit/<slug>/`) and edit each asset.
4. **Survey templates:** `/admin/workshops/<slug>/survey-templates` → **Load IFP starter** on pre and post (then edit), or build from scratch.
5. **Promote a session:** `/admin/workshops/<slug>` → **+ New session** → paste participant emails → share `/w/<slug>/survey/pre` link in the kickoff email.

---

## Adding a new partner domain

Edit `data/cohorts/_partners.json` to add the entry, push, and (if there are existing participants in the DB with that domain still showing `partner = NULL`) run a one-line SQL backfill — see prior PR backfills in the git log for templates.

---

## Cuts intentionally not in v1

- Password reset by email (facilitator resets manually via the admin password-reset action).
- Bulk user import (one paste-of-emails at a time per session).
- Multi-instance / load balancing (single box is plenty for 1–2 cohorts/week).
- Off-instance backup automation (manual via the three options above for v1; layer in S3 sync next).
- CloudWatch / external monitoring (`journalctl -u workshop -f` for v1).

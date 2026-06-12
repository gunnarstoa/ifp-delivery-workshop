# Deploying the workshop to AWS Lightsail

End-to-end deployment of the workshop site (auth-gated, with per-user page-view logging) at **https://anaplan-workshops.com**, running on a single Lightsail instance with auto-HTTPS via Caddy.

Total cost: **~$5/month** (Lightsail instance) + **$0.50/month** (Route 53 hosted zone).

---

## One-time setup (your part)

You'll click/type things at five points. Everything else is automated.

### 1. Install AWS CLI and configure credentials

```bash
brew install awscli
aws configure
```

Paste in your **Access Key ID**, **Secret Access Key**, and set the default region to `us-east-1`. The IAM user needs these permissions:

- `lightsail:*` (manage the instance, IP, key pair, firewall)
- `route53:ListHostedZones`, `route53:ChangeResourceRecordSets`, `route53:GetChange`
- `sts:GetCallerIdentity` (preflight check)

If you don't have an IAM user yet, create one in the AWS console with the policies `AmazonLightsailFullAccess` and `AmazonRoute53FullAccess` attached.

### 2. Confirm the Route 53 hosted zone exists

`anaplan-workshops.com` needs a Route 53 hosted zone — that's where the deploy script writes the A record.

If you registered through Route 53, the zone exists already. Verify:

```bash
aws route53 list-hosted-zones-by-name --dns-name anaplan-workshops.com
```

If empty, create one:

```bash
aws route53 create-hosted-zone --name anaplan-workshops.com --caller-reference "$(date +%s)"
```

### 3. Run the deploy script

```bash
cd /Users/gunnarstoa/git-repos/ifp-delivery-workshop
./scripts/aws-deploy.sh
```

This does:

- Creates an SSH key pair in Lightsail (saves the private key to `.aws-workshop-key.pem` in the repo — **keep this file**)
- Allocates a static IP
- Creates a 1 GB Ubuntu 22.04 Lightsail instance and feeds it the cloud-init bootstrap script
- Attaches the static IP, opens HTTP/HTTPS in the firewall
- Adds Route 53 A records for `anaplan-workshops.com` and `www.anaplan-workshops.com` → static IP

Total time: ~3 minutes for the script, plus another ~3–5 minutes for the instance to finish first-boot installation (Caddy, Python, Flask, the repo, the systemd service).

### 4. Create the first facilitator account

Once the instance is up and DNS has propagated (5–10 min):

```bash
ssh -i .aws-workshop-key.pem ubuntu@<STATIC_IP_FROM_DEPLOY_OUTPUT>
sudo -u workshop env $(sudo cat /etc/workshop/app.env | xargs) \
  /srv/workshop/app/.venv/bin/flask --app backend.app add-admin
```

Enter a username and password at the prompt. That account gets `is_facilitator = 1` and can sign in at https://anaplan-workshops.com/login to access `/admin` and create everyone else.

### 5. Wire up GitHub Actions for push-to-deploy

The workflow file lives in the repo as `infra/deploy-workshop.yml.template` (the PAT used to ship this PR doesn't have `workflow` scope, so the file can't be committed to `.github/workflows/` via API). Move it via the GitHub web UI:

1. Open `infra/deploy-workshop.yml.template` on GitHub, click the `...` menu → **Copy raw file**
2. Click **Add file** → **Create new file** at the repo root
3. Name it exactly `.github/workflows/deploy-workshop.yml` (GitHub will create the folders)
4. Paste the contents, commit to `main`

Then add two secrets at https://github.com/gunnarstoa/ifp-delivery-workshop/settings/secrets/actions:

| Secret name        | Value                                                  |
| ------------------ | ------------------------------------------------------ |
| `INSTANCE_IP`      | The static IP from the deploy script output            |
| `SSH_PRIVATE_KEY`  | The full contents of `.aws-workshop-key.pem`           |

After they're added, every push to `main` redeploys. The workflow logs are at https://github.com/gunnarstoa/ifp-delivery-workshop/actions.

---

## After the first deploy

- **Sign in:** https://anaplan-workshops.com/login
- **Admin (facilitators only):** https://anaplan-workshops.com/admin — create users, see who's logged in, reset passwords, view per-user activity
- **Workshop content:** the existing `docs/*.html` pages are served as before, behind login

The hidden-URL facilitator pages (e.g. `cohort-tracker-m4q9wx.html`) still work at the same paths — but they now require login *and* the `is_facilitator` flag. The obscure URLs become belt-and-suspenders rather than the only protection.

---

## How it all fits together

```
                                anaplan-workshops.com
                                         │
                          Route 53 A record → static IP
                                         │
                                    ┌────▼────┐
                                    │ Caddy   │  :80, :443  (auto Let's Encrypt)
                                    └────┬────┘
                                         │ reverse_proxy
                                    ┌────▼────┐
                                    │ gunicorn│  :8000     (systemd: workshop.service)
                                    └────┬────┘
                                         │
                                    ┌────▼────┐
                                    │ Flask   │  backend/app.py
                                    │  - auth │  (bcrypt + signed session cookies)
                                    │  - log  │  (page_views table)
                                    │  - serve│  (docs/, data/, css/, js/, images/)
                                    │  - admin│  (/admin, /admin/users, ...)
                                    └────┬────┘
                                         │
                                  /var/lib/workshop/workshop.db
                                    (SQLite, WAL mode)
```

---

## Common operations

### View live application logs

```bash
ssh -i .aws-workshop-key.pem ubuntu@<INSTANCE_IP>
sudo journalctl -u workshop -f
```

### View Caddy / HTTPS logs

```bash
sudo journalctl -u caddy -f
```

### Back up the SQLite database

```bash
ssh -i .aws-workshop-key.pem ubuntu@<INSTANCE_IP> \
  "sudo sqlite3 /var/lib/workshop/workshop.db '.backup /tmp/workshop-backup.db'"
scp -i .aws-workshop-key.pem ubuntu@<INSTANCE_IP>:/tmp/workshop-backup.db ./workshop-backup-$(date +%F).db
```

Schedule this with cron on your local machine, or follow up to add a Lightsail snapshot policy.

### Tear it all down

```bash
./scripts/aws-destroy.sh
```

This removes the instance, static IP, key pair, and DNS A records. It leaves the Route 53 hosted zone alone (so you can re-deploy later).

---

## What's NOT in this deploy (intentional v1 cuts)

- **Password reset by email.** SMTP not configured. Facilitators reset passwords in `/admin` and hand the new password to the user.
- **Bulk user import.** Add users one at a time via `/admin`. Follow-up PR can wire a CSV importer.
- **Multi-instance / load balancing.** Single Lightsail box is plenty for 1–2 cohorts/week.
- **Off-instance backups.** Manual `sqlite3 .backup` for now; add a daily cron and S3 sync later.
- **CloudWatch / external monitoring.** `journalctl -u workshop -f` works for v1.

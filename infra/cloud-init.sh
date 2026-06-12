#!/bin/bash
# Cloud-init script executed once on Lightsail instance first boot.
# Installs Caddy + Python, clones the workshop repo, sets up systemd service,
# and starts everything. Idempotent — safe to re-run.
#
# Required environment substitutions before passing to Lightsail user-data:
#   __DOMAIN__   → anaplan-workshops.com
#   __REPO_URL__ → https://github.com/gunnarstoa/ifp-delivery-workshop.git
#   __BRANCH__   → main
set -euxo pipefail
exec > >(tee -a /var/log/workshop-bootstrap.log) 2>&1
echo "=== workshop bootstrap @ $(date -u +%FT%TZ) ==="

DOMAIN="__DOMAIN__"
REPO_URL="__REPO_URL__"
BRANCH="__BRANCH__"

# --- Apt prerequisites + Caddy repo ---
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y curl ca-certificates gnupg debian-keyring debian-archive-keyring apt-transport-https \
                   python3 python3-venv python3-pip git sqlite3 ufw

if [ ! -f /etc/apt/sources.list.d/caddy-stable.list ]; then
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list
  apt-get update -y
fi
apt-get install -y caddy

# --- Service user + directories ---
id -u workshop >/dev/null 2>&1 || useradd --system --create-home --shell /usr/sbin/nologin --home-dir /srv/workshop workshop
mkdir -p /srv/workshop /var/lib/workshop /etc/workshop
chown -R workshop:workshop /srv/workshop /var/lib/workshop
chmod 750 /etc/workshop

# --- Clone or update repo ---
APP_DIR=/srv/workshop/app
if [ ! -d "$APP_DIR/.git" ]; then
  sudo -u workshop git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
else
  sudo -u workshop git -C "$APP_DIR" fetch origin
  sudo -u workshop git -C "$APP_DIR" reset --hard "origin/$BRANCH"
fi

# --- Python venv + deps ---
if [ ! -d "$APP_DIR/.venv" ]; then
  sudo -u workshop python3 -m venv "$APP_DIR/.venv"
fi
sudo -u workshop "$APP_DIR/.venv/bin/pip" install --upgrade pip wheel
sudo -u workshop "$APP_DIR/.venv/bin/pip" install -r "$APP_DIR/backend/requirements.txt"

# --- App secret + env file ---
if [ ! -f /etc/workshop/app.env ]; then
  SECRET=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
  cat > /etc/workshop/app.env <<EOF
WORKSHOP_SECRET_KEY=$SECRET
WORKSHOP_DB=/var/lib/workshop/workshop.db
WORKSHOP_PRODUCTION=1
PYTHONUNBUFFERED=1
EOF
  chmod 640 /etc/workshop/app.env
  chown root:workshop /etc/workshop/app.env
fi

# --- systemd unit ---
install -m 0644 "$APP_DIR/infra/workshop.service" /etc/systemd/system/workshop.service
systemctl daemon-reload
systemctl enable --now workshop

# --- Caddy site env + Caddyfile ---
cat > /etc/caddy/site.env <<EOF
DOMAIN=$DOMAIN
EOF
chmod 644 /etc/caddy/site.env
install -m 0644 "$APP_DIR/infra/Caddyfile" /etc/caddy/Caddyfile

# Inject DOMAIN env into Caddy systemd override
mkdir -p /etc/systemd/system/caddy.service.d
cat > /etc/systemd/system/caddy.service.d/override.conf <<EOF
[Service]
EnvironmentFile=/etc/caddy/site.env
EOF
systemctl daemon-reload
systemctl restart caddy

# --- Firewall: SSH + HTTP/HTTPS ---
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

echo "=== bootstrap complete @ $(date -u +%FT%TZ) ==="
echo "Next: SSH in and run: cd /srv/workshop/app && sudo -u workshop env \$(cat /etc/workshop/app.env | xargs) .venv/bin/flask --app backend.app add-admin"

#!/usr/bin/env bash
# Provision the IFP Delivery Workshop on AWS Lightsail + Route 53.
#
# Idempotent. Safe to re-run — existing resources are reused, not duplicated.
#
# Usage: ./scripts/aws-deploy.sh [domain]
# Default domain: anaplan-workshops.com
#
# Requires:
#   - aws CLI installed and configured (aws configure)
#   - IAM permissions: lightsail:*, route53:ChangeResourceRecordSets,
#     route53:ListHostedZones, route53:GetChange
#   - The domain's hosted zone must already exist in Route 53.
#
# Creates / reuses:
#   - Lightsail static IP   "workshop-ip"
#   - Lightsail instance    "workshop"   (Ubuntu 22.04, micro_3_0, $5/mo)
#   - Route 53 A record     <domain> + www.<domain> → static IP

set -euo pipefail

DOMAIN="${1:-anaplan-workshops.com}"
REPO_URL="${WORKSHOP_REPO_URL:-https://github.com/gunnarstoa/ifp-delivery-workshop.git}"
BRANCH="${WORKSHOP_BRANCH:-main}"
REGION="${AWS_REGION:-us-east-1}"
BUNDLE="${WORKSHOP_BUNDLE:-micro_3_0}"   # 1 GB RAM, 2 vCPU, 40 GB SSD — ~$5/mo
INSTANCE_NAME="workshop"
STATIC_IP_NAME="workshop-ip"
KEY_PAIR_NAME="${WORKSHOP_KEY_PAIR:-workshop-key}"
BLUEPRINT="${WORKSHOP_BLUEPRINT:-ubuntu_22_04}"

# --- Preflight ---
echo "==> preflight"
command -v aws >/dev/null || { echo "aws CLI not found. brew install awscli"; exit 1; }
aws sts get-caller-identity >/dev/null || { echo "aws not configured. run: aws configure"; exit 1; }

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CLOUD_INIT_TEMPLATE="$REPO_ROOT/infra/cloud-init.sh"
[ -f "$CLOUD_INIT_TEMPLATE" ] || { echo "missing $CLOUD_INIT_TEMPLATE"; exit 1; }

# Render user-data from template.
USER_DATA_FILE="$(mktemp)"
trap 'rm -f "$USER_DATA_FILE"' EXIT
sed \
  -e "s|__DOMAIN__|$DOMAIN|g" \
  -e "s|__REPO_URL__|$REPO_URL|g" \
  -e "s|__BRANCH__|$BRANCH|g" \
  "$CLOUD_INIT_TEMPLATE" > "$USER_DATA_FILE"

echo "==> using region: $REGION   domain: $DOMAIN   bundle: $BUNDLE"

# --- SSH key pair ---
echo "==> SSH key pair: $KEY_PAIR_NAME"
if ! aws lightsail get-key-pair --key-pair-name "$KEY_PAIR_NAME" --region "$REGION" >/dev/null 2>&1; then
  KEY_OUT_PEM="$REPO_ROOT/.aws-workshop-key.pem"
  echo "  creating new key pair, saving private key to $KEY_OUT_PEM"
  aws lightsail create-key-pair --key-pair-name "$KEY_PAIR_NAME" --region "$REGION" \
    --query 'privateKeyBase64' --output text > "$KEY_OUT_PEM"
  chmod 600 "$KEY_OUT_PEM"
  echo "  >>> KEEP THIS FILE. You will need it to SSH in and to upload to GitHub secrets."
else
  echo "  key pair exists, reusing"
fi

# --- Static IP ---
echo "==> static IP: $STATIC_IP_NAME"
if ! aws lightsail get-static-ip --static-ip-name "$STATIC_IP_NAME" --region "$REGION" >/dev/null 2>&1; then
  aws lightsail allocate-static-ip --static-ip-name "$STATIC_IP_NAME" --region "$REGION" >/dev/null
fi
STATIC_IP=$(aws lightsail get-static-ip --static-ip-name "$STATIC_IP_NAME" --region "$REGION" --query 'staticIp.ipAddress' --output text)
echo "  static IP: $STATIC_IP"

# --- Instance ---
echo "==> Lightsail instance: $INSTANCE_NAME"
if ! aws lightsail get-instance --instance-name "$INSTANCE_NAME" --region "$REGION" >/dev/null 2>&1; then
  echo "  creating instance (this takes ~30-60s)"
  AZ="${REGION}a"
  aws lightsail create-instances \
    --instance-names "$INSTANCE_NAME" \
    --availability-zone "$AZ" \
    --blueprint-id "$BLUEPRINT" \
    --bundle-id "$BUNDLE" \
    --key-pair-name "$KEY_PAIR_NAME" \
    --region "$REGION" \
    --user-data "$(cat "$USER_DATA_FILE")" >/dev/null
  echo "  waiting for instance to enter 'running' state..."
  for _ in $(seq 1 60); do
    STATE=$(aws lightsail get-instance --instance-name "$INSTANCE_NAME" --region "$REGION" --query 'instance.state.name' --output text 2>/dev/null || echo pending)
    [ "$STATE" = "running" ] && break
    sleep 5
  done
  [ "$STATE" = "running" ] || { echo "  timed out waiting for instance"; exit 1; }
else
  echo "  instance exists, reusing"
fi

# --- Attach static IP to instance ---
ATTACHED=$(aws lightsail get-static-ip --static-ip-name "$STATIC_IP_NAME" --region "$REGION" --query 'staticIp.attachedTo' --output text 2>/dev/null || echo None)
if [ "$ATTACHED" != "$INSTANCE_NAME" ]; then
  echo "==> attaching static IP to instance"
  aws lightsail attach-static-ip --static-ip-name "$STATIC_IP_NAME" --instance-name "$INSTANCE_NAME" --region "$REGION" >/dev/null
else
  echo "==> static IP already attached"
fi

# --- Open firewall ports (HTTP 80, HTTPS 443; SSH 22 is open by default) ---
echo "==> firewall: HTTP/HTTPS"
aws lightsail open-instance-public-ports \
  --instance-name "$INSTANCE_NAME" \
  --port-info "fromPort=80,toPort=80,protocol=TCP" \
  --region "$REGION" >/dev/null
aws lightsail open-instance-public-ports \
  --instance-name "$INSTANCE_NAME" \
  --port-info "fromPort=443,toPort=443,protocol=TCP" \
  --region "$REGION" >/dev/null

# --- Route 53 A records (apex + www) ---
echo "==> Route 53 records for $DOMAIN"
ZONE_ID=$(aws route53 list-hosted-zones-by-name --dns-name "$DOMAIN" --max-items 1 \
  --query "HostedZones[?Name=='${DOMAIN}.'].Id | [0]" --output text 2>/dev/null || echo None)
if [ "$ZONE_ID" = "None" ] || [ -z "$ZONE_ID" ]; then
  echo "  ERROR: no Route 53 hosted zone found for $DOMAIN."
  echo "  Either create one in Route 53 first, or point your registrar's nameservers at Route 53."
  echo "  (Instance is up at $STATIC_IP; you can come back and run this again once DNS is ready.)"
  exit 1
fi
ZONE_ID="${ZONE_ID#/hostedzone/}"

CHANGE_BATCH=$(cat <<JSON
{
  "Comment": "workshop apex + www → static IP",
  "Changes": [
    { "Action": "UPSERT", "ResourceRecordSet": { "Name": "$DOMAIN.",     "Type": "A", "TTL": 300, "ResourceRecords": [{ "Value": "$STATIC_IP" }] } },
    { "Action": "UPSERT", "ResourceRecordSet": { "Name": "www.$DOMAIN.", "Type": "A", "TTL": 300, "ResourceRecords": [{ "Value": "$STATIC_IP" }] } }
  ]
}
JSON
)
CHANGE_ID=$(aws route53 change-resource-record-sets --hosted-zone-id "$ZONE_ID" \
  --change-batch "$CHANGE_BATCH" --query 'ChangeInfo.Id' --output text)
echo "  submitted: $CHANGE_ID"

# --- Summary ---
cat <<SUMMARY

================================================================
 Deploy complete. Domain → instance plumbing is live.
================================================================
 Domain:        https://$DOMAIN
 Static IP:     $STATIC_IP
 Instance:      $INSTANCE_NAME (Lightsail / $REGION)
 Bundle:        $BUNDLE
 Cloud-init:    runs on instance first boot (~3-5 min total)
 HTTPS cert:    Caddy provisions Let's Encrypt automatically after
                DNS propagates to the static IP (usually <10 min)

 Next steps:
   1. Wait 5-10 minutes for bootstrap + cert. Then curl -I https://$DOMAIN
      should return 200 and show a login page.

   2. Create the first facilitator account. SSH in and run:

      ssh -i $REPO_ROOT/.aws-workshop-key.pem ubuntu@$STATIC_IP
      sudo -u workshop env \$(sudo cat /etc/workshop/app.env | xargs) \\
        /srv/workshop/app/.venv/bin/flask --app backend.app add-admin

   3. Wire up GitHub Actions for push-to-deploy. Add these secrets at
      https://github.com/gunnarstoa/ifp-delivery-workshop/settings/secrets/actions
        - INSTANCE_IP        = $STATIC_IP
        - SSH_PRIVATE_KEY    = paste contents of $REPO_ROOT/.aws-workshop-key.pem

   4. To tear down: ./scripts/aws-destroy.sh

SUMMARY

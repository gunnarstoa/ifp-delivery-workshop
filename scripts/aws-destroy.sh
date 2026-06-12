#!/usr/bin/env bash
# Tear down everything aws-deploy.sh created.
# Leaves the Route 53 hosted zone alone — that costs $0.50/mo and you may want to keep it.
#
# Usage: ./scripts/aws-destroy.sh [domain]
set -euo pipefail

DOMAIN="${1:-anaplan-workshops.com}"
REGION="${AWS_REGION:-us-east-1}"
INSTANCE_NAME="workshop"
STATIC_IP_NAME="workshop-ip"
KEY_PAIR_NAME="${WORKSHOP_KEY_PAIR:-workshop-key}"

echo "==> tearing down workshop deploy for $DOMAIN in $REGION"
read -p "Are you sure? [y/N] " ans
[ "$ans" = "y" ] || [ "$ans" = "Y" ] || { echo "aborted"; exit 0; }

STATIC_IP=$(aws lightsail get-static-ip --static-ip-name "$STATIC_IP_NAME" --region "$REGION" --query 'staticIp.ipAddress' --output text 2>/dev/null || echo)

if [ -n "${STATIC_IP:-}" ] && [ "$STATIC_IP" != "None" ]; then
  echo "==> removing Route 53 records"
  ZONE_ID=$(aws route53 list-hosted-zones-by-name --dns-name "$DOMAIN" --max-items 1 \
    --query "HostedZones[?Name=='${DOMAIN}.'].Id | [0]" --output text 2>/dev/null || echo None)
  if [ "$ZONE_ID" != "None" ] && [ -n "$ZONE_ID" ]; then
    ZONE_ID="${ZONE_ID#/hostedzone/}"
    for NAME in "$DOMAIN" "www.$DOMAIN"; do
      EXISTING=$(aws route53 list-resource-record-sets --hosted-zone-id "$ZONE_ID" \
        --query "ResourceRecordSets[?Name=='${NAME}.' && Type=='A']" --output json)
      if [ "$(echo "$EXISTING" | python3 -c 'import sys,json; print(len(json.load(sys.stdin)))')" -gt 0 ]; then
        BATCH=$(python3 -c "import json,sys; recs=json.loads('''$EXISTING'''); print(json.dumps({'Changes':[{'Action':'DELETE','ResourceRecordSet':r} for r in recs]}))")
        aws route53 change-resource-record-sets --hosted-zone-id "$ZONE_ID" --change-batch "$BATCH" >/dev/null || true
      fi
    done
  fi
fi

echo "==> deleting instance"
aws lightsail delete-instance --instance-name "$INSTANCE_NAME" --region "$REGION" >/dev/null 2>&1 || true

echo "==> releasing static IP"
aws lightsail release-static-ip --static-ip-name "$STATIC_IP_NAME" --region "$REGION" >/dev/null 2>&1 || true

echo "==> deleting key pair (keep the .pem locally if you want to re-use)"
aws lightsail delete-key-pair --key-pair-name "$KEY_PAIR_NAME" --region "$REGION" >/dev/null 2>&1 || true

echo "==> done"

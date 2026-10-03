#!/usr/bin/env bash
set -euo pipefail
cp /etc/systemd/system/crl-pilot.service /etc/systemd/system/crl-pilot-second.service
python3 - <<'PY'
p='/etc/systemd/system/crl-pilot-second.service'
s=open(p).read().replace('CRL private pilot HTTP node','CRL private pilot second HTTP node').replace('events.json --port 8765','events-second.json --port 8766')
open(p,'w').write(s)
PY
systemctl daemon-reload
systemctl enable --now crl-pilot-second
systemctl is-active crl-pilot-second

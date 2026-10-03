#!/usr/bin/env bash
set -euo pipefail
install -d -m 0750 /opt/crl-pilot
base64 -d /tmp/crl-pilot-bundle.b64 | tar -xz -C /opt/crl-pilot
python3 -m venv /opt/crl-pilot/venv
/opt/crl-pilot/venv/bin/pip install --disable-pip-version-check 'cryptography>=44,<48' 'rfc8785>=0.1,<1'
cat > /etc/systemd/system/crl-pilot.service <<'UNIT'
[Unit]
Description=CRL private pilot HTTP node
After=network.target
[Service]
Type=simple
User=crladmin
WorkingDirectory=/opt/crl-pilot
ExecStart=/opt/crl-pilot/venv/bin/python /opt/crl-pilot/crl_server.py --db /var/lib/crl-pilot/events.json --port 8765
Restart=on-failure
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/crl-pilot
PrivateTmp=true
[Install]
WantedBy=multi-user.target
UNIT
install -d -o crladmin -g crladmin -m 0750 /var/lib/crl-pilot
chown -R crladmin:crladmin /opt/crl-pilot
systemctl daemon-reload
systemctl enable --now crl-pilot
systemctl is-active crl-pilot
curl -fsS http://127.0.0.1:8765/health

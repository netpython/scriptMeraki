#!/usr/bin/env python3
"""Contrôle SSID, chiffrement, disponibilité et configuration IP des AP."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from common import *
log = setup('wireless_compliance')
args = base_parser('Conformité Wi-Fi Meraki').parse_args()
cfg = config(args.config)
api = dashboard()
oid = org_id(cfg)
rows = []
aps = []
for n in networks(api, oid):
    if 'wireless' not in n.get('productTypes', []):
        continue
    try:
        for s in api.wireless.getNetworkWirelessSsids(n['id']):
            if not s.get('enabled'):
                continue
            encryption = s.get('encryptionMode') or ''
            auth = s.get('authMode') or ''
            issues = []
            if encryption.lower() in {'wep', ''}:
                issues.append('WEAK_ENCRYPTION')
            if auth.lower() in {'open', 'psk'}:
                issues.append('AUTH_REVIEW')
            rows.append({'network': n['name'], 'ssid': s.get('name'), 'number': s.get('number'), 'auth': auth, 'encryption': encryption, 'ip_assignment': s.get('ipAssignmentMode'), 'vlan': s.get('defaultVlanId'), 'result': 'OK' if not issues else 'WARNING', 'issues': ','.join(issues)})
        for d in [x for x in api.networks.getNetworkDevices(n['id']) if x.get('model', '').startswith('MR')]:
            m = api.devices.getDeviceManagementInterface(d['serial'])
            wan = m.get('wan1', {})
            aps.append({'network': n['name'], 'ap': d.get('name'), 'model': d.get('model'), 'serial': d['serial'], 'mode': 'STATIC' if wan.get('usingStaticIp') else 'DHCP', 'ip': wan.get('staticIp') or d.get('lanIp'), 'result': 'OK' if d.get('name') and d.get('tags') else 'WARNING_METADATA'})
    except Exception as exc:
        rows.append({'network': n['name'], 'result': 'ERROR', 'issues': str(exc)})
log.info('SSID: %s', write_csv('wireless_ssid_compliance', rows))
log.info('AP: %s', write_csv('wireless_ap_compliance', aps))

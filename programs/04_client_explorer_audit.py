#!/usr/bin/env python3
"""Explore les clients filaires/Wi-Fi, consommateurs et équipements inconnus."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from common import *
p = base_parser('Client Explorer Meraki')
p.add_argument('--timespan', type=int, default=86400)
p.add_argument('--search')
args = p.parse_args()
cfg = config(args.config)
api = dashboard()
oid = org_id(cfg)
rows = []
for n in networks(api, oid):
    try:
        for c in api.networks.getNetworkClients(n['id'], timespan=args.timespan, total_pages='all'):
            row = {'network': n['name'], 'hostname': c.get('dhcpHostname') or c.get('description'), 'description': c.get('description'), 'mac': c.get('mac'), 'ip': c.get('ip'), 'type': c.get('recentDeviceConnection'), 'vlan': c.get('vlan'), 'switch_ap': c.get('recentDeviceName'), 'port_ssid': c.get('switchport') or c.get('ssid'), 'manufacturer': c.get('manufacturer'), 'os': c.get('os'), 'status': c.get('status'), 'sent': c.get('usage', {}).get('sent', 0), 'recv': c.get('usage', {}).get('recv', 0)}
            row['total_usage'] = row['sent'] + row['recv']
            if args.search and args.search.lower() not in ' '.join((str(v).lower() for v in row.values())):
                continue
            row['finding'] = 'UNKNOWN_CLIENT' if not row['hostname'] and (not row['manufacturer']) else 'OK'
            rows.append(row)
    except Exception as exc:
        rows.append({'network': n['name'], 'finding': 'ERROR', 'error': str(exc)})
rows.sort(key=lambda x: x.get('total_usage', 0), reverse=True)
log = setup('client_explorer')
log.info('%s', write_csv('client_explorer', rows))

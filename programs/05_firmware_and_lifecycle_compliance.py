#!/usr/bin/env python3
"""Compare firmwares par produit et prépare l'audit cycle de vie/SKU."""
from __future__ import annotations
import sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from common import *
log = setup('firmware_lifecycle')
args = base_parser('Firmware et lifecycle Meraki').parse_args()
cfg = config(args.config)
api = dashboard()
oid = org_id(cfg)
names = network_name_map(api, oid)
devices = api.organizations.getOrganizationDevices(oid, total_pages='all')
by_model = Counter((d.get('model', 'UNKNOWN') for d in devices))
rows = []
for n in networks(api, oid):
    try:
        data = api.networks.getNetworkFirmwareUpgrades(n['id'])
        for product, x in data.get('products', {}).items():
            current = x.get('currentVersion', {}).get('shortName', '')
            nextv = x.get('nextUpgrade', {}).get('toVersion', {}).get('shortName', '')
            status = x.get('nextUpgrade', {}).get('status', '')
            rows.append({'network': n['name'], 'product': product, 'current': current, 'next': nextv, 'upgrade_status': status, 'finding': 'PENDING_UPGRADE' if nextv and nextv != current else 'OK'})
    except Exception as exc:
        rows.append({'network': n['name'], 'finding': 'ERROR', 'error': str(exc)})
models = [{'model': m, 'quantity': q, 'lifecycle_status': 'TO_VERIFY', 'verification_date': '', 'confidence': 'LOW', 'notes': 'Validate EoL/EoS against Cisco official notice'} for m, q in sorted(by_model.items())]
log.info('Firmware: %s', write_csv('firmware_compliance', rows))
log.info('Lifecycle: %s', write_csv('lifecycle_inventory', models))

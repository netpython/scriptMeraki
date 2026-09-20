#!/usr/bin/env python3
import time
from rich.console import Console
from rich.table import Table
from common import *
p=base_parser("Monitoring live Meraki"); p.add_argument("--refresh",type=int,default=60); p.add_argument("--alerts-only",action="store_true"); args=p.parse_args(); cfg=config(args.config); api=dashboard(); oid=org_id(cfg); console=Console(); names=network_name_map(api,oid); wanted=set(cfg.get("device_tags",{}).get(k,k) for k in ("production_switch","production_ap"))
try:
    while True:
        devices={d["serial"]:d for d in api.organizations.getOrganizationDevices(oid,total_pages="all") if wanted&set(d.get("tags",[]))}; statuses=api.organizations.getOrganizationDevicesStatuses(oid,total_pages="all")
        offline=Table(title="Équipements offline"); alerts=Table(title="Alertes");
        for t in (offline,alerts):
            for c in ("Réseau","Équipement","Modèle","État"): t.add_column(c)
        for s in statuses:
            d=devices.get(s.get("serial"));
            if not d: continue
            row=(names.get(d.get("networkId"),""),d.get("name") or d["serial"],d.get("model",""),s.get("status",""))
            if s.get("status")=="offline": offline.add_row(*row)
            elif s.get("status")!="online": alerts.add_row(*row)
        console.clear(); console.print(offline); console.print(alerts); console.print(f"Actualisation: {args.refresh}s — Ctrl+C pour quitter")
        time.sleep(args.refresh)
except KeyboardInterrupt: console.print("[yellow]Monitoring arrêté proprement.[/yellow]")

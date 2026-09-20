#!/usr/bin/env python3
from common import *
log=setup("alerts_audit"); args=base_parser("Audit alertes").parse_args(); cfg=config(args.config); api=dashboard(); oid=org_id(cfg); rows=[]
for n in networks(api,oid):
    try:
        data=api.networks.getNetworkAlertsSettings(n["id"])
        for a in data.get("alerts",[]): rows.append({"network":n["name"],"type":a.get("type"),"enabled":a.get("enabled"),"filters":json.dumps(a.get("filters",{})),"recipients":json.dumps(a.get("alertDestinations",{}))})
    except Exception as exc: rows.append({"network":n["name"],"error":str(exc)})
log.info("Export: %s",write_csv("alerts",rows))


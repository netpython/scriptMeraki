#!/usr/bin/env python3
from common import *
log=setup("firmware_audit"); args=base_parser("Audit firmware").parse_args(); cfg=config(args.config); api=dashboard(); oid=org_id(cfg)
rows=[]
for n in networks(api,oid):
    try:
        fw=api.networks.getNetworkFirmwareUpgrades(n["id"])
        for product,data in fw.get("products",{}).items(): rows.append({"network":n["name"],"product":product,"current":data.get("currentVersion",{}).get("shortName"),"next":data.get("nextUpgrade",{}).get("toVersion",{}).get("shortName"),"status":data.get("nextUpgrade",{}).get("status")})
    except Exception as exc: rows.append({"network":n["name"],"error":str(exc)})
log.info("Export: %s",write_csv("firmware_audit",rows))


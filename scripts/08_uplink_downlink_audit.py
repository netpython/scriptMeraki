#!/usr/bin/env python3
from common import *
log=setup("uplink_downlink"); args=base_parser("Audit uplink/downlink").parse_args(); cfg=config(args.config); api=dashboard(); oid=org_id(cfg); names=network_name_map(api,oid); tags=cfg.get("device_tags",{}); rows=[]
for d in api.organizations.getOrganizationDevices(oid,total_pages="all"):
    role=next((r for r in ("uplink","downlink") if tags.get(r,r) in d.get("tags",[])),None)
    if role: rows.append({"network":names.get(d.get("networkId"),""),"device":d.get("name"),"serial":d.get("serial"),"model":d.get("model"),"role":role,"tags":",".join(d.get("tags",[]))})
log.info("Export: %s",write_csv("uplink_downlink",rows))


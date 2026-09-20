#!/usr/bin/env python3
from common import *
log=setup("mx_vlan_audit"); args=base_parser("Audit VLAN MX").parse_args(); cfg=config(args.config); api=dashboard(); oid=org_id(cfg); rows=[]
for n in networks(api,oid):
    if "appliance" not in n.get("productTypes",[]): continue
    try:
        for v in api.appliance.getNetworkApplianceVlans(n["id"]): rows.append({"network":n["name"],"id":v.get("id"),"name":v.get("name"),"subnet":v.get("subnet"),"applianceIp":v.get("applianceIp"),"dhcpHandling":v.get("dhcpHandling")})
    except Exception as exc: rows.append({"network":n["name"],"error":str(exc)})
log.info("Export: %s",write_csv("mx_vlans",rows))


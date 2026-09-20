#!/usr/bin/env python3
from common import *
log=setup("ssid_audit"); args=base_parser("Audit SSID").parse_args(); cfg=config(args.config); api=dashboard(); oid=org_id(cfg); rows=[]
for n in networks(api,oid):
    if "wireless" not in n.get("productTypes",[]): continue
    for s in api.wireless.getNetworkWirelessSsids(n["id"]): rows.append({"network":n["name"],"number":s.get("number"),"name":s.get("name"),"enabled":s.get("enabled"),"authMode":s.get("authMode"),"encryptionMode":s.get("encryptionMode"),"ipAssignmentMode":s.get("ipAssignmentMode"),"vlanId":s.get("defaultVlanId")})
log.info("Export: %s",write_csv("ssids",rows))


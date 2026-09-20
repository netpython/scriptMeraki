#!/usr/bin/env python3
from common import *
log=setup("organization_inventory"); args=base_parser("Inventaire Meraki").parse_args(); cfg=config(args.config); api=dashboard(); oid=org_id(cfg)
names=network_name_map(api,oid); devices=api.organizations.getOrganizationDevices(oid,total_pages="all")
rows=[{"network":names.get(d.get("networkId"),""),"name":d.get("name"),"model":d.get("model"),"serial":d.get("serial"),"mac":d.get("mac"),"lanIp":d.get("lanIp"),"tags":",".join(d.get("tags",[]))} for d in devices]
log.info("Export: %s",write_csv("organization_inventory",rows))


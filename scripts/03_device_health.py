#!/usr/bin/env python3
from common import *
log=setup("device_health"); args=base_parser("Santé des équipements").parse_args(); cfg=config(args.config); api=dashboard(); oid=org_id(cfg)
names=network_name_map(api,oid); statuses=api.organizations.getOrganizationDevicesStatuses(oid,total_pages="all")
rows=[{"network":names.get(x.get("networkId"),""),"name":x.get("name"),"serial":x.get("serial"),"model":x.get("model"),"status":x.get("status"),"lanIp":x.get("lanIp"),"publicIp":x.get("publicIp")} for x in statuses]
log.info("Export: %s",write_csv("device_health",rows))


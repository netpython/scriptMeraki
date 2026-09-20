#!/usr/bin/env python3
from common import *
log=setup("config_backup"); args=base_parser("Sauvegarde configurations Meraki").parse_args(); cfg=config(args.config); api=dashboard(); oid=org_id(cfg); backup={"organizationId":oid,"networks":[]}
for n in networks(api,oid):
    item={"network":n,"devices":api.networks.getNetworkDevices(n["id"])}
    if "wireless" in n.get("productTypes",[]): item["ssids"]=api.wireless.getNetworkWirelessSsids(n["id"])
    if "switch" in n.get("productTypes",[]): item["switchSettings"]=api.switch.getNetworkSwitchSettings(n["id"])
    backup["networks"].append(item)
log.info("Backup: %s",write_json("meraki_config_backup",backup))


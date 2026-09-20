#!/usr/bin/env python3
from common import *
log=setup("ap_ip_mode"); args=base_parser("IP statique ou DHCP des AP").parse_args(); cfg=config(args.config); api=dashboard(); oid=org_id(cfg); n=choose_network(api,oid); rows=[]
for d in [x for x in api.networks.getNetworkDevices(n["id"]) if x.get("model","").startswith("MR")]:
    mgmt=api.devices.getDeviceManagementInterface(d["serial"]); wan=mgmt.get("wan1",{})
    rows.append({"network":n["name"],"ap":d.get("name"),"model":d.get("model"),"serial":d["serial"],"mode":wan.get("usingStaticIp") and "STATIC" or "DHCP","ip":wan.get("staticIp") or d.get("lanIp"),"vlan":wan.get("vlan")})
log.info("Export: %s",write_csv("ap_ip_mode",rows))


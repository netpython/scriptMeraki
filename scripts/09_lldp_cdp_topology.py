#!/usr/bin/env python3
from common import *
log=setup("topology"); args=base_parser("Topologie LLDP/CDP").parse_args(); cfg=config(args.config); api=dashboard(); oid=org_id(cfg); names=network_name_map(api,oid); data=api.organizations.getOrganizationDevicesUplinksAddressesByDevice(oid,total_pages="all"); rows=[]
for d in api.organizations.getOrganizationDevices(oid,total_pages="all"):
    if not d.get("model","").startswith("MS"): continue
    try:
        for x in api.switch.getDeviceSwitchPortsStatuses(d["serial"]):
            nb=x.get("lldp") or x.get("cdp")
            if nb: rows.append({"network":names.get(d.get("networkId"),""),"switch":d.get("name"),"port":x.get("portId"),"protocol":"LLDP" if x.get("lldp") else "CDP","neighbor":json.dumps(nb,ensure_ascii=False)})
    except Exception as exc: rows.append({"switch":d.get("name"),"error":str(exc)})
log.info("Export: %s",write_csv("lldp_cdp_topology",rows))


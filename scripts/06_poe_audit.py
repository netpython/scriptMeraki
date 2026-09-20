#!/usr/bin/env python3
from common import *
log=setup("poe_audit"); p=base_parser("Audit PoE ports d'accès"); p.add_argument("--network-id"); args=p.parse_args(); cfg=config(args.config); api=dashboard(); oid=org_id(cfg); n={"id":args.network_id,"name":args.network_id} if args.network_id else choose_network(api,oid); rows=[]
for d in [x for x in api.networks.getNetworkDevices(n["id"]) if x.get("model","").startswith("MS")]:
    status=api.switch.getDeviceSwitchPortsStatuses(d["serial"]); max_port=24 if "24" in d.get("model","") else int(cfg.get("poe_access_ports",{}).get("default",48))
    access=[x for x in status if str(x.get("portId","")).isdigit() and int(x["portId"])<=max_port]; used=sum(float(x.get("powerUsageInWh") or 0) for x in access)
    rows.append({"network":n["name"],"switch":d.get("name"),"model":d.get("model"),"accessPorts":max_port,"poeActivePorts":sum(bool(x.get("isPoeEnabled")) and float(x.get("powerUsageInWh") or 0)>0 for x in access),"poeUsageWh":round(used,2)})
log.info("Export: %s",write_csv("poe_audit",rows))


#!/usr/bin/env python3
from common import *
log=setup("switch_ports"); p=base_parser("Audit des ports MS"); p.add_argument("--network-id"); args=p.parse_args(); cfg=config(args.config); api=dashboard(); oid=org_id(cfg)
n={"id":args.network_id,"name":args.network_id} if args.network_id else choose_network(api,oid)
devices=[d for d in api.networks.getNetworkDevices(n["id"]) if d.get("model","").startswith("MS")]; rows=[]
for d in devices:
    statuses={str(x["portId"]):x for x in api.switch.getDeviceSwitchPortsStatuses(d["serial"])}
    for port in api.switch.getDeviceSwitchPorts(d["serial"]):
        s=statuses.get(str(port["portId"]),{}); rows.append({"network":n["name"],"switch":d.get("name"),"port":port["portId"],"name":port.get("name"),"enabled":port.get("enabled"),"status":s.get("status"),"speed":s.get("speed"),"duplex":s.get("duplex"),"type":port.get("type"),"vlan":port.get("vlan"),"allowedVlans":port.get("allowedVlans"),"poeEnabled":port.get("poeEnabled"),"powerUsageWh":s.get("powerUsageInWh"),"neighbor":json.dumps(s.get("lldp") or s.get("cdp") or {},ensure_ascii=False)})
log.info("Export: %s",write_csv("switch_ports",rows))


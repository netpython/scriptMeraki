#!/usr/bin/env python3
"""Audit détaillé capacité switch, PoE, ports libres et voisins réseau."""
from __future__ import annotations
import re,sys
from pathlib import Path
from openpyxl import Workbook
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from common import *
log=setup("switch_capacity_poe");args=base_parser("Capacité et PoE Meraki").parse_args();cfg=config(args.config);api=dashboard();oid=org_id(cfg);names=network_name_map(api,oid);ports=[];summary=[]
for d in [x for x in api.organizations.getOrganizationDevices(oid,total_pages="all") if x.get("model","").startswith("MS")]:
 try:
  conf={str(x["portId"]):x for x in api.switch.getDeviceSwitchPorts(d["serial"])};stats=api.switch.getDeviceSwitchPortsStatuses(d["serial"]);match=re.search(r"(24|48)",d.get("model",""));max_access=int(match.group(1)) if match else 48;used=poe=free=0
  for s in stats:
   pid=str(s.get("portId",""));is_access=pid.isdigit() and int(pid)<=max_access
   if not is_access:continue
   c=conf.get(pid,{});active=s.get("status")=="Connected" or str(s.get("status","")).lower()=="connected";power=float(s.get("powerUsageInWh") or 0);used+=int(active);free+=int(not active);poe+=power
   ports.append({"network":names.get(d.get("networkId"),""),"switch":d.get("name"),"model":d.get("model"),"serial":d["serial"],"port":pid,"name":c.get("name"),"status":s.get("status"),"vlan":c.get("vlan"),"type":c.get("type"),"poe_enabled":c.get("poeEnabled"),"poe_usage_wh":power,"neighbor":json.dumps(s.get("lldp") or s.get("cdp") or {},ensure_ascii=False)})
  summary.append({"network":names.get(d.get("networkId"),""),"switch":d.get("name"),"model":d.get("model"),"access_ports":max_access,"used":used,"free":free,"utilization_pct":round(100*used/max_access,1),"poe_usage_wh":round(poe,2),"result":"WARNING_CAPACITY" if used/max_access>=.8 else "OK"})
 except Exception as exc:summary.append({"switch":d.get("name"),"result":"ERROR","error":str(exc)})
wb=Workbook();wb.remove(wb.active)
for title,data in (("Summary",summary),("Ports",ports)):
 ws=wb.create_sheet(title);headers=sorted({k for r in data for k in r}) or ["result"];ws.append(headers)
 for r in data:ws.append([r.get(h,"") for h in headers])
 ws.freeze_panes="A2";ws.auto_filter.ref=ws.dimensions
path=OUTPUT/f"switch_capacity_poe_{stamp()}.xlsx";wb.save(path);log.info("%s",path)

